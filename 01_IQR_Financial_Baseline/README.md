# Phase 1: Deterministic Baseline & IQR Financial Modeling

This module establishes the financial baseline for the anomaly detection pipeline. Before applying complex machine learning, it is critical to use deterministic, mathematically auditable frameworks to quantify actual economic exposure.

## Files in this Module
* `01_data_generation_pipeline.py`: Ingests the raw synthetic medical claims, handles missing values, and prepares the dataset for statistical analysis.
* `02_analytics_modules.py`: Applies John Tukey's Interquartile Range (IQR) methodology to isolate high-variance cost clusters across provider specialties.
* `build_clean_claims_table.sql`: ETL script for data cleaning, validation, and table creation.
* `claims_expanded_clean.sql`: SQL dump containing raw claims data and insertion queries.
* `financial_leakage_summary.png` (Screenshot): Visual proofs isolating 245 outlier claims and pinpointing $3.6 million in auditable financial leakage within the Gastroenterology subset.

## Methodology & Business Value
This module intentionally avoids "black-box" predictions in favor of hard statistical thresholds. By defining anomalies via strict IQR multipliers, healthcare economics and compliance operations can generate immediate, legally defensible utilization management (UM) targets before deploying predictive AI.
