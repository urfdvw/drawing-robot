"""
- left
    - GP5
    - 0: reach
    - 90: back
    - drift: 0
- right
    - GP6
    - 0: back
    - 90: reach
    - drift: + 80
- lift
    - GP4
    - 60: pen down
    - 0: pen raise
"""

import time
import board
import pwmio
import math
from adafruit_motor import servo

class DrawingRobot:
    def __init__(self, pen_pin, left_pin, right_pin):
        pwm_pen = pwmio.PWMOut(pen_pin, duty_cycle=2 ** 15, frequency=50)
        pwm_left = pwmio.PWMOut(left_pin, duty_cycle=2 ** 15, frequency=50)
        pwm_right = pwmio.PWMOut(right_pin, duty_cycle=2 ** 15, frequency=50)
        
        self.servo_pen = servo.Servo(pwm_pen, min_pulse = 500, max_pulse = 2500)
        self.servo_left = servo.Servo(pwm_left, min_pulse = 500, max_pulse = 2500)
        self.servo_right = servo.Servo(pwm_right, min_pulse = 500, max_pulse = 2500)
        
        # init
        self.last_pen = False
        self.last_left = 0
        self.last_right = 0
        self.use_pen(self.last_pen)
        self.set_left(0)
        self.set_right(0)

    def set_left(self, r):
        d = r / math.pi * 180
        self.servo_left.angle = 90 - d
        
    def set_right(self, r):
        d = r / math.pi * 180
        self.servo_right.angle = d + 80
        
    def use_pen(self, use):
        if use:
            self.servo_pen.angle = 60
        else:
            self.servo_pen.angle = 30 # 0: full
            
    def wait_move(self, pen, left, right):
        time.sleep(max([
            abs(self.last_left - left),
            abs(self.last_right - right),
        ]) * (0.8 if pen else 0.1)) # speed control
        
    def wait_pen(self, pen):
        if pen != self.last_pen:
            if pen:
                time.sleep(0.3)
            else:
                time.sleep(0.1)
        
    def move(self, pen, left, right):
        if pen:
            self.set_left(left)
            self.set_right(right)
            self.wait_move(pen, left, right)
            self.use_pen(pen)
            self.wait_pen(pen)
        else:
            self.use_pen(pen)
            self.wait_pen(pen)
            self.set_left(left)
            self.set_right(right)
            self.wait_move(pen, left, right)
        self.last_pen = pen
        self.last_left = left
        self.last_right = right
        
robot = DrawingRobot(board.GP4, board.GP5, board.GP6)

#%%
robot.move(False, 0, 0)
pos_left = 0.0
pos_right = 0.0
# print('startplot:', 'r_left', 'r_right')
while pos_left < math.pi * 4:
    r_left = (math.sin(pos_left) + 1) / 2 * math.pi / 2
    r_right = (math.cos(pos_right) + 1) / 2 * math.pi / 2
    if r_left < math.pi / 4 and r_right > math.pi / 4:
        robot.move(False, r_left, r_right)
    else:
        robot.move(True, r_left, r_right)
    # print(r_left, r_right)
    pos_left += math.pi * 0.002
    pos_right += math.pi * 0.005

#%%
robot.move(False, 0, 0)
time.sleep(5)