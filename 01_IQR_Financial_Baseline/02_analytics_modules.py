import pandas as pd

# Load the master dataset (Read-only, no np.random here!)
load_path = r"C:\Users\damic\OneDrive\Desktop\Portfolio One files\claims_expanded.csv"
df = pd.read_csv(load_path)
save_folder = r"C:\Users\damic\OneDrive\Desktop\Portfolio One files\\"

# ---------------------------------------------------------
# Module 1 (Verification Only)
# ---------------------------------------------------------
dept_summary = df.groupby('department').agg(
    Total_Spend=('paid_amount', 'sum'),
    Claim_Count=('paid_amount', 'count')
).reset_index()

dept_summary['Avg_Cost_Per_Claim'] = dept_summary['Total_Spend'] / dept_summary['Claim_Count']
dept_summary = dept_summary.sort_values(by='Total_Spend', ascending=False)
dept_summary.to_csv(save_folder + 'm1_department_summary.csv', index=False)

print("\nVerified Baseline Departments by Spend:")
print(dept_summary.head(6))

# ---------------------------------------------------------
# Module 2: Mapping HCC/RAF scores
# ---------------------------------------------------------
hcc_weights = {
    'E11.9': 0.104,  # Type 2 Diabetes
    'I50.9': 0.331,  # Heart Failure
    'J44.9': 0.328,  # COPD
    'C34.90': 2.51,  # Lung Cancer
    'F32.9': 0.395   # Major Depressive Disorder
}

df['hcc_weight'] = df['diagnosis_code'].map(hcc_weights).fillna(0)

patient_risk = df.groupby('patient_id').agg(
    total_spend=('paid_amount', 'sum'),
    total_hcc_weight=('hcc_weight', 'sum') 
).reset_index()

patient_risk['total_raf_score'] = 0.35 + patient_risk['total_hcc_weight']
patient_risk['risk_adjusted_cost'] = patient_risk['total_spend'] / patient_risk['total_raf_score']
patient_risk = patient_risk.sort_values(by='risk_adjusted_cost', ascending=False)

print("\nTop 5 Patients by Risk-Adjusted Cost:")
print(patient_risk.head())
patient_risk.to_csv(save_folder + 'm2_patient_risk_scores.csv', index=False)

# ---------------------------------------------------------
# Module 3: FWA (Payment Integrity)
# ---------------------------------------------------------
# 1. Calculate IQR thresholds using .transform() to safely preserve all columns
Q1 = df.groupby('department')['paid_amount'].transform(lambda x: x.quantile(0.25))
Q3 = df.groupby('department')['paid_amount'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

# 2. Flag the anomalies
df['is_anomaly'] = df['paid_amount'] > upper_bound

# 3. Isolate Gastroenterology and Calculate the Financial Impact
gastro_anomalies = df[(df['department'] == 'Gastroenterology') & (df['is_anomaly'] == True)]
gastro_impact_total = gastro_anomalies['paid_amount'].sum()
gastro_anomaly_count = len(gastro_anomalies)

print(f"\nTotal capital tied up in Gastroenterology anomalies: ${gastro_impact_total:,.2f}")
print(f"Number of flagged Gastroenterology claims to audit: {gastro_anomaly_count}")

# 4. Export all anomalies across the network for Tableau scatterplot
anomalies_df = df[df['is_anomaly'] == True]
anomalies_df.to_csv(save_folder + 'm3_flagged_audits.csv', index=False)
# ---------------------------------------------------------
# Module 4: Utilization Management 
# ---------------------------------------------------------
ed_visits = df[df['service_location'] == 'ER']
inpatient_stays = df[df['service_location'] == 'Inpatient']

patient_ed_counts = ed_visits.groupby('patient_id').size().reset_index(name='ed_visit_count')
patient_ip_counts = inpatient_stays.groupby('patient_id').size().reset_index(name='inpatient_admissions')

risk_df = pd.read_csv(save_folder + 'm2_patient_risk_scores.csv')
um_dashboard = risk_df.merge(patient_ed_counts, on='patient_id', how='left').fillna(0)
um_dashboard = um_dashboard.merge(patient_ip_counts, on='patient_id', how='left').fillna(0)

um_dashboard['is_frequent_flyer'] = (um_dashboard['ed_visit_count'] >= 3) | (um_dashboard['inpatient_admissions'] >= 2)
um_dashboard = um_dashboard.sort_values(by=['ed_visit_count', 'inpatient_admissions'], ascending=False)

print("\nTop 5 Utilization Management Targets (Frequent Flyers):")
print(um_dashboard[['patient_id', 'total_raf_score', 'ed_visit_count', 'inpatient_admissions']].head())
um_dashboard.to_csv(save_folder + 'm4_utilization.csv', index=False)

# ---------------------------------------------------------
# Module 5: Provider Scorecard
# ---------------------------------------------------------
provider_scorecard = df.groupby('provider_id').agg(
    Total_Generated_Spend=('paid_amount', 'sum'),
    Claim_Count=('paid_amount', 'count'),
    FWA_Flagged_Claims=('is_anomaly', 'sum') 
).reset_index()

provider_scorecard['Avg_Cost_Per_Claim'] = provider_scorecard['Total_Generated_Spend'] / provider_scorecard['Claim_Count']
provider_scorecard = provider_scorecard.sort_values(by='FWA_Flagged_Claims', ascending=False)
provider_scorecard.to_csv(save_folder + 'm5_provider_scorecard.csv', index=False)

df.to_csv(save_folder + 'claims_expanded.csv', index=False)

print("All 5 Analytics CSVs successfully generated in Desktop Folder!")
