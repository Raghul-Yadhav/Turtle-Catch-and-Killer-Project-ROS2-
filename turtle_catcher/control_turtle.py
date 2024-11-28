#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from my_robot_interfaces.msg import ArrayTurtle
from my_robot_interfaces.srv import TurtleServer
from functools import partial



class ControlTurtleNode(Node): 
    def __init__(self):
        super().__init__("control_turtle")
        
        self.target_turtle = None
        
        self.current_pose = None
        self.declare_parameter("Closest_turtle_first", True)
        
        self.catch_closest_turtle = self.get_parameter("Closest_turtle_first").value
        
        self.subcriber_data = self.create_subscription(ArrayTurtle,"turtle_alive",self.tutrles_alive,10)

        self.target_data_subscription = self.create_subscription (Pose, "/turtle1/pose",self.pose_callback, 10) # Subcribers to the topic "/turtle1/pose" to get the current pose of the turtle_1
        
        self.publish_movement_data = self.create_publisher (Twist, "/turtle1/cmd_vel", 10) # Publishes how much the turtle should move linearly and angularly in topic "/turtle1/cmd_vel"
        
        self.loop_timer = self.create_timer (0.01,self.control_loop) # Timer which call the control loop function to check the current pose , remaining distance and angular differance and publishes the data to turtle1
        
    def tutrles_alive(self,msg):
        if len(msg.turtles)>0:
            if self.catch_closest_turtle:
                closest_turtle = None
                closest_turtle_dist = None
                for turtle in msg.turtles:
                    real_x = turtle.x - self.current_pose.x
                    real_y = turtle.y - self.current_pose.y
                    dist = math.sqrt(real_x**2 + real_y**2)
                    if closest_turtle == None or dist < closest_turtle_dist:
                        closest_turtle = turtle
                        closest_turtle_dist = dist
                
                self.target_turtle = closest_turtle
                
            else:
                self.target_turtle = msg.turtles[0]
        
    def pose_callback (self, msg): # Function gets the current pose of the turtle1
            self.current_pose = msg
        
    def control_loop (self): # Calculates the difference in angle and distance and control the turtle1
            
            if  self.current_pose == None or self.target_turtle == None:
                return
            
            
            real_x = self.target_turtle.x - self.current_pose.x
            real_y = self.target_turtle.y - self.current_pose.y
            Distance = math.sqrt(real_x**2 + real_y**2)
            
            msg = Twist()
            
            
            if Distance > 0.1 :
                msg.linear.x =  1.5*Distance
                
                Goal_angle = math.atan2(real_y,real_x)
                Diff_angle = Goal_angle - self.current_pose.theta
                if Diff_angle > math.pi:
                    Diff_angle -= 2 * math.pi
                elif Diff_angle < -math.pi:
                    Diff_angle += 2 * math.pi
                    
                msg.angular.z = 5.7*Diff_angle
                
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                self.Catch_turtle_server(self.target_turtle.name)
                self.target_turtle = None
                
            
            self.publish_movement_data.publish (msg)
            
            
    def Catch_turtle_server(self, turtle_name):
        
        self.kill_client = self.create_client(TurtleServer, 'catch_turtle')   
        while not self.kill_client.wait_for_service(1.0): 
            self.get_logger().warn("Waiting for Server!!!!")
        request = TurtleServer.Request()
        request.name = turtle_name
        
        # Call the kill service and handle response
        future = self.kill_client.call_async(request)
        future.add_done_callback(
            partial(self.callback_catch_turtle,turtle_name=turtle_name))
    
            
    def callback_catch_turtle(self, future,turtle_name):
        
        try:
            response = future.result()
            if not response.success:
                self.get_logger().error (str(turtle_name) + "can't be killed ")
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
            
            
            
def main(args=None):
    rclpy.init(args=args)
    node = ControlTurtleNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()                                                     