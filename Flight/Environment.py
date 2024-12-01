from vpython import *
from Ball import Ball  # Import Ball class
import math  # Import math module
from Exceptions import ReValueError, RrValueError, DragCoefficientUnknownError
import warnings  # Import the warnings module

# Ensure warnings are displayed only once
warnings.simplefilter("once", UserWarning)


class Environment:
    # Constants
    G = 6.67e-11
    earth_mass = 5.792e24
    earth_radius = 6.371e6 
    gas_constant_air = 287.05  # Specific gas constant for air (J/(kg·K))
    sutherland_constant = 110.4  # Sutherland constant for air (K)
    reference_temperature = 288.15  # Reference temperature at sea level (K)
    reference_viscosity = 1.7894e-5  # Reference dynamic viscosity at sea level (Pa·s)


    def __init__(self):
        self.torque_warning_displayed = False  # Flag to track if warning has been displayed
        self.used_correlations = []

    def calculate_temperature_and_pressure_at_altitude(self, altitude):
        # Calculates temperature and pressure at the given altitude (meters).
        if altitude <= 11000:  # Troposphere
            temperature = self.reference_temperature - 0.0065 * altitude
            pressure = 101325 * (temperature / self.reference_temperature) ** (9.80665 / (0.0065 * self.gas_constant_air))
        elif altitude <= 20000:  # Lower Stratosphere
            temperature = 216.65
            pressure = 22632.06 * math.exp(-9.80665 * (altitude - 11000) / (self.gas_constant_air * temperature))
        else:
            raise ValueError("Altitude exceeds the supported range of the standard atmosphere model.")
        return temperature, pressure

    def calculate_air_density(self, altitude):
        # Computes air density using altitude (meters).
        temperature, pressure = self.calculate_temperature_and_pressure_at_altitude(altitude)
        return pressure / (self.gas_constant_air * temperature)

    def calculate_dynamic_viscosity(self, altitude):
        # Computes dynamic viscosity using Sutherland's formula.
        temperature, _ = self.calculate_temperature_and_pressure_at_altitude(altitude)
        return self.reference_viscosity * (temperature / self.reference_temperature) ** 1.5 * (self.reference_temperature + self.sutherland_constant) / (temperature + self.sutherland_constant)      
      
    def calculate_force_gravity(self, projectile):
        height = projectile.pos.y
        return ((self.G * self.earth_mass * projectile.mass) / (self.earth_radius + height) ** 2) * vector(0, -1, 0)
    
    def calculate_torque_gravity(self, projectile):
        # Gravity acts at the center of mass, so torque due to gravity is zero
        gravity_force = self.calculate_force_gravity(projectile)
        lever_arm = vector(0, 0, 0)  # Acts on Center of mass, so lever arm is zero
        return lever_arm.cross(gravity_force)  # Should return vector(0, 0, 0)
    
    def calculate_buoyant_force(self, projectile):
        # Volume of the spherical particle
        volume = (4 / 3) * pi * (projectile.radius ** 3)
        acceleration_gravity = self.calculate_force_gravity(projectile) / projectile.mass
        # Buoyant force using Archimedes' principle
        buoyant_force = self.calculate_air_density(projectile.pos.y) * (4/3)  * volume * acceleration_gravity
        return buoyant_force  # Acts opposing gravity
    
    def calculate_reynolds_number_p(self, projectile):  #Works for Spheres, in form from Cambridge Paper
        
        # Calculate the dynamic viscosity using the air temperature
        altitude = projectile.pos.y
        mu_dynamic_viscosity_coefficient = self.calculate_dynamic_viscosity(altitude)
        
        # Calculate freestream velocity
        freestream_velocity = mag(projectile.vel)
        
        # Use diameter as the reference length for a sphere
        reference_length = 2 * projectile.radius  

        gamma_kinematic_viscosity = mu_dynamic_viscosity_coefficient / self.calculate_air_density(altitude)
        
        # Reynolds number formula: Re = (rho * V * L) / mu
        reynolds_number_p = (reference_length * freestream_velocity) / gamma_kinematic_viscosity
        projectile.reynolds_number = reynolds_number_p
        return reynolds_number_p
    
    def calculate_dimensionless_rotation_rate(self, projectile):
        # Calculate the dynamic viscosity using the air temperature
        altitude = projectile.pos.y
        mu_dynamic_viscosity_coefficient = self.calculate_dynamic_viscosity(altitude)
       
        # Use diameter as the reference length for a sphere
        reference_length = 2 * projectile.radius  

        gamma_kinematic_viscosity = mu_dynamic_viscosity_coefficient / self.calculate_air_density(projectile.pos.y)

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
        #   lift_coefficient = lift_coefficient_shear_flow + lift_coefficient_rotation 

        #CALCULATE COEFFICIENT OF LIFT DUE TO ROTATION:
        if r_r == 0:
            if "No rotation, no lift" not in self.used_correlations:
                self.used_correlations.append("No rotation, no lift")
            return 0

        if re_p >= 200:
            raise ReValueError(f"No accurate lift coefficient due to rotation correlation for Re = {re_p}; value exceeded 200. At Re > 200, Burification starts to take effect")
        
        if re_p == 0 or r_r == "No freestream velocity": # Chance "If it's not moving then there's no lift"

            if "No freestream velocity, no lift" not in self.used_correlations:
                self.used_correlations.append("No freestream velocity, no lift")

            return 0
        
        if re_p <= 0.1: # Loth eq 12

            if "Loth" not in self.used_correlations:
                self.used_correlations.append("Loth")

            lift_coefficient_rotation= r_r * (1 - ( 0.675 +  0.15 * (1 + math.tanh( 0.28 * (r_r - 2)))) * math.tanh(0.18 * re_p ** (1/2)))
            return lift_coefficient_rotation +   lift_coefficient_shear_flow
        
        if re_p >= 10 and re_p <= 140 and r_r >=2 and r_r <= 12: # Osterle

            if "Osterle" not in self.used_correlations:
                self.used_correlations.append("Osterle")

            lift_coefficient_rotation = 0.45 + (r_r - 0.45) ** ((-0.05684) * (r_r**0.4)*( re_p ** 0.7))
            return lift_coefficient_rotation +  lift_coefficient_shear_flow
        
        # Present Correlation eq 13


        if "Present Lift Correlation" not in self.used_correlations:
            self.used_correlations.append("Present Lift Correlation")

        lift_coefficient_rotation = r_r * (1 - 0.62 * math.tanh(0.3 * re_p ** (1/2)) - (0.24 * math.tanh(0.01*re_p) *  (math.cosh(0.8 * r_r ** (1/2)) / math.sinh(0.8 * r_r ** (1/2)) )* math.atan(0.47 * (r_r - 1)) ) )

        return lift_coefficient_rotation +  lift_coefficient_shear_flow
 
        
    
    def calculate_lift_force(self, projectile):
        
        lift_coefficient = self.calculate_lift_coefficient(projectile)

        altitude = projectile.pos.y
    
        lift_force = (1/2) * lift_coefficient * math.pi * (projectile.radius ** 2) * self.calculate_air_density(altitude) * mag2(projectile.vel) * norm(cross(-projectile.vel, projectile.angular_velocity)) 

        return lift_force
            

    def calculate_drag_coefficient(self, projectile):
        reynolds_number = self.calculate_reynolds_number_p(projectile)
        dimensionless_rotation_rate = self.calculate_dimensionless_rotation_rate(projectile)

        
        if reynolds_number == 0 or dimensionless_rotation_rate == "Projectile Not Translating": #If object isnt moving, no lift. IF object isnt moving, Re = 0
            return 0
        
        if reynolds_number < 2:

            if "24/RE Drag" not in self.used_correlations:
                self.used_correlations.append("24/RE Drag")

            return 24/reynolds_number
            
        
        #Calculating C_d, Drag Coefficient for Non-Spinning Sphere Using Michigan Tech's Correlation

        if "Michigan Tech Drag" not in self.used_correlations:
            self.used_correlations.append("Michigan Tech Drag")

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
            
            if "Drag #17" not in self.used_correlations:
                self.used_correlations.append("Drag #17")

            spinning_sphere_drag_coefficient = (0.989 + 0.482 * dimensionless_rotation_rate - 0.093 * (dimensionless_rotation_rate ** 2)) * non_spinning_drag_coefficient #EQ 17 from water paper
            return spinning_sphere_drag_coefficient

        if (reynolds_number > 0 and reynolds_number < 3500) and (dimensionless_rotation_rate >= 2.5 and dimensionless_rotation_rate < 25):
            
            if "Drag #18" not in self.used_correlations:
                self.used_correlations.append("Drag #18")

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

        altitude = projectile.pos.y
         # Force = 1/2 * fluid density * v * C_d * Cross-sectional Area * opposite to the direction of motion
        Force = 0.5 * self.calculate_air_density(altitude) * mag(projectile.vel) * drag_coefficient * math.pi * (projectile.radius ** 2) * -norm(projectile.vel)
        return Force
        
        
        
    def calculate_torque(self, projectile):
        reynolds_number = self.calculate_reynolds_number_p(projectile)
        lambda_aspect_ratio = 1  # Projectile is a sphere
        dimensionless_rotation_rate = self.calculate_dimensionless_rotation_rate(projectile)

        if reynolds_number > 50 and dimensionless_rotation_rate > 0.1:
            raise ReValueError(f"Torque calculation error: Re = {reynolds_number}, R_r = {dimensionless_rotation_rate}; No accurate Torque Calculation for Re > 50 and the Rotation is not negligible, therefore, cannot be ignored.")

        if reynolds_number > 50 and dimensionless_rotation_rate < 0.1:
            if not self.torque_warning_displayed:  # Check if the warning has been displayed before
                warnings.warn(
                    f"Torque calculation accuracy is questionable for Re = {reynolds_number} "
                    f"and R_r = {dimensionless_rotation_rate}. However, torque is negligible due to low R_r.",
                    UserWarning
                )
                self.torque_warning_displayed = True
        
        if "Torque Correlation" not in self.used_correlations:
                self.used_correlations.append("Torque Correlation") 

        altitude = projectile.pos.y
        second_order_torque = lambda_aspect_ratio * self.calculate_air_density(altitude) * ( mag2(projectile.vel) ) * (projectile.radius ** 3) * dot(norm(projectile.angular_velocity), norm(projectile.vel)) * cross(norm(projectile.angular_velocity), norm(projectile.vel))
        
        return second_order_torque
    
        
    
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

