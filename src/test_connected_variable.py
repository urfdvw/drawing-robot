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

# from test_gcode import *
# import sys
# sys.exit()
#%%

import time
import board
import pwmio
import math
from adafruit_motor import servo
from connected_variables import ConnectedVariables

def p2(x):
    """Power of 2."""
    return x * x

class DrawingRobot:
    def __init__(
        self,
        pen_pin,
        left_pin,
        right_pin,
        a,
        b,
        c,
        d
    ):
        self.a, self.b, self.c, self.d = a, b, c, d
        
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
        ]) * (0.2 if pen else 0.1)) # speed control
        
    def wait_pen(self, pen):
        if pen != self.last_pen:
            if pen:
                time.sleep(0.3)
            else:
                time.sleep(0.3)
        
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
        
    def move_xy(self, pen, x0, y0):
        a, b, c, d = self.a, self.b, self.c, self.d
        k1A = (a - x0) / y0
        k0A = (p2(c + d) + p2(a) - p2(b) - p2(x0) - p2(y0)) / (-2 * y0)
        # print(k1A, k0A)
        aA = 1 + p2(k1A)
        bA = 2 * (-a + k1A * k0A)
        cA = p2(a) + p2(k0A) - p2(b)
        
        under_root_A = p2(bA) - 4 * aA * cA
        if under_root_A < 0:
            return False
        xA = (-bA + math.sqrt(under_root_A))/(2 * aA)
        yA = k1A * xA  + k0A
        angle_right = math.atan2(yA, xA - a)
        # print(xA, yA)
        # print(angle_left / math.pi * 180)
        
        x1 = (x0 - xA) * c / (c + d) + xA
        y1 = (y0 - yA) * c / (c + d) + yA
        
        k1B = (-a - x1) / y1
        k0B = (p2(c) + p2(-a) - p2(b) - p2(x1) - p2(y1)) / (-2 * y1)
        # print(k1B, k0B)
        aB = 1 + p2(k1B)
        bB = 2 * (a + k1B * k0B)
        cB = p2(-a) + p2(k0B) - p2(b)
        
        under_root_B = p2(bB) - 4 * aB * cB
        if under_root_B < 0:
            return False
        xB = (-bB - math.sqrt(under_root_B))/(2 * aB)
        yB = k1B * xB  + k0B
        angle_left = math.atan2(yB, -xB - a)
        # print(xB, yB)
        # print(angle_right / math.pi * 180)
        if (
            angle_left > -20 / 180 * math.pi and
            angle_left < math.pi / 2 and
            angle_right > -20 / 180 * math.pi and
            angle_right < math.pi / 2
        ):
            self.move(pen, angle_left, angle_right)
            return True
        else:
            return False
        
robot = DrawingRobot(
    board.GP4,
    board.GP5,
    board.GP6,
    23.2,
    30.0,
    60.0,
    12.5
)

#%%
robot.move(False, 0, 0)

cv = ConnectedVariables()
cv.define('draw_pos', {'x': 0, 'y': 50, 'z': 0})

while True:
    pos = cv.read('draw_pos')
    robot.move_xy(bool(pos['z']), pos['x'], pos['y'])
