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
        self.set_left(0)
        self.set_right(0)
        self.last_pen = False
        self.use_pen(self.last_pen)

    def set_left(self, r):
        d = r / math.pi * 180
        self.servo_left.angle = 90 - d
        
    def set_right(self, r):
        d = r / math.pi * 180
        self.servo_right.angle = d + 80
        
    def use_pen(self, use):
        if use:
            self.servo_pen.angle = 60
            if use != self.last_pen:
                time.sleep(0.5)
        else:
            self.servo_pen.angle = 0
        self.last_pen = use
    
robot = DrawingRobot(board.GP4, board.GP5, board.GP6)

#%%
pos_left = 0.0
pos_right = 0.0
# print('startplot:', 'r_left', 'r_right')
while pos_left < math.pi * 4:
    pos_left += math.pi * 0.002
    pos_right += math.pi * 0.005
    r_left = (math.sin(pos_left) + 1) / 2 * math.pi / 2
    r_right = (math.cos(pos_right) + 1) / 2 * math.pi / 2
    # print(r_left, r_right)
    robot.set_left(r_left)
    robot.set_right(r_right)
    if r_left < math.pi / 4 and r_right > math.pi / 4:
        robot.use_pen(False)
        time.sleep(0.003)
    else:
        robot.use_pen(True)
        time.sleep(0.01)

#%%
robot.set_left(0)
robot.set_right(0)
robot.use_pen(False)
time.sleep(5)