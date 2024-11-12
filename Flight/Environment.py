from vpython import *

class Environment:
    # Constants
    G = 6.67e-11
    earth_mass = 5.792e24
    earth_radius = 6.371e6 
    air_density = 1.225 
    air_temperature_celsius = 20  

    def __init__(self):
        pass  # No need for instance-specific initialization unless required

    def calculate_force_gravity(self, ball):
        height = ball.pos.y
        return ((self.G * self.earth_mass * ball.mass) / (self.earth_radius + height) ** 2) * vector(0, -1, 0)
    
    def calculate_torque_gravity(self, ball):
        # Gravity acts at the center of mass, so torque due to gravity is zero
        gravity_force = self.calculate_force_gravity(ball)
        lever_arm = vector(0, 0, 0)  # Acts on Center of mass, so lever arm is zero
        return lever_arm.cross(gravity_force)  # Should return vector(0, 0, 0)

    def calculate_dynamic_viscosity_coefficient(self):
        degrees_kelvin = self.air_temperature_celsius + 273.15                      
        mu_nought = 1.733e-5  # Pa*s
        T_nought = 288.2  # Kelvin
        mu = mu_nought * ((degrees_kelvin / T_nought) ** 2) * ((degrees_kelvin + 110.4) / (T_nought + 110.4))
        return mu
    
    def calculate_reynolds_number(self, ball):
        # Calculate the dynamic viscosity using the air temperature
        dynamic_viscosity = self.calculate_dynamic_viscosity_coefficient()
        
        # Calculate freestream velocity
        freestream_velocity = mag(ball.vel)
        
        # Use diameter as the reference length for a sphere
        reference_length = 2 * ball.radius  # Diameter of the sphere
        
        # Reynolds number formula: Re = (rho * V * L) / mu
        reynolds_number = (self.air_density * freestream_velocity * reference_length) / dynamic_viscosity
        return reynolds_number

    def calculate_drag_coefficient(self, reynolds_number):
        # Calculate the drag coefficient based on Reynolds number using the given equation
        term1 = 24 / reynolds_number
        term2 = (2.6 * (reynolds_number / 5.0)) / (1 + (reynolds_number / 5.0) ** 1.52)
        term3 = (0.411 * (reynolds_number / 2.63e5) ** -7.94) / (1 + (reynolds_number / 2.63e5) ** -8.00)
        term4 = (0.25 * (reynolds_number / 1e6)) / (1 + (reynolds_number / 1e6))
        drag_coefficient = term1 + term2 + term3 + term4
        return drag_coefficient

    def calculate_drag(self, ball):
        # Calculate Reynolds number
        reynolds_number = self.calculate_reynolds_number(ball)
        
        # Calculate drag coefficient based on Reynolds number
        drag_coefficient = self.calculate_drag_coefficient(reynolds_number)
        
        # Calculate the drag force: F_d = 0.5 * C_d * rho * V^2 * A
        drag_magnitude = 0.5 * drag_coefficient * self.air_density * mag(ball.vel) ** 2 * pi * ball.radius ** 2
        return -drag_magnitude * ball.vel.norm()  # Direction opposite to velocity
