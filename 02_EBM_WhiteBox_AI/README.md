# Phase 2: Explainable Boosting Machine (EBM) Pipeline

This module scales the anomaly detection established in Phase 1 by deploying a transparent machine learning model. Using the `InterpretML` framework, this pipeline predicts the probability of medical upcoding while outputting exact, mathematically auditable weights for every feature.

## Files in this Module
* `ebm_pipeline.py`: The core Python script that trains the Explainable Boosting Classifier on the synthetic claims dataset.
* `requirements.txt`: Environment dependencies needed to run the model.
* `Screenshot (167).png`: Global Feature Importance dashboard demonstrating the macro-level drivers of upcoding.
* `Screenshot (173).png`: Local Waterfall chart providing single-claim proof of an anomaly within the Gastroenterology subset.

## How to Run Locally
To execute this pipeline and generate the InterpretML dashboard locally, ensure you have Python installed and run the following commands in your terminal:

```bash
# Install required dependencies
pip install -r requirements.txt

# Execute the pipeline
python ebm_pipeline.py
