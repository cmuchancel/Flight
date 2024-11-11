from vpython import graph, gcurve, color
class PlotManager:
    def __init__(self, time_flight, max_x, max_y, max_y_velocity):
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

    def update(self, t, ball):
        self.draw_X_pos.plot(pos=(t, ball.pos.x))
        self.draw_Y_pos.plot(pos=(t, ball.pos.y))
        self.draw_X_velocity.plot(pos=(t, ball.vel.x))
        self.draw_Y_velocity.plot(pos=(t, ball.vel.y))


