from quanser.devices import GameController
import numpy as np

class gamepadViaTarget():
    """This method opens a GameController device and opens a connection to it. This is set up for the Logitech Gamepad F710. \n
    Use the read() method to update joystick states and terminate() method to close the connection. """
    def __init__(self, controller_number):
        self.joystick = GameController()
        self.joystick.open(controller_number)

        self.LLA = 0
        self.LLO = 0
        self.LT = 0
        self.RLA = 0
        self.RLO = 0
        self.RT = 0
        self.flag_z = False
        self.flag_rz = False
        self.A = 0
        self.B = 0
        self.X = 0
        self.Y = 0
        self.LB = 0
        self.RB = 0
        self.up = 0
        self.right = 0
        self.left = 0
        self.down = 0
        # self.buttons = np.zeros((32,1), dtype=np.bool)

    def read(self):
        """This method polls to read current gamepad state. The updated states are: \n
         \n
        Continuous: \n
            LLA - Left Lateral stick \n
            LLO - Left Longitudonal stick \n
            RLA - Right Lateral stick \n
            RLO - Right Longitudonal stick \n
            LT - Left Trigger \n
            RT - Right Trigger \n
         \n
        Buttons/Arrows: \n
            A, B, X, Y, LB, LR \n
            up, right, down, left \n
        """
        data, new = self.joystick.poll() 
        self.LLA = -1*data.x
        self.LLO = -1*data.y 
        if data.z == 0 and not self.flag_z:
            self.LT = 0
        else:
            self.LT = 0.5 + 0.5*data.z
            self.flag_z = True 

        self.RLA = -1*data.rx 
        self.RLO = -1*data.ry 

        if data.rz == 0 and not self.flag_rz:
            self.RT = 0
        else:
            self.RT = 0.5 + 0.5*data.rz
            self.flag_rz = True 

        self.A = int(data.buttons & (1 << 0))
        self.B = int((data.buttons & (1 << 1))/2)
        self.X = int((data.buttons & (1 << 2))/4)
        self.Y = int((data.buttons & (1 << 3))/8)
        self.LB = int((data.buttons & (1 << 4))/16)
        self.RB = int((data.buttons & (1 << 5))/32)
        val = 180*data.point_of_views[0]/np.pi
        self.up = 0
        self.right = 0
        self.left = 0
        self.down = 0
        if val >= 310 or (val >= 0 and val < 50):
            self.up = 1
        if val >= 40 and val < 140:
            self.right = 1
        if val >= 130 and val < 230:
            self.down = 1
        if val >= 220 and val < 320:
            self.left = 1
        
        return new

    def terminate(self):
        """This method terminates the joystick correctly. """
        self.joystick.close()
