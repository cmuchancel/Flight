from math import *
from vpython import *

#Constants 
G = 6.67e-11
earth_mass = 5.792e24
earth_radius = 6.371e6
air_density = 1.225 #kg/m^3

#Variables
drop_height = 10
ball_mass = 0.5
ball_radius = 0.5

#Initial Velocities
initial_horizontal_velocity = 1
initial_vertical_velocity = 0
initial_z_velocity = 0

#Runtime Variables
dt= 0.01
t=0
max_t=10

#Calculated Variables
momentum_initial = ball_mass * vector(initial_horizontal_velocity,  initial_horizontal_velocity, initial_z_velocity)



# Set up the canvas
scene = canvas(title = 'Dropping a ball', caption = 'Hopefully this works',
               center = vector(0, drop_height//2, 0), background = color.white)
left_wall = box(pos = vector(0-2*ball_radius,drop_height//2,0),size = vector(1,9,5),color=color.red)
floor = box(pos=vector(9,0,0),size = vector(21,1,5),color=color.green)
ball = sphere(pos = vector(0,drop_height,0,),radius = ball_radius, color = color.orange)

#Initializing object variables from instance variables
ball.mass = ball_mass
ball.mom = momentum_initial
gravity = vector(0,-9.8*ball.mass,0) #THIS IS NOT HOW WE SHOULD DO THIS

#Plots 
s='<b>X Position over Time</b>'
graph(title = s, xtitle = 'Time', ytitle = 'X position',xmin = 0,xmax = max_t*1.05, 
      ymax = drop_height*1.05, ymin = 0)
#
drawX = gcurve(color=color.cyan, label='X Pos')



while(t<max_t):
    rate(25)
    t = t + dt
# Stuff to move the ball
    #Attempted drag force calculations
    ball.speed = mag(ball.mom/ball.mass)
    F_drag = vector(-0.5*air_density*ball.speed**2*0.47*pi*ball_radius**2,0,0)
    
# For later
    #gravity = G * earth_mass*ball_mass/(earth_radius+ball.pos.x)**2
    ball.force = gravity 
    ball.mom += ball.force*dt
    ball.pos += ball.mom / ball.mass * dt
    if ball.pos.y <= 2*ball.radius:
        break
    if ball.pos.x<=left_wall.pos.x:
        break

    drawX.plot(pos=(t,ball.pos.x))

#Gravity stuff
    