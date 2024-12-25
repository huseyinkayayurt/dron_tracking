import math
import numpy as np

class SpaceObject:
    def __init__(self, latitude, longitude, altitude, roll=0, pitch=0, yaw=0):
        """
        Base class for objects in 3D space.

        Parameters:
        latitude (float): Latitude coordinate in degrees.
        longitude (float): Longitude coordinate in degrees.
        altitude (float): Altitude in meters.
        roll (float): Roll angle in degrees.
        pitch (float): Pitch angle in degrees.
        yaw (float): Yaw angle in degrees.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def move(self, lat_delta, lon_delta, alt_delta):
        """
        Update the position of the object in 3D space.

        Parameters:
        lat_delta (float): Change in latitude.
        lon_delta (float): Change in longitude.
        alt_delta (float): Change in altitude.
        """
        self.latitude += lat_delta
        self.longitude += lon_delta
        self.altitude += alt_delta

    def rotate(self, roll_delta, pitch_delta, yaw_delta):
        """
        Update the orientation of the object.

        Parameters:
        roll_delta (float): Change in roll angle.
        pitch_delta (float): Change in pitch angle.
        yaw_delta (float): Change in yaw angle.
        """
        self.roll += roll_delta
        self.pitch += pitch_delta
        self.yaw += yaw_delta

class Ownship(SpaceObject):
    def __init__(self, latitude, longitude, altitude, roll=0, pitch=0, yaw=0):
        super().__init__(latitude, longitude, altitude, roll, pitch, yaw)

    def update(self, strategy):
        """
        Update ownship position using a movement strategy.

        Parameters:
        strategy (callable): Function to determine movement deltas.
        """
        deltas = strategy(self)
        self.move(*deltas)

class UAV(SpaceObject):
    def __init__(self, latitude, longitude, altitude, roll=0, pitch=0, yaw=0):
        super().__init__(latitude, longitude, altitude, roll, pitch, yaw)

    def intercept(self, ownship, model):
        """
        Perform an interception maneuver.

        Parameters:
        ownship (Ownship): The target to intercept.
        model (callable): Machine learning model to predict movement.
        """
        input_features = self._prepare_input(ownship)
        deltas = model.predict(input_features)
        self.move(*deltas[:3])
        self.rotate(*deltas[3:])

    def _prepare_input(self, ownship):
        """
        Prepare input features for the ML model.

        Parameters:
        ownship (Ownship): The target to intercept.

        Returns:
        np.ndarray: Feature vector for ML model.
        """
        return np.array([
            self.latitude - ownship.latitude,
            self.longitude - ownship.longitude,
            self.altitude - ownship.altitude,
            self.roll - ownship.roll,
            self.pitch - ownship.pitch,
            self.yaw - ownship.yaw
        ])