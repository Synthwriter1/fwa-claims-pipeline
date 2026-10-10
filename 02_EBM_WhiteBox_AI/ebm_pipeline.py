import os
# Force underlying math engines to use exactly 1 thread, preventing memory spikes during import
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'

import pandas as pd
from sklearn.model_selection import train_test_split
from interpret.glassbox import ExplainableBoostingClassifier
from interpret import show  

# Load the synthetic claims dataset
load_path = r"C:\Users\damic\OneDrive\Desktop\Portfolio One files\claims_expanded.csv"
df = pd.read_csv(load_path)
print(df.columns.tolist())

# Convert the boolean True/False into 1 and 0 for the model
df['is_anomaly'] = df['is_anomaly'].astype(int)

# Define features and target
features = [
    'provider_specialty', 
    'department', 
    'cpt_code', 
    'diagnosis_code', 
    'patient_age', 
    'risk_score'
]

target = 'is_anomaly'

X = df[features]
y = df[target]

# Standard 80/20 split for validation, stratified to handle rare anomalies
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Initialize the model using a single job to maintain memory control
ebm = ExplainableBoostingClassifier(interactions=10, random_state=42, n_jobs=1)

print("Training the Explainable Boosting Machine...")
ebm.fit(X_train, y_train)

print("Generating Global Dashboard...")
ebm_global = ebm.explain_global()
show(ebm_global)

print("Generating Local Dashboard for Highest Risk Anomalies...")

# Calculate the raw probability percentages (predict_proba) instead of the rigid 0/1 predictions
probabilities = ebm.predict_proba(X_test)[:, 1]

# Create a temporary dataframe to rank the actual anomalies by the AI's suspicion level
results = pd.DataFrame({'actual': y_test, 'prob': probabilities})
top_anomalies = results[results['actual'] == 1].sort_values(by='prob', ascending=False).head(5)

# Isolate the top 5 most suspicious claims
X_top = X_test.loc[top_anomalies.index]
y_top = y_test.loc[top_anomalies.index]

# Generate the dashboard
ebm_local = ebm.explain_local(X_top, y_top)
show(ebm_local)

input("Dashboards are live! Press Enter in this terminal to shut down the server and exit...")