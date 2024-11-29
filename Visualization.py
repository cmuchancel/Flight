from sympy import Curve
from vpython import canvas, box, sphere, vector, color, cylinder, curve
from math import *
from Ball import Ball  # Import Ball class


class Visualization:
    def __init__(self, projectile):
        # Set up the scene
        self.scene = canvas(title='Dropping a projectile', caption='Hopefully this works',
                            center=vector(0, projectile.pos.y / 2, 0), background=color.white)

          # Create walls and floor
        self.left_wall = box(pos=vector(-10, 700, 0),
                             size=vector(10, 600, 5), color=color.red)
        self.floor = box(pos=vector(40, 400, 0), size=vector(100, 10, 5), color=color.green)
        projectile.trail = curve(color=color.magenta)
        projectile.trail.append(pos=projectile.pos)
          # Create the projectile visualization based on type
        if isinstance(projectile, Ball):
            # Create a sphere if the projectile is a Ball
            self.projectile_visual = sphere(pos=projectile.pos, 
                                            radius=10, 
                                            color=color.orange)
        else:
            raise ValueError("Unsupported projectile type")
        
    def update_projectile_position(self, position):
        # Update the position of the projectile in the visualization
        self.projectile_visual.pos = position