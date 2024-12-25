import json
import os
import shutil
import socket

import imageio.v2 as imageio
from matplotlib import pyplot as plt

from data.space_objects import Ownship, UAV
from data.simulation import Simulation
from ml.model import PlaceholderModel,random_movement_strategy
from utils.performance_metrics import calculate_metrics
from utils.visualization import Visualization



def main():
    # Initialize ownship and UAV objects
    ownship = Ownship(latitude=0, longitude=0, altitude=1000)
    uav = UAV(latitude=-10, longitude=-10, altitude=800)

    # Initialize placeholder model
    model = PlaceholderModel()

    # Initialize simulation
    time_step = 1/30  # Time step in seconds for 30 Hz frequency
    max_time = 60  # Maximum simulation time in seconds (1 minute)
    simulation = Simulation(ownship, uav, model, time_step, max_time)

    # UDP socket setup
    udp_ip = "127.0.0.1"
    udp_port = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Lists to store paths for visualization
    ownship_path = []
    uav_path = []
    frames_dir = "frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    def custom_log_state(sim):
        ownship_path.append((sim.ownship.latitude, sim.ownship.longitude, sim.ownship.altitude))
        uav_path.append((sim.uav.latitude, sim.uav.longitude, sim.uav.altitude))

        # Send data via UDP
        data = {
            "ownship": {
                "latitude": sim.ownship.latitude,
                "longitude": sim.ownship.longitude,
                "altitude": sim.ownship.altitude
            },
            "uav": {
                "latitude": sim.uav.latitude,
                "longitude": sim.uav.longitude,
                "altitude": sim.uav.altitude
            }
        }
        sock.sendto(json.dumps(data).encode('utf-8'), (udp_ip, udp_port))

        # Generate visualization for the current step
        step = int(sim.time_elapsed / time_step)
        if step % 10 == 0:  # Log progress every 10 steps
            print(f"Simulation progress: Step {step}, Time elapsed: {sim.time_elapsed:.2f}s")

        # Generate visualization for the current step
        step = int(sim.time_elapsed / time_step)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(*zip(*ownship_path), label="Ownship", color="blue")
        ax.scatter(*zip(*uav_path), label="UAV", color="red")

        ax.set_xlabel("Latitude")
        ax.set_ylabel("Longitude")
        ax.set_zlabel("Altitude")
        ax.legend()

        plt.title(f"Step {step}")
        plt.savefig(os.path.join(frames_dir, f"frame_{step:04d}.png"))
        plt.close()

    # Run the simulation with the logging
    simulation._log_state = lambda: custom_log_state(simulation)
    simulation.run(random_movement_strategy)

    images = []
    for frame_file in sorted(os.listdir(frames_dir)):
        if frame_file.endswith(".png"):
            images.append(imageio.imread(os.path.join(frames_dir, frame_file)))

    imageio.mimsave("simulation.gif", images, duration=0.1)

    # Calculate and display performance metrics
    metrics = calculate_metrics(ownship_path, uav_path)
    print("Performance Metrics:", metrics)

    # Visualize the results
    visualization = Visualization()
    visualization.plot_path(ownship_path, uav_path)

    # Calculate and display performance metrics
    metrics = calculate_metrics(ownship_path, uav_path)
    print("Performance Metrics:", metrics)

    # Close the UDP socket
    sock.close()


if __name__ == "__main__":
    main()