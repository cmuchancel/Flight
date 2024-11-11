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
rotational_velocity_initial = 0

#Runtime Variables
dt= 0.01
t=0
plottedTime=2

# Initialize objects

environment = Environment()

ball = Ball(mass=ball_mass, radius=ball_radius, initial_position=vector(0, drop_height, 0), initial_velocity=vector(initial_horizontal_velocity,  initial_vertical_velocity, initial_z_velocity))

plot_manager = PlotManager(time_flight=plottedTime, max_x=1.5, max_y=drop_height * 1.05, max_y_velocity=15)

visualization = Visualization(ball_radius=ball_radius, drop_height=drop_height)

while(ball.pos.y >= 2 * ball.radius):
    rate(25)
  # Calculate forces
    gravity_force = environment.calculate_gravity(ball)
   #drag_force = environment.calculate_drag(ball) WE NEED TO REDO DRAG FORCE
    net_force = gravity_force #+ drag_force

    # Apply forces and update position
    ball.apply_net_force(net_force, dt)

    #Update Visualization
    visualization.update_ball_position(ball.pos)

    # Update plots
    plot_manager.update(t, ball)
    
    t = t + dt

