# Healthcare Claims Analytics & Transparent FWA Detection Pipeline

**Author:** Greg D'Amico

**Articles & Technical Breakdown:**
* **Phase One:** [Catching a $3.6 Million Leak (Medium)](https://medium.com/@gregdamico82/catching-a-3-6-million-leak-a-transparent-data-pipeline-for-fwa-detection-bff984f7f08d?sharedUserId=gregdamico82)
* **Phase Two:** [Beyond the Baseline: Uncovering Multivariate Fraud with an Explainable Boosting Machine (Medium)](https://medium.com/@gregdamico82/beyond-the-baseline-uncovering-multivariate-fraud-with-an-explainable-boosting-machine-3209b0bd16a6?sharedUserId=gregdamico82)

## Executive Summary
Advanced analytics in healthcare compliance often operate as ‘black boxes,’ making machine‑learning findings impossible to legally or financially defend during high‑stakes audits or commercial disputes. This repository demonstrates an end-to-end, mathematically defensible pipeline for detecting Fraud, Waste, and Abuse (FWA) within medical claims. 

Processing a synthetic dataset of 50,000 medical claims, this project establishes a deterministic financial baseline using Interquartile Range (IQR) logic to quantify economic exposure, and subsequently deploys an Explainable Boosting Machine (EBM) to isolate complex multi-variable upcoding behaviors while maintaining 100% algorithmic transparency. 

## Repository Architecture

```text
fwa-claims-pipeline/
│
├── data/
│   └── claims_expanded.csv             # 50,000-record dataset modeling real billing distributions
│
├── 01_IQR_Financial_Baseline/               # Phase 1: Deterministic Modeling
│   ├── 01_data_generation_pipleine.py       # SQLite ingestion and log-normal financial variance modeling
│   ├── 02_analytics_modules.py              # Statistical outlier isolation algorithms
│   ├── build_clean_claims_table.sql         # ETL script for data cleaning, validation, and table creation
│   ├── claims_expanded_clean.sql            # SQL dump containing raw claims data and insertion queries
│   └── (Tableau Dashboards)                 # Visual proofs of $3.6M Gastroenterology variance
│
├── 02_EBM_WhiteBox_AI/                      # Phase 2: Transparent Machine Learning
│   ├── ebm_pipeline.py                      # InterpretML training and scoring pipeline
│   ├── requirements.txt                     # Environment dependencies
│   └── (InterpretML Dashboards)             # Global Feature Importance & Local Waterfall charts
│
└── README.md                                # Master project documentation
