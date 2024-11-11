from vpython import vector, pi

class Environment:

    #Constants 
    G = 6.67e-11
    earth_mass = 5.792e24
    earth_radius = 6.371e6 
    air_density = 1.225 

    def __init__(self):
        pass  # No need for instance-specific initialization unless required

    def calculate_gravity(self, ball):
        height = ball.pos.y
        return ((self.G * self.earth_mass * ball.mass) / (self.earth_radius + height) ** 2) * vector(0, -1, 0)

    def calculate_drag(self, ball):
        drag_magnitude = 0.5 * self.air_density * ball.vel.mag**2 * 0.47 * pi * ball.radius**2
        return -drag_magnitude * ball.vel.norm()