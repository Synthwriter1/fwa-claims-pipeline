import pandas as pd
import numpy as np
import sqlite3

# Spin up the local SQLite database & build the empty table
conn = sqlite3.connect('healthcare_claims.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS claims_expanded")
cursor.execute('''
CREATE TABLE claims_expanded (
    claim_id TEXT, patient_id TEXT, provider_id TEXT, facility_id TEXT,
    patient_age INTEGER, gender TEXT, state TEXT, days_to_process INTEGER, 
    risk_score REAL, network_status TEXT, claim_status TEXT,
    provider_specialty TEXT, department TEXT, cpt_code TEXT,
    diagnosis_code TEXT, flag_1 INTEGER, claim_amount REAL,
    paid_amount REAL, ratio REAL, flag_2 INTEGER, service_date TEXT,
    service_location TEXT
)
''')
# Read the raw SQL text file
with open(r"C:\Users\damic\OneDrive\Desktop\claims_expanded.sql", 'r') as file:
    conn.executescript(file.read())
df = pd.read_sql_query("SELECT * FROM claims_expanded", conn)

# Apply Realistic Baseline Costs (Log-Normal Distribution)
np.random.seed(42)
df['paid_amount'] = np.random.lognormal(mean=5.2, sigma=1.0, size=len(df)).round(2)
specialist_mask = df['department'] == 'Specialist'
gastro_indices = df[specialist_mask].sample(frac=0.25, random_state=42).index
df.loc[gastro_indices, 'department'] = 'Gastroenterology'
gastro_mask = df['department'] == 'Gastroenterology'
outlier_indices = df[gastro_mask].sample(frac=0.05, random_state=42).index
df.loc[outlier_indices, 'paid_amount'] = np.random.uniform(15000, 45000, size=len(outlier_indices)).round(2)

# FORCE SAVE TO DOWNLOADS 
save_path = r"C:\Users\damic\OneDrive\Desktop\Portfolio One files\claims_expanded.csv"
df.to_csv(save_path, index=False)
print(f"Master file successfully saved to: {save_path}")