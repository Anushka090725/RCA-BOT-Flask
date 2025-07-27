import numpy as np

# print("preprocess.py")

def preprocess_metrics(metrics):
    """
    Converts raw metric data into numerical features for clustering.
    Assumes input is a list of dicts with 'value' keys.
    """
    try:
        values = [float(metric.get("value", 0)) for metric in metrics if "value" in metric]
        print("values to preprocess metrics",values)
        return np.array(values).reshape(-1, 1)
    except Exception as e:
        print(f"[ERROR] Preprocessing metrics failed: {e}")
        
        return np.array([]).reshape(-1, 1)
