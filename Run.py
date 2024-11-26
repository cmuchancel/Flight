from math import *
from vpython import *
from PlotManager import PlotManager
from Environment import Environment
from Ball import Ball
from Visualization import Visualization


# Terminal velocity tracking
velocity_tolerance = 0.00001  # Range within which the velocity is considered constant
consecutive_stable_steps = 1000  # Number of consecutive stable steps needed
stable_counter = 0  # Counter for stable velocity
terminal_velocity_flag = False  # Flag to indicate if terminal velocity is reached
previous_velocity_magnitude = None  # Variable to store the previous velocity value

#Initialize projectile
projectile = Ball(
   
    mass = 1.011 * 10**(-8),
    radius = 0.00005,
    initial_position = vector(0, 1000, 0),
    initial_velocity = vector(0, 0, 0),
    initial_angular_speed = 0,
    initial_rot_direction = "counterclockwise"

    )
print(f"Initial angular velocity: {projectile.angular_velocity}")


'''projectile = Disk(
    mass = 0.5,
    radius = 0.5,
    thickness = .01,
    initial_position = vector(0, 10, 0),
    initial_velocity = vector(0, 0, 0),
    initial_angular_speed = 0,
    initial_rot_direction = "counterclockwise"
)'''


#Runtime Variables
dt= 0.001
t=0
plottedTime=100

# Auto Initialized other class objects
environment = Environment()


plot_manager = PlotManager(

    time_flight=plottedTime, 
    max_x=100, 
    max_y=projectile.pos.y * 1.05, 
    max_y_velocity=100, 
    max_angular_velocity=1000,
    max_reynolds = 200,
    max_force = 1 * 10**(-7),
    max_dimensionless_angular_velocity = 4
    )

visualization = Visualization(projectile)

while(projectile.pos.y >= 2 * projectile.radius and not terminal_velocity_flag):  #CHANGE FOR DISK
    rate(1000000000)
    # Calculate forces   (ADD DRAG FORCE, ADD MAGNUS EFFECT PSUEDOFORCE)
    gravity_force = environment.calculate_force_gravity(projectile)
    drag_force = environment.calculate_drag_force(projectile)
    lift_force = environment.calculate_lift_force(projectile)
    net_force = gravity_force + drag_force + lift_force
    # Calculate Torques
    torque = environment.calculate_torque(projectile)
    net_torque = torque

    # Apply forces and torque 
    environment.apply_net_force(projectile, net_force, dt)
    environment.apply_net_torque(projectile, net_torque, dt)

    #Update Visualization
    visualization.update_projectile_position(projectile.pos)

    # Update plots
    plot_manager.update(t, projectile)
    t = t + dt
    print(mag(projectile.vel))

    # Get current velocity magnitude
    current_velocity_magnitude = mag(projectile.vel)

    if previous_velocity_magnitude is not None:  # Only check if we have a previous value
        if abs(current_velocity_magnitude - previous_velocity_magnitude) < velocity_tolerance:
            stable_counter += 1
            if stable_counter >= consecutive_stable_steps and not terminal_velocity_flag:
                terminal_velocity_flag = True
                print(f"Terminal velocity reached: {current_velocity_magnitude:.3f} m/s at t = {t:.3f} seconds")
                plot_manager.update_xmax(t)  # Rescale the plots

        else:
            stable_counter = 0  # Reset counter if velocity is not stable

    # Update the previous velocity value
    previous_velocity_magnitude = current_velocity_magnitude

