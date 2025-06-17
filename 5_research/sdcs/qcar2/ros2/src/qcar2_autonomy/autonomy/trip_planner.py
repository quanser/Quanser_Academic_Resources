#! /usr/bin/env python3

import rclpy # Python client library for ROS 2
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,SetParametersResult
from rclpy.parameter import ParameterType
from std_msgs.msg import Bool

import time


class tripPlanner(Node):
    def __init__(self):
        super().__init__('trip_planner')

        # node names to set 
        self.path_follower_node = "path_follower"
        self.qcar_hardware_node= "qcar2_hardware"


        # start clients for node parameters
        self.path_follower_client = self.create_client(SetParameters, f'/{self.path_follower_node}/set_parameters')
        self.qcar_hardware_client = self.create_client(SetParameters, f'/{self.qcar_hardware_node}/set_parameters')
        
        #waiting for services to become availble...
        while not self.path_follower_client.wait_for_service(timeout_sec = 4.0):
            self.get_logger().info(f'waiting for {self.path_follower_node} parameter service!.....')
        
        self.get_logger().info(f'connected to  {self.path_follower_node} parameter service!.....')
        
        while not self.qcar_hardware_client.wait_for_service(timeout_sec = 4.0):
            self.get_logger().info(f'waiting for {self.qcar_hardware_node} parameter service!.....')
        
        self.get_logger().info(f'connected to  {self.qcar_hardware_node} parameter service!.....')

        self.parameter_change_retries = 5
        self.parameter_sleep_time = 2


        # define new parameters for taxi node to use 
        self.declare_parameter('taxi_node', [10])
        self.taxi_node = list(self.get_parameter("taxi_node").get_parameter_value().integer_array_value)[0]
        
        # define new parameters for node to use 
        self.declare_parameter('trip_nodes', [2,8])
        self.trip_nodes = list(self.get_parameter("trip_nodes").get_parameter_value().integer_array_value)



        # parameter callback for new rides/update to taxi node
        self.add_on_set_parameters_callback(self.parameter_update_callback) 


        '''
        State definition for trip planner logic
        trip super states 
        1 - going to taxi hub 
        2 - ready for rides


        trip actions
        0 - driving to taxi hub
        1 - driving to pickup
        2 - driving to stops (optional)  
        3 - driving to dropoff
        4 - driving to taxi hub        
        
        trip states
        1 - driving -> green led 
        2 - waiting -> colors led for specific time
        

        '''
        self.trip_super_state = 1.0 # qcar first drives to taxi hub
        self.current_trip_state = 1.0 # once at taxi hub, hold red for 3s
        self.path_nodes = []
        self.super_state_1_flags = [False, False]
        self.taxi_node = 10
        self.new_ride_requested = False
        self.trip_length = 0
        self.current_trip_status = False # True/False if trip complete/not complete
        self.current_stop = 0
        self.goal_stop = 0
        self.stop_index = 0
        self.nodes_sent = False

        # LED specific parameters 
        self.led_time = 3
        self.led_time_t0 = time.time()
        self.led_timer_reset = False
        self.path_status_subscrition = self.create_subscription(Bool, '/path_status',self.path_status_callback, 1)
        self.qcar_state = 4.0
        self.previous_led_state = 0.0
        self.current_path_status = False
        self.led_set_logic()

        self.dt = 1/10
        self.trip_time = time.time()
        self.timer1 = self.create_timer(self.dt, self.trip_planner_controller)

        
    def parameter_update_callback(self, params):
        for param in params:
            if param.name == 'taxi_node' and param.type_== param.Type.INTEGER_ARRAY:
                # Navigation specific variables
                self.taxi_node = list(param.value)
                if len(self.taxi_node > 1):
                    self.get_logger().info('Incorrect number of nodes given... setting default')
                    self.taxi_node = 10
                          
            elif param.name == 'trip_nodes' and param.type_== param.Type.INTEGER_ARRAY:
                if self.trip_super_state ==1:
                        self.get_logger().info('Cant assign trip, not at the taxi hub!')

                # The QCar2 has to reach the taxi hub before a new trip can be requested
                if self.current_trip_status == True and self.trip_super_state == 2: 
                    self.trip_nodes = list(param.value)
                    self.path_nodes = []
                    self.trip_length = len(self.trip_nodes)

                    if self.trip_length <2:
                        self.get_logger().info('Invalid trip scenario... minimum 2 point required for trip')
                    else:
                        for i in range(2+self.trip_length):
                            if i == 0 or i == len(self.trip_nodes)+1:
                                self.path_nodes.append(10)
                            else:
                                self.path_nodes.append(self.trip_nodes[i-1])

                        print("New trip requested!")
                        print(self.path_nodes)                        

                        self.new_ride_requested = True
                        self.stop_index = 0
                        self.trip_time = time.time()
                        
                        # We travel slowly to pickup station and speed up during actual rides
                        self.send_request(param_name="desired_speed",
                                    param_value= [1.0],
                                    param_type= ParameterType.PARAMETER_DOUBLE_ARRAY,
                                    client= self.path_follower_client)
                            

                # The QCar2 has to reach the taxi hub before a new trip can be requested
                if self.current_trip_status == False and self.trip_super_state == 2:
                    self.get_logger().info('Cant assign trip, current trip in progress!')

        return SetParametersResult(successful = True)

    def trip_planner_controller(self):
        # Note: initial condition for qcar2 as it travels from strating origin to taxi hub keeps LED green
        t_current = time.time() - self.trip_time
        # construct total path to know how many LED states the QCar will have 
        
        # At the start the QCar will need to generate a path from the starting origin to the taxihub
        # this path is different from every other path
        if self.trip_super_state == 1:
            # Generate path
            if t_current < 10 and len(self.path_nodes) == 0 and self.current_path_status == False:
                self.path_nodes.append(0)
                for node in self.trip_nodes:
                    self.path_nodes.append(node)
                self.path_nodes.append(self.taxi_node)
                
                if self.super_state_1_flags[0] == False:
                    self.super_state_1_flags[0] = self.send_request(param_name="node_values",
                              param_value= self.path_nodes,
                              param_type= ParameterType.PARAMETER_INTEGER_ARRAY,
                              client= self.path_follower_client)
                
                if self.super_state_1_flags[1] == False:
                    self.super_state_1_flags[1] = self.send_request(param_name="start_path",
                              param_value= [True],
                              param_type= ParameterType.PARAMETER_BOOL_ARRAY,
                              client= self.path_follower_client)

            # We have passed the first 10 seconds and are now waiting for new rides 
            if self.current_path_status == True and t_current > 10:

                # reset LED timer to ensure LEDs are only on for 3s
                if not self.led_timer_reset:
                    self.led_time_t0 = time.time()
                    self.led_timer_reset = True                    
                
                if time.time()-self.led_time_t0 < self.led_time:
                    # this will set the LED red for 3 seconds
                    self.qcar_state = 1
                elif time.time()-self.led_time_t0 > self.led_time: 
                    #ready for another ride
                    self.qcar_state = 4
                
                    # clear current nodes
                    self.path_nodes = []

                    # switch into full ride planning mode
                    self.trip_super_state = 2
                    
                    # ready for a new trip!
                    self.current_trip_status = True
                    self.led_timer_reset = False

        # QCar has reached the taxihub area and is ready for a new trip!
        if  self.trip_super_state == 2:
            self.qcar_state = 4
            if self.new_ride_requested:
                # breakdown ride into subsets of paths 
                if self.stop_index+1 <= len(self.path_nodes)-1:
                    if self.nodes_sent == False:
                        
                        # extract current trip values
                        self.current_stop = self.path_nodes[self.stop_index]
                        self.goal_stop = self.path_nodes[self.stop_index+1]
                        
                        trip = [self.current_stop,self.goal_stop]

                        # send nodes to path follower
                        if not self.nodes_sent: 
                            self.nodes_sent = self.send_request(param_name="node_values",
                                param_value= trip,
                                param_type= ParameterType.PARAMETER_INTEGER_ARRAY,
                                client= self.path_follower_client)
                        
                        
                    
                    if self.current_path_status == True and t_current > 2:
                        if not self.led_timer_reset: 
                            self.led_time_t0 = time.time()
                            self.led_timer_reset = True

                        if time.time() - self.led_time_t0 < self.led_time:
                            
                            if len(self.path_nodes) > 4:
                                # First stop is the pickup
                                if self.stop_index+1 == 1:
                                    self.qcar_state = 2

                                # This is for intermediate stops or back at taxi hub
                                if (self.stop_index+1 > 1 or self.stop_index+1 == len(self.path_nodes)-1 and 
                                    self.stop_index+1 !=  len(self.path_nodes)-2):
                                    
                                    self.qcar_state = 1

                                # This is for drop off stop 
                                if self.stop_index+1 ==  len(self.path_nodes)-2:
                                    self.qcar_state = 3
                            elif len(self.path_nodes) == 4:
                                #becomes ambigious to decern stops, manually define the sequence
                                if self.stop_index+1 == 1:
                                    self.qcar_state = 2
                                elif self.stop_index+1 == 2:
                                    self.qcar_state = 3
                                elif self.stop_index+1 == 3:
                                    self.qcar_state = 1
                            

                        elif time.time()-self.led_time_t0 > self.led_time: 

                            #reset triggers used for timing lights
                            self.led_timer_reset = False
                            self.nodes_sent = False
                            self.qcar_state = 4
                            self.stop_index +=1
                            self.trip_time = time.time()
        
        if self.previous_led_state != self.qcar_state:
            self.previous_led_state = self.qcar_state
            self.led_set_logic()

    def led_set_logic(self):

        # This section is trying to emulate the cli call -> ros2 param set qcar2_hardware led_color_id <value>
        # LED Red (used for taxi hub stop and inbetween ride stops)

        if self.qcar_state == 1.0:
            self.send_request(param_name="led_color_id",
                              param_value= 0,
                              param_type= ParameterType.PARAMETER_INTEGER,
                              client= self.qcar_hardware_client)
        
        # Arrived at pickup
        elif self.qcar_state == 2.0:
            self.send_request(param_name="led_color_id",
                              param_value= 2,
                              param_type= ParameterType.PARAMETER_INTEGER,
                              client= self.qcar_hardware_client)
        
        # Drop off coordinate
        elif self.qcar_state == 3.0:
            self.send_request(param_name="led_color_id",
                              param_value= 3,
                              param_type= ParameterType.PARAMETER_INTEGER,
                              client= self.qcar_hardware_client)
        # Driving state
        elif self.qcar_state == 4.0:
            self.send_request(param_name="led_color_id",
                              param_value= 1,
                              param_type= ParameterType.PARAMETER_INTEGER,
                              client= self.qcar_hardware_client)

    def path_status_callback(self,msg):
        self.current_path_status  = msg.data

    # method used to end multiple parameters to multiple nodes
    def send_request(self, param_name, param_value, param_type,client):
            

        param = Parameter()
        param.name = param_name
        param.value.type = param_type

        if param_type == ParameterType.PARAMETER_INTEGER_ARRAY:
            param.value.integer_array_value = param_value

        elif param_type == ParameterType.PARAMETER_INTEGER:
            param.value.integer_value = param_value

        elif param_type == ParameterType.PARAMETER_BOOL_ARRAY:
            param.value.bool_array_value = param_value
        
        elif param_type == ParameterType.PARAMETER_DOUBLE_ARRAY:
            param.value.double_array_value = param_value


        request = SetParameters.Request()
        request.parameters = [param]
        future = client.call_async(request)

 
        

def main():
 
  # Start the ROS 2 Python Client Library
  rclpy.init()

  node = tripPlanner()
  try:
      rclpy.spin(node)
  except KeyboardInterrupt:
      pass

  rclpy.shutdown()
  
if __name__ == '__main__':
  main()