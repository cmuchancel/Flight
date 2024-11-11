from math import *
from vpython import *

# Initializing Constants 

G = 6.67e-11
drop_height = 10
ball_mass = 0.5
earth_mass = 5.792e24
earth_radius = 6.371e6
ball_radius = 0.5
air_density = 1.225 #kg/m^3
dt=0.01
t=0
max_t=10
# Set up the canvas

scene = canvas(title = 'Dropping a ball', caption = 'Hopefully this works',
               center = vector(0, drop_height//2, 0), background = color.white)
left_wall = box(pos=vector(0-2*ball_radius,drop_height//2,0),size=vector(1,9,5),color=color.red)
floor = box(pos=vector(9,0,0),size=vector(21,1,5),color=color.green)
ball = sphere(pos = vector(0,drop_height,0,),radius = ball_radius, color = color.orange)

#Plots 
s='<b>X Position over Time</b>'
graph(title=s, xtitle='Time', ytitle='X position',xmin=0,xmax=max_t*1.05, 
      ymax=drop_height*1.05, ymin=0)
#
drawX = gcurve(color=color.cyan, label='X Pos')

#Stuff to make the things work or something
ball.mass=ball_mass
ball.mom = vector(0,0,0)
gravity = vector(0,-9.8*ball.mass,0)
initial_horiz_force = vector(2.5,0,0)
while(t<max_t):
    rate(25)
    t = t + dt
# Stuff to move the ball
    #Attempted drag force calculations
    ball.speed = mag(ball.mom/ball.mass)
    F_drag = vector(-0.5*air_density*ball.speed**2*0.47*pi*ball_radius**2,0,0)
    
# For later
    #gravity = G * earth_mass*ball_mass/(earth_radius+ball.pos.x)**2
    ball.force = gravity + initial_horiz_force
    ball.mom += ball.force*dt
    ball.pos += ball.mom / ball.mass * dt
    if ball.pos.y <= 2*ball.radius:
        break
    if ball.pos.x<=left_wall.pos.x:
        break

    drawX.plot(pos=(t,ball.pos.x))

#Gravity stuff
    