from vpython import vector

class Ball:
    def __init__(self, mass, radius, initial_position, initial_velocity, initial_angular_speed, initial_rot_direction):
        self.mass = mass
        self.radius = radius
        self.pos = initial_position
        self.vel = initial_velocity
        self.mom = self.mass * self.vel
        self.angular_speed = initial_angular_speed
        self.moment_of_inertia = (2/5) * self.mass * self.radius ** 2  # Example for a solid spher
        self.reynolds_number_p = None
        self.reynolds_number_r = None
        self.correlation_accuracy = "Good"

         
        # Set rotational direction based on the string input
        if initial_rot_direction.lower() == "clockwise":
            self.rot_direction = vector(0, 0, -1)  # Clockwise direction (assuming -Z axis)
        elif initial_rot_direction.lower() == "counterclockwise":
            self.rot_direction = vector(0, 0, 1)  # Counterclockwise direction (assuming +Z axis)
        else:
            raise ValueError("Invalid rotational direction. Use 'clockwise' or 'counterclockwise'.")

        # Initialize angular velocity and momentum as a vector
        self.angular_velocity = self.angular_speed * self.rot_direction 
        self.angular_momentum = self.moment_of_inertia * self.angular_velocity
       