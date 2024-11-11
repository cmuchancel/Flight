from vpython import vector

class Ball:
    def __init__(self, mass, radius, initial_position, initial_velocity, initial_rot_velocity=0):
        self.mass = mass
        self.radius = radius
        self.pos = initial_position
        self.vel = initial_velocity
        self.rot_vel = initial_rot_velocity
        self.mom = self.mass * self.vel

    def apply_net_force(self, force, dt):
        # Update momentum and velocity
        self.mom += force * dt
        self.vel = self.mom / self.mass
        self.pos += self.vel * dt
