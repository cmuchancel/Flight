from vpython import graph, gcurve, color
from Environment import Environment

environment = Environment()

class PlotManager:
    def __init__(self, time_flight, max_x, max_y, max_y_velocity, max_angular_velocity, max_reynolds):

        
        # X and Y Position graphs
        self.graph_X_pos = graph(title='<b>X Position over Time</b>', xtitle='Time', ytitle='X position',
                                 xmin=0, xmax=time_flight, ymin=0, ymax=max_x)
        self.draw_X_pos = gcurve(color=color.cyan, graph=self.graph_X_pos, label='X Pos')

        self.graph_Y_pos = graph(title='<b>Y Position over Time</b>', xtitle='Time', ytitle='Y position',
                                 xmin=0, xmax=time_flight, ymin=0, ymax=max_y)
        self.draw_Y_pos = gcurve(color=color.cyan, graph=self.graph_Y_pos, label='Y Pos')

        # X and Y Velocity graphs
        self.graph_X_velocity = graph(title='<b>X Velocity over Time</b>', xtitle='Time', ytitle='X Velocity',
                                      xmin=0, xmax=time_flight, ymin=0, ymax=max_x)
        self.draw_X_velocity = gcurve(color=color.cyan, graph=self.graph_X_velocity, label='X Vel')

        self.graph_Y_velocity = graph(title='<b>Y Velocity over Time</b>', xtitle='Time', ytitle='Y Vel',
                                      xmin=0, xmax=time_flight, ymin=-max_y_velocity, ymax=0)
        self.draw_Y_velocity = gcurve(color=color.cyan, graph=self.graph_Y_velocity, label='Y Vel')

        # Angular Velocity graph
        self.graph_angular_velocity = graph(title='<b>Angular Velocity over Time</b>', xtitle='Time', ytitle='Angular Velocity',
                                            xmin=0, xmax=time_flight, ymin=-max_angular_velocity, ymax=max_angular_velocity)
        self.draw_angular_velocity = gcurve(color=color.magenta, graph=self.graph_angular_velocity, label='Angular Vel')

        # Reynolds Number graph
        self.graph_reynolds = graph(title='<b>Reynolds Number over Time</b>', xtitle='Time', ytitle='Reynolds Number',
                                            xmin=0, xmax=time_flight, ymin=0, ymax=10000)
        self.draw_reynolds = gcurve(color=color.magenta, graph=self.graph_reynolds, label='Reynolds Number')



    def update(self, t, projectile):
         # Update position and velocity plots
        self.draw_X_pos.plot(pos=(t, projectile.pos.x))
        self.draw_Y_pos.plot(pos=(t, projectile.pos.y))
        self.draw_X_velocity.plot(pos=(t, projectile.vel.x))
        self.draw_Y_velocity.plot(pos=(t, projectile.vel.y))
        self.draw_angular_velocity.plot(pos=(t, projectile.angular_velocity.z))
        self.draw_reynolds.plot(pos=(t, environment.calculate_reynolds_number(projectile)))
      
       



