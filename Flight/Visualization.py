from vpython import canvas, box, sphere, vector, color

class Visualization:
    def __init__(self, ball_radius, drop_height):
        # Set up the scene
        self.scene = canvas(title='Dropping a ball', caption='Hopefully this works',
                            center=vector(0, drop_height // 2, 0), background=color.white)
        
        # Create walls and floor
        self.left_wall = box(pos=vector(-2 * ball_radius, drop_height // 2, 0),
                             size=vector(1, 9, 5), color=color.red)
        self.floor = box(pos=vector(9, 0, 0), size=vector(21, 1, 5), color=color.green)

        # Create the ball visualization
        self.ball_visual = sphere(pos=vector(0, drop_height, 0), radius=ball_radius, color=color.orange)

    def update_ball_position(self, position):
        # Update the position of the ball in the visualization
        self.ball_visual.pos = position
