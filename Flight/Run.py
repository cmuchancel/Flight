from math import *
from vpython import *
from PlotManager import PlotManager
from Environment import Environment
from Ball import Ball
from Visualization import Visualization


#Variables
drop_height = 10
ball_mass = 0.5
ball_radius = 0.5

#Initial Velocities
initial_horizontal_velocity = 1
initial_vertical_velocity = 0
initial_z_velocity = 0
initial_rotational_speed = 0
initial_rotational_direction = "counterclockwise"

#Runtime Variables
dt= 0.01
t=0
plottedTime=2

# Initialize objects
environment = Environment()
ball = Ball(mass=ball_mass, radius=ball_radius, initial_position=vector(0, drop_height, 0), initial_velocity=vector(initial_horizontal_velocity, initial_vertical_velocity, initial_z_velocity),initial_angular_speed = initial_rotational_speed, initial_rot_direction = initial_rotational_direction)
plot_manager = PlotManager(time_flight=plottedTime, max_x=1.5, max_y=drop_height * 1.05, max_y_velocity=15, max_angular_velocity=5)
visualization = Visualization(ball_radius=ball_radius, drop_height=drop_height)

#RUN IT
while(ball.pos.y >= 2 * ball.radius):
    rate(25)
    # Calculate forces   (ADD DRAG FORCE, ADD MAGNUS EFFECT PSUEDOFORCE)
    gravity_force = environment.calculate_force_gravity(ball)
    gravity_torque = environment.calculate_torque_gravity(ball)
    drag_force = environment.calculate_drag(ball)
    net_force = gravity_force + drag_force
    net_torque = gravity_torque 
    # Calculate Torques
    
    # Apply forces 
    ball.apply_net_force(net_force, dt)
    ball.apply_net_torque(net_torque, dt)

    #Update Visualization
    visualization.update_ball_position(ball.pos)

    # Update plots
    plot_manager.update(t, ball)
    
    t = t + dt

