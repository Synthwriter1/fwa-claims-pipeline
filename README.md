# fwa-claims-pipeline
A Python-based IQR anomaly detection pipeline for healthcare claims and FWA identification.

### Executive Summary
In value-based care and HEOR, identifying revenue leakage requires separating routine clinical variance from true Fraud, Waste, and Abuse (FWA). This project features an automated, deterministic Python data pipeline that ingests raw synthetic healthcare claims (50,000 records), applies Interquartile Range (IQR) algorithms to detect billing anomalies, and calculates patient clinical risk using HCC (Hierarchical Condition Category) weights. 

The pipeline outputs directly to a Tableau executive dashboard, successfully isolating a highly concentrated pocket of financial risk: **$3,627,282.57 in tied-up capital across 245 flagged claims in the Gastroenterology department.**

<img width="1909" height="856" alt="Image" src="https://github.com/user-attachments/assets/b6e54f91-549f-44a4-8708-5ddd6679b751" />


### Tech Stack
* **Python (Pandas):** Data ingestion, synthetic anomaly injection, probabilistic risk scoring, and deterministic IQR outlier calculations.
* **SQLite / CSV:** Flat-file database management and staging.
* **Tableau:** Front-end executive visualization and operational targeting.

### Methodology & Pipeline Architecture
The Python pipeline executes a multi-module analytical framework in a single pass:

* **01. Data Ingestion & Synthetic Generation:** Built a local SQLite database to ingest raw flat files, applying a Log-Normal distribution matrix via Pandas to accurately simulate the real-world financial skew of healthcare claims data before staging it for analysis.
* **02. Baseline Department Variance:** Aggregates total spend and claim counts to establish normal clinical cost distributions (e.g., standard Evaluation & Management codes averaging ~$300/claim).
* **03. Clinical Risk Scoring (RAF):** Maps diagnostic codes (ICD-10) to HCC weights to calculate individual Patient Risk Adjustment Factor (RAF) scores, identifying high-acuity populations.
* **04. FWA Anomaly Detection:** Applies a strict Interquartile Range algorithm to flag highly abnormal claim amounts escaping the normal distribution (Upper Bound = $Q3 + 1.5 \times IQR$).
* **05. Utilization Management:** Merges financial flags with clinical acuity to build a 4-quadrant targeting matrix, isolating "Frequent Flyer" patients (High ER utilization + Low Clinical Risk).
* **06. Provider Penalty Box:** Aggregates FWA flags by Provider ID to generate a targeted audit list for compliance and revenue integrity teams.

### Key Findings & Business Impact
* **Targeted Revenue Leakage:** The IQR algorithm bypassed 49,000 routine hospital visits to pinpoint exactly 245 anomalous Gastroenterology claims, quantifying over $3.6M in auditable waste without relying on machine learning models.
* **Actionable Provider Audits:** The Provider Scorecard isolated specific actors (e.g., PR0238, PR0078) driving the highest volume of outlier claims, enabling immediate compliance intervention.
* **Operational Efficiency:** The Utilization Quadrant successfully identified low-risk patients with 3+ ER visits, providing care management teams with a deterministic call list to reduce unnecessary hospital utilization.
