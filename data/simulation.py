from data.space_objects import Ownship, UAV
import numpy as np

class Simulation:
    def __init__(self, ownship, uav, model, time_step=0.1, max_time=100):
        """
        Initialize the simulation environment.

        Parameters:
        ownship (Ownship): The ownship object.
        uav (UAV): The interceptor UAV.
        model (object): Machine learning model for UAV control.
        time_step (float): Simulation time step in seconds.
        max_time (float): Maximum simulation time in seconds.
        """
        self.ownship = ownship
        self.uav = uav
        self.model = model
        self.time_step = time_step
        self.max_time = max_time
        self.time_elapsed = 0

    def run(self, ownship_strategy):
        """
        Run the simulation loop.

        Parameters:
        ownship_strategy (callable): Function to update ownship's movement.
        """
        while self.time_elapsed < self.max_time:
            self.ownship.update(ownship_strategy)
            self.uav.intercept(self.ownship, self.model)
            self.time_elapsed += self.time_step
            self._log_state()

    def _log_state(self):
        """
        Log the state of the simulation for debugging and analysis.
        """
        print(f"Time: {self.time_elapsed:.2f}s")
        print(f"Ownship Position: ({self.ownship.latitude:.2f}, {self.ownship.longitude:.2f}, {self.ownship.altitude:.2f})")
        print(f"UAV Position: ({self.uav.latitude:.2f}, {self.uav.longitude:.2f}, {self.uav.altitude:.2f})")