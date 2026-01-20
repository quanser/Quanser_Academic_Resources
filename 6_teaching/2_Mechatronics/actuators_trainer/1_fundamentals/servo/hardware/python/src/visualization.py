import numpy as np
import os
import cv2

class VisualizePWM():
    def __init__(self, kbd, dim):
        self.kbd = kbd
        self.dim = dim
        self.dutyCycle = int(dim/2)
        self.counter = 0
        self.rows = 300
        self.cols = 600
        self.sec = 30
        ledImg = cv2.cvtColor(cv2.imread('src/pwm_led.png'), cv2.COLOR_RGB2GRAY)
        self.img = 125*np.ones((self.rows, self.cols), dtype=np.uint8)
        self.bar = np.zeros((self.sec, self.cols), dtype=np.uint8)
        self.img = np.vstack((np.vstack((self.img, self.bar)), ledImg))

    def render(self):
        if self.kbd.states[self.kbd.K_RIGHT]:
            self.dutyCycle = self.dutyCycle + 1
            if self.dutyCycle >= self.dim-1: self.dutyCycle = self.dim-1
        elif self.kbd.states[self.kbd.K_LEFT]:
            self.dutyCycle = self.dutyCycle - 1
            if self.dutyCycle < 1: self.dutyCycle = 1

        # Top left section (pick black or white based on counter & dim)
        if (self.counter % self.dim) >= self.dutyCycle:
            self.img[0:self.rows, 0:int(self.cols/2)] = np.zeros((self.rows, int(self.cols/2)), dtype=np.uint8)
        else:
            self.img[0:self.rows, 0:int(self.cols/2)] = 255*np.ones((self.rows, int(self.cols/2)), dtype=np.uint8)

        # Top right section (average color for the square)
        self.img[0:self.rows, int(self.cols/2):self.cols] = int(255*self.dutyCycle/self.dim)*np.ones((self.rows, int(self.cols/2)), dtype=np.uint8)

        # Middle horizontal bar representing the current duty cycle
        self.img[self.rows:self.rows+self.sec, 0:int(self.cols*(self.dutyCycle)/self.dim)] = 235
        self.img[self.rows:self.rows+self.sec, int(self.cols*(self.dutyCycle)/self.dim):self.cols] = 20
        self.counter = self.counter + 1
        if self.counter % 20 == 0:
            clear_cmd = 'cls' if os.name == 'nt' else 'clear'
            try:
                os.system(clear_cmd)
            except Exception:
                pass
            print("Duty Cycle is at", int(100*self.dutyCycle/self.dim), "%.")
        cv2.imshow('PWM Visualization',  self.img)
        cv2.waitKey(1)