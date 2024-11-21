from math import *
from vpython import *
from PlotManager import PlotManager
from Environment import Environment
from Ball import Ball
from Visualization import Visualization


#Initialize projectile
projectile = Ball(
   
    mass = 0.5,
    radius = 0.00005,
    initial_position = vector(0, 10, 0),
    initial_velocity = vector(0, 0, 0),
    initial_angular_speed = 1,
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
plottedTime=2

# Auto Initialized other class objects
environment = Environment()


plot_manager = PlotManager(

    time_flight=plottedTime, 
    max_x=1.5, 
    max_y=projectile.pos.y * 1.05, 
    max_y_velocity=15, 
    max_angular_velocity=5,
    max_reynolds = 10000

    )

visualization = Visualization(projectile)

while(projectile.pos.y >= 2 * projectile.radius):  #CHANGE FOR DISK
    rate(1000000)
    # Calculate forces   (ADD DRAG FORCE, ADD MAGNUS EFFECT PSUEDOFORCE)
    gravity_force = environment.calculate_force_gravity(projectile)
    drag_force = environment.calculate_drag_force(projectile)
    net_force = gravity_force + drag_force
    # Calculate Torques
    gravity_torque = environment.calculate_torque_gravity(projectile)
    drag_torque = environment.calculate_drag_torque(projectile)
    net_torque = gravity_torque + drag_torque
    # Apply forces 
    environment.apply_net_force(projectile, net_force, dt)
    environment.apply_net_torque(projectile, net_torque, dt)

    #Update Visualization
    visualization.update_projectile_position(projectile.pos)

    # Update plots
    plot_manager.update(t, projectile)
    print(environment.calculate_reynolds_number(projectile))
    t = t + dt

