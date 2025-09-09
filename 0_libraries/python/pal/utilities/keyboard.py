import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time
import numpy as np
import subprocess
from pal.utilities.stream import BasicStream
from quanser.devices import Keyboard, KeyState, VirtualKeyCodes

class PygameKeyboard():
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 100))
        pygame.display.set_caption("Keyboard Window")
        clock = pygame.time.Clock()
        self.k_space = False
        self.k_esc   = False
        self.k_up    = False
        self.k_down  = False
        self.k_left  = False
        self.k_right = False
        self.k_w     = False
        self.k_a     = False
        self.k_s     = False
        self.k_d     = False
        self.k_q     = False
        self.k_i     = False
        self.k_j     = False
        self.k_k     = False
        self.k_l     = False
        self.k_u     = False
        self.k_o     = False

    def read(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()

        self.k_space = keys[pygame.K_SPACE]
        self.k_esc   = keys[pygame.K_ESCAPE]
        self.k_up    = keys[pygame.K_UP]
        self.k_down  = keys[pygame.K_DOWN]
        self.k_left  = keys[pygame.K_LEFT]
        self.k_right = keys[pygame.K_RIGHT]
        self.k_w     = keys[pygame.K_w]
        self.k_a     = keys[pygame.K_a]
        self.k_s     = keys[pygame.K_s]
        self.k_d     = keys[pygame.K_d]
        self.k_q     = keys[pygame.K_q]
        self.k_i     = keys[pygame.K_i]
        self.k_j     = keys[pygame.K_j]
        self.k_k     = keys[pygame.K_k]
        self.k_l     = keys[pygame.K_l]
        self.k_u     = keys[pygame.K_u]
        self.k_o     = keys[pygame.K_o]

    def terminate(self):
        """Terminate pygame"""
        pygame.quit()

class PygameKeyboardDrive():
    def __init__(self,maxThrottle=0.2,maxSteer=0.1):
        self.deceleration = 0.1
        self.aceleration = 0.2
        self.key_throttle = 0
        self.key_steer = 0
        self.max_throttle = maxThrottle
        self.max_steer = maxSteer

    def update(self,keyb):
        if keyb.k_w or keyb.k_s:
            sign=int(keyb.k_w)-int(keyb.k_s)
        else:
            sign = np.sign(self.key_throttle)
        self.key_throttle += (int(keyb.k_w)-int(keyb.k_s))*0.2 - self.deceleration*sign
        self.key_throttle = np.clip(self.key_throttle,-self.max_throttle,self.max_throttle)

        if keyb.k_a or keyb.k_d:
            sign=int(keyb.k_a)-int(keyb.k_d)
        else:
            sign = np.sign(self.key_steer)
        self.key_steer += (int(keyb.k_a)-int(keyb.k_d))*0.2 - self.deceleration*sign
        self.key_steer = np.clip(self.key_steer,-self.max_steer,self.max_steer)
        return self.key_steer,self.key_throttle
    
class KeyboardDrive():
    def __init__(self,mode=0,maxThrottle=0.2,maxSteer=0.1):
        self.deceleration = 0.1
        self.aceleration = 0.2
        self.key_throttle = 0
        self.key_steer = 0
        self.max_throttle = maxThrottle
        self.max_steer = maxSteer
        self.mode = mode

    def update(self,kb):
        
        if self.mode == 0:
            forward = kb.states[kb.K_W]
            backword = kb.states[kb.K_S]
            left = kb.states[kb.K_A]
            right = kb.states[kb.K_D]
        elif self.mode == 1:
            forward = kb.states[kb.K_UP]
            backword = kb.states[kb.K_DOWN]
            left = kb.states[kb.K_LEFT]
            right = kb.states[kb.K_RIGHT]
        
        if forward or backword:
            sign=int(forward)-int(backword)
        else:
            sign = np.sign(self.key_throttle)
        self.key_throttle += (int(forward)-int(backword))*0.2 - self.deceleration*sign
        self.key_throttle = np.clip(self.key_throttle,-self.max_throttle,self.max_throttle)

        if left or right:
            sign=int(left)-int(right)
        else:
            sign = np.sign(self.key_steer)
        self.key_steer += (int(left)-int(right))*0.2 - self.deceleration*sign
        self.key_steer = np.clip(self.key_steer,-self.max_steer,self.max_steer)
        return self.key_steer,self.key_throttle

class KeyBoardDriver():
    '''This class supports real-time key press polls for 30 specific keys. The
    keys included are function keys (Space, Home and Esc), True Arrow keys (
    Up, Down, Right, Left), False Arrow keys (W, S, D, A), Numpad keys (1 to 9)
    , Number Keys (1 to 0).'''

    def __init__(self, rate=30):
        '''Valid options for keyboard rate = 10, 30, 100 & 500 Hz.'''

        self.rate = rate
        # Pick a driver file based on rate requested.
        if self.rate==10:
            fileName = 'keyboardDriver10.rt-win64'
        elif self.rate==30:
            fileName = 'keyboardDriver30.rt-win64'
        elif self.rate==100:
            fileName = 'keyboardDriver100.rt-win64'
        elif self.rate==500:
            fileName = 'keyboardDriver500.rt-win64'
        else:
            print('Rate provided not a valid option.')
            return
        # Full path to keyboardDriver.rt-win64
        self.keyboardDriver = os.path.join(os.getenv('QAL_DIR'),
                                      '0_libraries',
                                      'resources',
                                      'applications',
                                      'KeyboardDriver',
                                      fileName)

        # Close existing instance of quanser host peripheral client and launch new one
        subprocess.Popen(['quanser_host_peripheral_client.exe', '-q'])
        time.sleep(0.5)
        subprocess.Popen(['quanser_host_peripheral_client.exe',
                          '-uri', 'tcpip://localhost:18798'])
        time.sleep(0.5)

        # Close existing instance of the keyboardDriver and launch new one
        os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-win64')
        time.sleep(0.5)
        os.system('quarc_run -D -r -t tcpip://localhost:17000 ' + self.keyboardDriver)

        # Start the BasicStream session to the keyboard driver
        # (must be a non-blocking client)
        self.keyboardArray = np.zeros((1,37), dtype=bool)
        self.client = BasicStream('tcpip://localhost:18799', 'C',
                                  receiveBuffer=self.keyboardArray,
                                  nonBlocking=True)
        self.connected = self.client.connected

        # Initialize all 30 keys
        self.assign()

        return

    def assign(self):
        '''This method updates keys from the receive buffer.'''
        # On first call, these are False.
        self.k_space = self.client.receiveBuffer[0][0]
        self.k_home  = self.client.receiveBuffer[0][1]
        self.k_esc   = self.client.receiveBuffer[0][2]
        self.k_up    = self.client.receiveBuffer[0][3]
        self.k_down  = self.client.receiveBuffer[0][4]
        self.k_right = self.client.receiveBuffer[0][5]
        self.k_left  = self.client.receiveBuffer[0][6]
        self.k_w     = self.client.receiveBuffer[0][7]
        self.k_s     = self.client.receiveBuffer[0][8]
        self.k_d     = self.client.receiveBuffer[0][9]
        self.k_a     = self.client.receiveBuffer[0][10]
        self.k_x     = self.client.receiveBuffer[0][11]
        self.k_y     = self.client.receiveBuffer[0][12]
        self.k_z     = self.client.receiveBuffer[0][13]
        self.k_g     = self.client.receiveBuffer[0][14]
        self.k_f     = self.client.receiveBuffer[0][15]
        self.k_r     = self.client.receiveBuffer[0][16]
        self.k_t     = self.client.receiveBuffer[0][17]
        self.k_np1   = self.client.receiveBuffer[0][18]
        self.k_np2   = self.client.receiveBuffer[0][19]
        self.k_np3   = self.client.receiveBuffer[0][20]
        self.k_np4   = self.client.receiveBuffer[0][21]
        self.k_np5   = self.client.receiveBuffer[0][22]
        self.k_np6   = self.client.receiveBuffer[0][23]
        self.k_np7   = self.client.receiveBuffer[0][24]
        self.k_np8   = self.client.receiveBuffer[0][25]
        self.k_np9   = self.client.receiveBuffer[0][26]
        self.k_1     = self.client.receiveBuffer[0][27]
        self.k_2     = self.client.receiveBuffer[0][28]
        self.k_3     = self.client.receiveBuffer[0][29]
        self.k_4     = self.client.receiveBuffer[0][30]
        self.k_5     = self.client.receiveBuffer[0][31]
        self.k_6     = self.client.receiveBuffer[0][32]
        self.k_7     = self.client.receiveBuffer[0][33]
        self.k_8     = self.client.receiveBuffer[0][34]
        self.k_9     = self.client.receiveBuffer[0][35]
        self.k_0     = self.client.receiveBuffer[0][36]

    def poll(self):
        '''This method checks if any of the 37 supported keys are
        currently pressed.'''
        # check if any of the 30 keys is pressed
        return np.any(self.client.receiveBuffer)

    def update(self):
        '''This method updates the keyboard variables to the
        current key press status.'''
        new, bytesReceived = self.client.receive()
        if new and self.poll: self.assign()
        return new

    def checkConnection(self):
        self.client.checkConnection()
        self.connected = self.client.connected

    def print(self):
        os.system('cls')
        print('Space:', self.k_space, ', Home:', self.k_home, ', Esc:', self.k_esc)
        print('Up:', self.k_up, ', Down:', self.k_down, ', Right:', self.k_right, ', Left:', self.k_left)
        print('W:', self.k_w, ', S:', self.k_s, ', D:', self.k_d, ', A:', self.k_a)
        print('X:', self.k_x, ', Y:', self.k_y, ', Z:', self.k_z)
        print('G:', self.k_g, ', F:', self.k_f, ', R:', self.k_r, ', T:', self.k_t)
        print('NP 1:', int(self.k_np1), ', NP 2:', int(self.k_np2), ', NP 3:', int(self.k_np3), ', NP 4:', int(self.k_np4), ', NP 5:', int(self.k_np5), ', NP 6:', int(self.k_np6), ', NP 7:', int(self.k_np7), ', NP 8:', int(self.k_np8), ', NP 9:', int(self.k_np9))
        print('1:', int(self.k_1), ', 2:', int(self.k_2), ', 3:', int(self.k_3), ', 4:', int(self.k_4), ', 5:', int(self.k_5), ', 6:', int(self.k_6), ', 7:', int(self.k_7), ', 8:', int(self.k_8), ', 9:', int(self.k_9), ', 0:', int(self.k_0))

    def terminate(self):
        '''This method terminates the Keyboard and it's client gracefully.'''
        self.client.terminate()

class QKeyboard():

    K_SPACE = 0
    K_HOME  = 1
    K_ESC   = 2
    K_UP    = 3
    K_DOWN  = 4
    K_RIGHT = 5
    K_LEFT  = 6
    K_W     = 7
    K_S     = 8
    K_D     = 9
    K_A     = 10
    K_X     = 11
    K_Y     = 12
    K_Z     = 13
    K_G     = 14
    K_F     = 15
    K_R     = 16
    K_T     = 17
    K_NP0   = 18
    K_NP1   = 19
    K_NP2   = 20
    K_NP3   = 21
    K_NP4   = 22
    K_NP5   = 23
    K_NP6   = 24
    K_NP7   = 25
    K_NP8   = 26
    K_NP9   = 27
    K_0     = 28
    K_1     = 29
    K_2     = 30
    K_3     = 31
    K_4     = 32
    K_5     = 33
    K_6     = 34
    K_7     = 35
    K_8     = 36
    K_9     = 37

    def __init__(self):
        self.kbd = Keyboard()

        self.keys = np.array([VirtualKeyCodes.VK_SPACE,
                         VirtualKeyCodes.VK_HOME,
                         VirtualKeyCodes.VK_ESCAPE,
                         VirtualKeyCodes.VK_UP,
                         VirtualKeyCodes.VK_DOWN,
                         VirtualKeyCodes.VK_RIGHT,
                         VirtualKeyCodes.VK_LEFT,
                         VirtualKeyCodes.VK_W,
                         VirtualKeyCodes.VK_S,
                         VirtualKeyCodes.VK_D,
                         VirtualKeyCodes.VK_A,
                         VirtualKeyCodes.VK_X,
                         VirtualKeyCodes.VK_Y,
                         VirtualKeyCodes.VK_Z,
                         VirtualKeyCodes.VK_G,
                         VirtualKeyCodes.VK_F,
                         VirtualKeyCodes.VK_R,
                         VirtualKeyCodes.VK_T,
                         VirtualKeyCodes.VK_NUMPAD0,
                         VirtualKeyCodes.VK_NUMPAD1,
                         VirtualKeyCodes.VK_NUMPAD2,
                         VirtualKeyCodes.VK_NUMPAD3,
                         VirtualKeyCodes.VK_NUMPAD4,
                         VirtualKeyCodes.VK_NUMPAD5,
                         VirtualKeyCodes.VK_NUMPAD6,
                         VirtualKeyCodes.VK_NUMPAD7,
                         VirtualKeyCodes.VK_NUMPAD8,
                         VirtualKeyCodes.VK_NUMPAD9,
                         VirtualKeyCodes.VK_0,
                         VirtualKeyCodes.VK_1,
                         VirtualKeyCodes.VK_2,
                         VirtualKeyCodes.VK_3,
                         VirtualKeyCodes.VK_4,
                         VirtualKeyCodes.VK_5,
                         VirtualKeyCodes.VK_6,
                         VirtualKeyCodes.VK_7,
                         VirtualKeyCodes.VK_8,
                         VirtualKeyCodes.VK_9], dtype=np.int32)
        self.states_raw = self.kbd.createBuffer(len(self.keys))
        self.update()

    def update(self):
        self.kbd.getKeyStates(self.keys, self.states_raw)
        self.states = self.states_raw
        for idx, key in enumerate(self.states_raw):
            self.states[idx] = bool(key and KeyState.KEY_DOWN)
