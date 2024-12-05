from math import *
from vpython import *
from PlotManager import PlotManager
from Environment import Environment
from Ball import Ball
from Visualization import Visualization
import matplotlib.pyplot as plt
import pandas as pd
from tqdm.notebook import tqdm  # Use tqdm.notebook for Jupyter compatibility

# Parameters for the loop
initial_angular_speeds = range(1, 1001, 1)  # From 1 to 1000 in increments of 5
terminal_velocities = []  # To store terminal velocities for each angular speed
terminal_x_velocities = []  # To store terminal x velocities
terminal_y_velocities = []  # To store terminal y velocities

# Loop through initial angular speeds with a progress bar
for angular_speed in tqdm(initial_angular_speeds, desc="Simulating angular speeds"):
    print(f"Simulating for initial angular speed: {angular_speed}")  # Debugging print
    # Reinitialize projectile with the new angular speed
    projectile = Ball(
        mass=1.011 * 10**(-8),
        radius=0.00005,
        initial_position=vector(0, 1000, 0),
        initial_velocity=vector(0, 0, 0),
        initial_angular_speed=angular_speed,
        initial_rot_direction="counterclockwise"
    )

    # Reinitialize environment and visualization objects
    environment = Environment()
    visualization = Visualization(projectile)

    # Reinitialize tracking variables
    dt = 0.001
    t = 0
    velocity_tolerance = 0.00001  # Range within which the velocity is considered constant
    consecutive_stable_steps = 1000  # Number of consecutive stable steps needed
    stable_counter = 0
    terminal_velocity_flag = False
    previous_velocity_magnitude = None

    # Simulation loop
    while projectile.pos.y >= 2 * projectile.radius:
        # Forces
        gravity_force = environment.calculate_force_gravity(projectile)
        drag_force = environment.calculate_drag_force(projectile)
        lift_force = environment.calculate_lift_force(projectile)
        buoyant_force = environment.calculate_buoyant_force(projectile)
        net_force = gravity_force + drag_force + lift_force + buoyant_force

        # Torques
        torque = environment.calculate_torque(projectile)
        net_torque = torque

        # Apply forces and torques
        environment.apply_net_force(projectile, net_force, dt)
        environment.apply_net_torque(projectile, net_torque, dt)

        # Update time and velocity tracking
        t += dt
        current_velocity_magnitude = mag(projectile.vel)

        # Check for terminal velocity
        if previous_velocity_magnitude is not None:
            if abs(current_velocity_magnitude - previous_velocity_magnitude) < velocity_tolerance:
                stable_counter += 1
                if stable_counter >= consecutive_stable_steps:
                    terminal_velocity_flag = True
                    terminal_velocities.append(current_velocity_magnitude)
                    terminal_x_velocities.append(projectile.vel.x)
                    terminal_y_velocities.append(projectile.vel.y)
                    break
            else:
                stable_counter = 0

        # Update the previous velocity value
        previous_velocity_magnitude = current_velocity_magnitude

    # Append terminal velocities if not already added
    if not terminal_velocity_flag:
        terminal_velocities.append(mag(projectile.vel))
        terminal_x_velocities.append(projectile.vel.x)
        terminal_y_velocities.append(projectile.vel.y)

# Store the results in a DataFrame
df = pd.DataFrame({
    'Initial Angular Speed (rad/s)': initial_angular_speeds,
    'Terminal Velocity (m/s)': terminal_velocities,
    'Terminal X Velocity (m/s)': terminal_x_velocities,
    'Terminal Y Velocity (m/s)': terminal_y_velocities
})

# Output the DataFrame to an Excel file
output_file = "terminal_velocity_results.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

# Notify user
print(f"Data saved to {output_file}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(initial_angular_speeds, terminal_velocities, marker='o', linestyle='-', color='b')
plt.title("Effect of Initial Angular Speed on Terminal Velocity")
plt.xlabel("Initial Angular Speed (rad/s)")
plt.ylabel("Terminal Velocity (m/s)")
plt.grid(True)
plt.show()
