import numpy as np

def calculate_metrics(ownship_path, uav_path):
    """
    Calculate performance metrics for the simulation.

    Parameters:
    ownship_path (list): List of ownship positions as (latitude, longitude, altitude).
    uav_path (list): List of UAV positions as (latitude, longitude, altitude).

    Returns:
    dict: Dictionary of performance metrics.
    """
    ownship_path = np.array(ownship_path)
    uav_path = np.array(uav_path)

    distances = np.linalg.norm(ownship_path - uav_path, axis=1)
    mean_distance = np.mean(distances)
    max_distance = np.max(distances)
    min_distance = np.min(distances)

    return {
        "mean_distance": mean_distance,
        "max_distance": max_distance,
        "min_distance": min_distance
    }
