from vpython import graph, gcurve, color
from Environment import Environment

environment = Environment()

class PlotManager:
    def __init__(self, time_flight, max_x, max_y, max_y_velocity, max_angular_velocity, max_reynolds, max_force, max_dimensionless_angular_velocity):
        
        # X and Y Position graphs
        self.graph_X_pos = graph(title='<b>X Position over Time</b>', xtitle='Time', ytitle='X position', xmin=0, xmax=time_flight, ymin=0, ymax=max_x)
        self.draw_X_pos = gcurve(color=color.cyan, graph=self.graph_X_pos, label='X Pos')

        self.graph_Y_pos = graph(title='<b>Y Position over Time</b>', xtitle='Time', ytitle='Y position', xmin=0, xmax=time_flight, ymin=0, ymax=max_y)
        self.draw_Y_pos = gcurve(color=color.cyan, graph=self.graph_Y_pos, label='Y Pos')

        # X and Y Velocity graphs
        self.graph_X_velocity = graph(title='<b>X Velocity over Time</b>', xtitle='Time', ytitle='X Velocity', xmin=0, xmax=time_flight, ymin=0, ymax=max_x)
        self.draw_X_velocity = gcurve(color=color.cyan, graph=self.graph_X_velocity, label='X Vel')

        self.graph_Y_velocity = graph(title='<b>Y Velocity over Time</b>', xtitle='Time', ytitle='Y Vel', xmin=0, xmax=time_flight, ymin=-max_y_velocity, ymax=0)
        self.draw_Y_velocity = gcurve(color=color.cyan, graph=self.graph_Y_velocity, label='Y Vel')

        # Angular Velocity graph
        self.graph_angular_velocity = graph(title='<b>Angular Velocity over Time</b>', xtitle='Time', ytitle='Angular Velocity', xmin=0, xmax=time_flight, ymin=-max_angular_velocity, ymax=max_angular_velocity)
        self.draw_angular_velocity = gcurve(color=color.magenta, graph=self.graph_angular_velocity, label='Angular Vel')

        # Reynolds Number graph
        self.graph_reynolds = graph(title='<b>Reynolds Number over Time</b>', xtitle='Time', ytitle='Reynolds Number', xmin=0, xmax=time_flight, ymin=0, ymax=max_reynolds)
        self.draw_reynolds = gcurve(color=color.magenta, graph=self.graph_reynolds, label='Reynolds Number')

        # Gravitational Force graph
        self.graph_gravitational_force = graph(title='<b>Gravitational Force over Time</b>', xtitle='Time', ytitle='Gravitational Force', xmin=0, xmax=time_flight, ymin=0, ymax=max_force)
        self.draw_gravitational_force = gcurve(color=color.red, graph=self.graph_gravitational_force, label='Gravitational Force')

        # Drag Force graph
        self.graph_drag_force = graph(title='<b>Drag Force over Time</b>', xtitle='Time', ytitle='Drag Force', xmin=0, xmax=time_flight, ymin=0, ymax=max_force)
        self.draw_drag_force = gcurve(color=color.green, graph=self.graph_drag_force, label='Drag Force')

        # Lift Force graph
        self.graph_lift_force = graph(title='<b>Lift Force over Time</b>', xtitle='Time', ytitle='Lift Force', xmin=0, xmax=time_flight, ymin=0, ymax=max_force)
        self.draw_lift_force = gcurve(color=color.blue, graph=self.graph_lift_force, label='Lift Force')

        # Dimensionless Angular Velocity graph
        self.graph_dimensionless_angular_velocity = graph(title='<b>Dimensionless Angular Velocity over Time</b>', xtitle='Time', ytitle='Dimensionless Angular Velocity (R_r)', xmin=0, xmax=time_flight, ymin=0, ymax=max_dimensionless_angular_velocity)
        self.draw_dimensionless_angular_velocity = gcurve(color=color.orange, graph=self.graph_dimensionless_angular_velocity, label='R_r')

        # Torque over time
        self.graph_torque = graph(title='<b>Torque over Time</b>', xtitle='Time', ytitle='Torque', xmin=0, xmax=time_flight, ymin=0, ymax=max_force * 10)
        self.draw_torque = gcurve(color=color.purple, graph=self.graph_torque, label='Torque')

        # Net Force over time
        self.graph_net_force = graph(title='<b>Net Force over Time</b>', xtitle='Time', ytitle='Net Force',xmin=0, xmax=time_flight, ymin=0, ymax=max_force * 1)
        self.draw_net_force = gcurve(color=color.blue, graph=self.graph_net_force, label='Net Force')

        # Magnitude of Velocity over time
        self.graph_velocity_magnitude = graph(title='<b>Velocity Magnitude over Time</b>', xtitle='Time', ytitle='|Velocity|',xmin=0, xmax=time_flight, ymin=0, ymax=max_y_velocity)
        self.draw_velocity_magnitude = gcurve(color=color.green, graph=self.graph_velocity_magnitude, label='|Velocity|')

        # Angular Speed over time
        self.graph_angular_speed = graph(title='<b>Angular Speed over Time</b>', xtitle='Time', ytitle='Angular Speed', xmin=0, xmax=time_flight, ymin=0, ymax=max_angular_velocity)
        self.draw_angular_speed = gcurve(color=color.orange, graph=self.graph_angular_speed, label='Angular Speed')
        

    def update(self, t, projectile):
        # Update position and velocity plots
        self.draw_X_pos.plot(pos=(t, projectile.pos.x))
        self.draw_Y_pos.plot(pos=(t, projectile.pos.y))
        self.draw_X_velocity.plot(pos=(t, projectile.vel.x))
        self.draw_Y_velocity.plot(pos=(t, projectile.vel.y))
        self.draw_angular_velocity.plot(pos=(t, projectile.angular_velocity.z))
        self.draw_reynolds.plot(pos=(t, environment.calculate_reynolds_number_p(projectile)))     
        self.draw_gravitational_force.plot(pos=(t, (environment.calculate_force_gravity(projectile)).mag))
        self.draw_drag_force.plot(pos=(t, (environment.calculate_drag_force(projectile).mag)))
        self.draw_lift_force.plot(pos=(t, (environment.calculate_lift_force(projectile)).mag))

        # Update dimensionless angular velocity (R_r)
        dimensionless_angular_velocity = environment.calculate_dimensionless_rotation_rate(projectile)
        self.draw_dimensionless_angular_velocity.plot(pos=(t, dimensionless_angular_velocity))

        # Update torque plot
        self.draw_torque.plot(pos=(t, (environment.calculate_torque(projectile)).mag))

        # Update net force plot
        self.draw_net_force.plot(pos=(t,((environment.calculate_force_gravity(projectile) + environment.calculate_drag_force(projectile) + environment.calculate_lift_force(projectile)).mag)))

        # Update velocity magnitude plot
        self.draw_velocity_magnitude.plot(pos=(t, (projectile.vel).mag))

        # Update angular speed plot
        self.draw_angular_speed.plot(pos=(t, (projectile.angular_velocity).mag))

    def update_xmax(self, new_time_flight):
        """Rescale the xmax of all graphs to the new time range."""
        self.graph_X_pos.xmax = new_time_flight
        self.graph_Y_pos.xmax = new_time_flight
        self.graph_X_velocity.xmax = new_time_flight
        self.graph_Y_velocity.xmax = new_time_flight
        self.graph_angular_velocity.xmax = new_time_flight
        self.graph_reynolds.xmax = new_time_flight
        self.graph_lift_force.xmax = new_time_flight
        self.graph_torque.xmax = new_time_flight
        self.graph_dimensionless_angular_velocity.xmax = new_time_flight
        self.graph_net_force.xmax = new_time_flight
        self.graph_drag_force.xmax = new_time_flight
        self.graph_gravitational_force.xmax = new_time_flight
        self.graph_velocity_magnitude.xmax = new_time_flight
        self.graph_angular_speed.xmax = new_time_flight


