from math import *
from vpython import *
from PlotManager import PlotManager
from Environment import Environment
from Ball import Ball

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
max_t=10

#Calculated Variables
velocity_initial = vector(initial_horizontal_velocity,  initial_vertical_velocity, initial_z_velocity)
momentum_initial = (ball_mass * velocity_initial)

# Initialize objects

environment = Environment()

ball = Ball(mass=ball_mass, radius=ball_radius,
            initial_position=vector(0, drop_height, 0),
            initial_velocity=velocity_initial)

plot_manager = PlotManager(max_time=10, max_x=1.5, max_y=drop_height * 1.05, max_y_velocity=15)

# Set up the canvas
scene = canvas(title = 'Dropping a ball', caption = 'Hopefully this works',
               center = vector(0, drop_height//2, 0), background = color.white)
left_wall = box(pos = vector(0-2*ball_radius,drop_height//2,0),size = vector(1,9,5),color=color.red)
floor = box(pos=vector(9,0,0),size = vector(21,1,5),color=color.green)
visual_ball = sphere(pos=ball.pos, radius=ball.radius, color=color.orange)

while(ball.pos.y >= 2 * ball.radius or ball.pos.x <= left_wall.pos.x):
    rate(25)
  # Calculate forces
    gravity_force = environment.calculate_gravity(ball)
   #drag_force = environment.calculate_drag(ball)
    net_force = gravity_force #+ drag_force

    # Apply forces and update position
    ball.apply_net_force(net_force, dt)
    visual_ball.pos = ball.pos  # Update visual representation of the ball

    # Update plots
    plot_manager.update(t, ball)
    
    t = t + dt

