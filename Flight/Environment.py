from vpython import *
from Ball import Ball  # Import Ball class
import math  # Import math module
from Exceptions import ReValueError, RrValueError, DragCoefficientUnknownError



class Environment:
    # Constants
    G = 6.67e-11
    earth_mass = 5.792e24
    earth_radius = 6.371e6 
    air_density = 1.225 
    air_temperature_celsius = 20  

    def __init__(self):
        pass  # No need for instance-specific initialization unless required

    def calculate_force_gravity(self, projectile):
        height = projectile.pos.y
        return ((self.G * self.earth_mass * projectile.mass) / (self.earth_radius + height) ** 2) * vector(0, -1, 0)
    
    def calculate_torque_gravity(self, projectile):
        # Gravity acts at the center of mass, so torque due to gravity is zero
        gravity_force = self.calculate_force_gravity(projectile)
        lever_arm = vector(0, 0, 0)  # Acts on Center of mass, so lever arm is zero
        return lever_arm.cross(gravity_force)  # Should return vector(0, 0, 0)

    @staticmethod
    def calculate_dynamic_viscosity_coefficient():
        degrees_kelvin = Environment.air_temperature_celsius + 273.15                      
        mu_nought = 1.733e-5  # Pa*s
        T_nought = 288.2  # Kelvin
        mu = mu_nought * ((degrees_kelvin / T_nought) ** 2) * ((degrees_kelvin + 110.4) / (T_nought + 110.4))
        return mu
    
    @staticmethod
    def calculate_reynolds_number_p(projectile):  #Works for Spheres, in form from Cambridge Paper
        
        # Calculate the dynamic viscosity using the air temperature
        mu_dynamic_viscosity_coefficient = Environment.calculate_dynamic_viscosity_coefficient()
        
        # Calculate freestream velocity
        freestream_velocity = mag(projectile.vel)
        
        # Use diameter as the reference length for a sphere
        reference_length = 2 * projectile.radius  

        gamma_kinematic_viscosity = mu_dynamic_viscosity_coefficient / Environment.air_density
        
        # Reynolds number formula: Re = (rho * V * L) / mu
        reynolds_number_p = (reference_length * freestream_velocity) / gamma_kinematic_viscosity
        projectile.reynolds_number = reynolds_number_p
        return reynolds_number_p
    
    def calculate_dimensionless_rotation_rate(self, projectile):
        # Calculate the dynamic viscosity using the air temperature
        mu_dynamic_viscosity_coefficient = Environment.calculate_dynamic_viscosity_coefficient()
       
        # Use diameter as the reference length for a sphere
        reference_length = 2 * projectile.radius  

        gamma_kinematic_viscosity = mu_dynamic_viscosity_coefficient / Environment.air_density

        Re_ohm = ( mag(projectile.angular_velocity) * projectile.radius**2 ) / (gamma_kinematic_viscosity)

        Re_p = self.calculate_reynolds_number_p(projectile)

        if Re_p == 0:
            return "No freestream velocity"

        R_r = Re_ohm / Re_p 
        return R_r


    def calculate_lift_coefficient(self,projectile):
        
        re_p = self.calculate_reynolds_number_p(projectile) #Reynolds number 
        r_r = self.calculate_dimensionless_rotation_rate(projectile) #dimensionless rotation rate
    
        lift_coefficient_shear_flow = 0 #coefficinet of lift due to shear flow is 0 because our atmosphere is "stationary"


        #CALCULATE COEFFICIENT OF LIFT DUE TO ROTATION:

        if re_p == 0 or r_r == "No freestream velocity": # Chance "If it's not moving then there's no drag"
            return 0

        if re_p <= 0.1: # Loth eq 12
            lift_coefficient_rotation= r_r * (1 - ( 0.675 +  0.15 * (1 + math.tanh( 0.28 * (r_r - 2)))) * math.tanh(0.18 * re_p ** (1/2)))

        if re_p >= 10 and re_p <= 140 and r_r >=2 and r_r <= 12: # Osterle
            lift_coefficient_rotation = 0.45 + (r_r - 0.45) ** ((-0.05684) * (r_r**0.4)*( re_p ** 0.7))

        else: # Present Correlation eq 13
            lift_coefficient_rotation = r_r * (1 - 0.62 * math.tanh(0.3 * re_p ** (1/2)) - (0.24 * math.tanh(0.01*re_p) *  (math.cosh(0.8 * r_r ** (1/2)) / math.sinh(0.8 * r_r ** (1/2)) )* math.atan(0.47 * (r_r - 1)) ) )

        if re_p >=140:
            raise ReValueError(f"No accurate lift coefficient due to rotation correlation for Re = {re_p}; value exceeded 140.")
        
        lift_coefficient = lift_coefficient_shear_flow + lift_coefficient_rotation #Valid from 
        
        return lift_coefficient
    
    def calculate_lift_force(self, projectile):
        
        lift_coefficient = self.calculate_lift_coefficient(projectile)
    
        lift_force = (1/2) * math.pi * (projectile.radius ** 2) * self.air_density * mag2(projectile.vel) * norm(cross(projectile.vel, projectile.angular_velocity)) 

        return lift_force
            

    def calculate_drag_coefficient(self, projectile):
        reynolds_number = self.calculate_reynolds_number_p(projectile)
        dimensionless_rotation_rate = self.calculate_dimensionless_rotation_rate(projectile)

        
        if reynolds_number == 0 or dimensionless_rotation_rate == "Projectile Not Translating": #If object isnt moving, no lift. IF object isnt moving, Re = 0
            return "Use Stokes Drag"
        
        if reynolds_number < 0.1:
            return "Use Stokes Drag"
        
        #Calculating C_d, Drag Coefficient for Non-Spinning Sphere Using Michigan Tech's Correlation
        term1 = 24 / reynolds_number
        term2 = (2.6 * (reynolds_number / 5.0)) / (1 + (reynolds_number / 5.0) ** 1.52)
        term3 = (0.411 * (reynolds_number / 2.63e5) ** -7.94) / (1 + (reynolds_number / 2.63e5) ** -8.00)
        term4 = (0.25 * (reynolds_number / 1e6)) / (1 + (reynolds_number / 1e6))
        non_spinning_drag_coefficient = term1 + term2 + term3 + term4
        
        if projectile.angular_speed == 0:
            return non_spinning_drag_coefficient

        if reynolds_number > 3500:
            raise ReValueError(f"No accurate drag coefficient correlation for Re = {reynolds_number}; value exceeded 3,500.")
        
        if dimensionless_rotation_rate >= 25:
            raise RrValueError(f"No accurate drag coefficient correlation for Rr = {dimensionless_rotation_rate}; value exceeded 25.")

        if (reynolds_number > 0 and reynolds_number < 3500) and (dimensionless_rotation_rate > 0 and dimensionless_rotation_rate < 2.5):
            spinning_sphere_drag_coefficient = (0.989 + 0.482 * dimensionless_rotation_rate - 0.093 * (dimensionless_rotation_rate ** 2)) * non_spinning_drag_coefficient #EQ 17 from water paper
            return spinning_sphere_drag_coefficient

        if (reynolds_number > 0 and reynolds_number < 3500) and (dimensionless_rotation_rate >= 2.5 and dimensionless_rotation_rate < 25):
            spinning_sphere_drag_coefficient = 2.117 * (dimensionless_rotation_rate ** (-0.33)) * non_spinning_drag_coefficient #EQ 18 from water paper
            return spinning_sphere_drag_coefficient
        
        raise DragCoefficientUnknownError(f"Did not meet any of the conditions for calculating drag coefficient, check code")
        
    

    def calculate_drag_force(self, projectile):
        """
        Calculate the drag force on the ball.
        If the flow regime is Creeping Flow, use Stokes' law.
        Otherwise, use the drag coefficient-based formulas.
        :param ball: Ball object with properties radius, density, and velocity
        :return: Drag force as a vector
        """
        drag_coefficient = self.calculate_drag_coefficient(projectile)
    
        if drag_coefficient == "Use Stokes Drag" :
            Force = - 6 * math.pi * Environment.calculate_dynamic_viscosity_coefficient() * projectile.radius * mag(projectile.vel) * norm(projectile.vel)
            return Force
        
        else:
            # Force = 1/2 * fluid density * v * C_d * Cross-sectional Area * opposite to the direction of motion
            Force = 0.5 * self.air_density * mag(projectile.vel) * drag_coefficient * math.pi * (projectile.radius ** 2) * -norm(projectile.vel)
            return Force
        
        
        
    def calculate_drag_torque(self, projectile):
        reynolds_number = self.calculate_reynolds_number_p(projectile)
        lambda_aspect_ratio = 1 #projectile is a sphere

        if reynolds_number < 0.1:
            # Stokes' Torque : T_d = -8 * pi * dynamic_viscosity_coefficient * r^3 * angular_velocity             FROM Low Reynolds number hydrodynamics by John Happel, Adapted from Equation 7-8.21 , PAGE 351
            dynamic_viscosity_coefficient = self.calculate_dynamic_viscosity_coefficient() 
            torque = - 8 * math.pi * dynamic_viscosity_coefficient * projectile.radius**3 * projectile.angular_velocity
            return torque
        elif reynolds_number < 50:

            second_order_torque = lambda_aspect_ratio * self.air_density * ( mag2(projectile.vel) ) * (projectile.radius ** 3) * dot(norm(projectile.angular_velocity), norm(projectile.vel)) * cross(norm(projectile.angular_velocity), norm(projectile.vel))
            return second_order_torque
        
        else:
             raise ReValueError(f"No accurate inertial torque correlation for Re = {reynolds_number}; value exceeded 50.")
        
    
    def apply_net_force(self, projectile, force, dt):
        # Update momentum and velocity
        projectile.mom += force * dt
        projectile.vel = projectile.mom / projectile.mass
        projectile.pos += projectile.vel * dt

    def apply_net_torque(self, projectile, net_torque, dt):
        # Update angular momentum based on net torque and time interval
        projectile.angular_momentum += net_torque * dt
        # Update angular velocity based on the new angular momentum
        projectile.angular_velocity = projectile.angular_momentum / projectile.moment_of_inertia

