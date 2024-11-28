#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import random
from turtlesim.srv import Spawn, Kill
from functools import partial
from my_robot_interfaces.msg import SpawnedTurtleData
from my_robot_interfaces.msg import ArrayTurtle
from my_robot_interfaces.srv import TurtleServer


class SpawnTurtleNode(Node): 
    def __init__(self):
        super().__init__("spawn_turtle") 
        self.publish_turtle_data = self.create_publisher (ArrayTurtle, "turtle_alive",10)
        self.turtle_catch_server = self.create_service (TurtleServer, "catch_turtle",self.callback_catch_turtle)
        self.declare_parameter ("TimeInterval",2.0)
        self.time_interval = self.get_parameter("TimeInterval").value
        self.num = 2
        
        self.spawned_turtles = []
        self.spawn_timer = self.create_timer (self.time_interval, self.turtle_creator)
        
    def callback_catch_turtle (self, request, response):
        self.kill_turtle (request.name)
        response.success = True
        return response
    
    def publish_turtles(self):
        msg =ArrayTurtle()
        msg.turtles = self.spawned_turtles
        self.publish_turtle_data.publish(msg)
        
        
    def turtle_creator(self):
        x = round(random.uniform(1.0,9.0), 2)
        y = round(random.uniform(1.0,9.0), 2)
        theta = round(random.uniform(0.5325,1.5707), 4) 
        turtle_name = "Turtle"+ str(self.num)
        self.spawn_turtle(x, y, theta, turtle_name)
        self.num+=1
        
        
        
    def spawn_turtle(self, x, y, theta, name):
        # Prepare the request to spawn a new turtle
        spawn_client = self.create_client(Spawn, '/spawn') # Creating a client called "spawn_client" which connect to the server "/spawn"  
        spawn_client.wait_for_service()    # "spawn_client" waiting for the service
        spawn_request = Spawn.Request()
        spawn_request.x = x
        spawn_request.y = y
        spawn_request.theta = theta
        spawn_request.name = name
        
        future = spawn_client.call_async(spawn_request)
        future.add_done_callback(
            partial(self.callback_spawner, x=x, y=y, theta=theta, name=name))
        
    
        
    def callback_spawner(self, future, x, y, theta, name):
        
        try:
            response = future.result()
            if response.name != "":
                self.get_logger().info(str(response.name + " is now alive"))
                new_turtle = SpawnedTurtleData()
                new_turtle.name =response.name
                new_turtle.x = x
                new_turtle.y = y
                new_turtle.theta = theta
                self.spawned_turtles.append(new_turtle)
                self.publish_turtles()
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
            
            
    def kill_turtle(self, turtle_name):
        # Prepare the request to kill the specified turtle
        self.kill_client = self.create_client(Kill, '/kill')    # Creating a client called "kill_client" which connect to the server "/kill"
        while not self.kill_client.wait_for_service(1.0): # "kill_client" waiting for the service. 
            self.get_logger().warn("Waiting for Server!!!!")
        kill_request = Kill.Request()
        kill_request.name = turtle_name
        
        # Call the kill service and handle response
        future = self.kill_client.call_async(kill_request)
        future.add_done_callback(
            partial(self.callback_killer,turtle_name=turtle_name))
    
            
    def callback_killer(self, future,turtle_name):
        
        try:
            future.result()
            for (i, turtle) in enumerate (self.spawned_turtles):
                del self.spawned_turtles[i]
                self.publish_turtles()
                break
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))
            
    


def main(args=None):
    rclpy.init(args=args)
    node = SpawnTurtleNode() 
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()