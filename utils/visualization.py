import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Visualization:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def plot_path(self, ownship_path, uav_path):
        """
        Plot the paths of the ownship and UAV in 3D space.

        Parameters:
        ownship_path (list): List of ownship positions as (latitude, longitude, altitude).
        uav_path (list): List of UAV positions as (latitude, longitude, altitude).
        """
        ownship_path = np.array(ownship_path)
        uav_path = np.array(uav_path)

        self.ax.plot(ownship_path[:, 0], ownship_path[:, 1], ownship_path[:, 2], label='Ownship', color='blue')
        self.ax.plot(uav_path[:, 0], uav_path[:, 1], uav_path[:, 2], label='UAV', color='red')

        self.ax.set_xlabel('Latitude')
        self.ax.set_ylabel('Longitude')
        self.ax.set_zlabel('Altitude')
        self.ax.legend()
        plt.savefig("simulation_result.png")
        plt.show()