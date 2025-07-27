from sklearn.cluster import KMeans
import numpy as np

# print("clustering_engine.py")

def run_clustering(features, n_clusters=3):
    """
    Clusters the metrics data using KMeans.
    Returns the cluster labels and cluster centers.
    """
    if features.shape[0] == 0:
        print("[WARNING] Empty feature set passed to clustering.")
        return [], []
    
    try:
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(features)
        return kmeans.labels_, kmeans.cluster_centers_
    except Exception as e:
        print(f"[ERROR] Clustering failed: {e}")
        return [], []
