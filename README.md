# Healthcare Claims Analytics & Transparent FWA Detection Pipeline

**Author:** Greg D'Amico  
**Articles & Technical Breakdown:** [Catching a $3.6 Million Leak (Medium)](https://medium.com/@gregdamico82)

## Executive Summary
Advanced analytics in healthcare compliance often operate as a "black box," making it impossible to legally or financially defend machine learning findings during high-stakes audits or commercial disputes. This repository demonstrates an end-to-end, mathematically defensible pipeline for detecting Fraud, Waste, and Abuse (FWA) within medical claims. 

Processing a synthetic dataset of 50,000 medical claims, this project establishes a deterministic financial baseline using Interquartile Range (IQR) logic to quantify economic exposure, and subsequently deploys an Explainable Boosting Machine (EBM) to isolate complex multi-variable upcoding behaviors while maintaining 100% algorithmic transparency. 

## Repository Architecture

```text
fwa-claims-pipeline/
│
├── data/
│   └── claims_expanded.csv             # 50,000-record dataset modeling real billing distributions
│
├── 01_IQR_Financial_Baseline/               # Phase 1: Deterministic Modeling
│   ├── 01_data_generation_pipleine.py       # SQLite ingestion and Pandas data cleaning
│   ├── 02_analytics_modules.py              # Statistical outlier isolation algorithms
│   ├── fwa_sql_queries.sql                  # SQL schema and raw claims data extraction
│   └── (Tableau Dashboards)                 # Visual proofs of $3.6M Gastroenterology variance
│
├── 02_EBM_WhiteBox_AI/                      # Phase 2: Transparent Machine Learning
│   ├── ebm_pipeline.py                      # InterpretML training and scoring pipeline
│   ├── requirements.txt                     # Environment dependencies
│   └── (InterpretML Dashboards)             # Global Feature Importance & Local Waterfall charts
│
└── README.md                                # Master project documentation
