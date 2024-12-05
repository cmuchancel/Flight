
import matplotlib.pyplot as plt
from math import sqrt
from vpython import vector, mag, norm
from Ball import Ball
from Environment import Environment

# Initialize parameters
initial_spin_rates = range(1, 1001, 1)  # From 50 to 1000 in steps of 50
terminal_velocity_vectors = []  # To store terminal velocity vectors

# Function to normalize a vector
def normalize(vector_input):
    magnitude = mag(vector_input)
    return vector_input / magnitude if magnitude != 0 else vector(0, 0, 0)

# Simulate for each spin rate
for spin_rate in initial_spin_rates:
    # Initialize a projectile with the given spin rate
    projectile = Ball(
        mass=1.011e-8,
        radius=0.00005,
        initial_position=vector(0, 1000, 0),
        initial_velocity=vector(0, 0, 0),
        initial_angular_speed=spin_rate,
        initial_rot_direction="counterclockwise"
    )
    
    # Initialize environment
    environment = Environment()
    
    # Terminal velocity simulation variables
    dt = 0.001
    velocity_tolerance = 0.00001
    stable_counter = 0
    consecutive_stable_steps = 1000
    previous_velocity_magnitude = None
    terminal_velocity_flag = False

    while projectile.pos.y >= 2 * projectile.radius:  # Using vpython.vector's .y attribute
        # Calculate forces
        gravity_force = environment.calculate_force_gravity(projectile)
        drag_force = environment.calculate_drag_force(projectile)
        lift_force = environment.calculate_lift_force(projectile)
        net_force = gravity_force + drag_force + lift_force

        # Apply net force
        environment.apply_net_force(projectile, net_force, dt)

        # Check for terminal velocity
        current_velocity_magnitude = mag(projectile.vel)
        if previous_velocity_magnitude is not None:
            if abs(current_velocity_magnitude - previous_velocity_magnitude) < velocity_tolerance:
                stable_counter += 1
                if stable_counter >= consecutive_stable_steps:
                    terminal_velocity_flag = True
                    terminal_velocity_vectors.append(normalize(projectile.vel))
                    print(f"Spin rate: {spin_rate}, Terminal velocity: {projectile.vel}")
                    break
            else:
                stable_counter = 0
        previous_velocity_magnitude = current_velocity_magnitude

    if not terminal_velocity_flag:
        terminal_velocity_vectors.append(normalize(projectile.vel))
        print(f"Spin rate: {spin_rate}, Terminal velocity (not stabilized): {projectile.vel}")

# Plotting
plt.figure(figsize=(12, 8))
for i, spin_rate in enumerate(initial_spin_rates):
    velocity_vector = terminal_velocity_vectors[i]
    plt.quiver(
        spin_rate, 0, velocity_vector.x, velocity_vector.y, angles="xy", scale_units="xy", scale=1, color="blue"
    )

plt.title("Normalized Terminal Velocity Vectors vs. Initial Spin Rate")
plt.xlabel("Initial Spin Rate (rad/s)")
plt.ylabel("Normalized Terminal Velocity Vector")
plt.xlim(0, 1050)
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.show()
