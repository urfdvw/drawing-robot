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

pwm_pen = pwmio.PWMOut(board.GP4, duty_cycle=2 ** 15, frequency=50)
pwm_left = pwmio.PWMOut(board.GP5, duty_cycle=2 ** 15, frequency=50)
pwm_right = pwmio.PWMOut(board.GP6, duty_cycle=2 ** 15, frequency=50)

servo_pen = servo.Servo(pwm_pen, min_pulse = 500, max_pulse = 2500)
servo_left = servo.Servo(pwm_left, min_pulse = 500, max_pulse = 2500)
servo_right = servo.Servo(pwm_right, min_pulse = 500, max_pulse = 2500)

def set_left(r):
    d = r / math.pi * 180
    servo_left.angle = 90 - d
    
def set_right(r):
    d = r / math.pi * 180
    servo_right.angle = d + 80
    
def use_pen(use):
    if use:
        servo_pen.angle = 60
    else:
        servo_pen.angle = 0
    
servo_right.angle = (90 + 80)
servo_left.angle = 0

#%%
pos_left = 0.0
pos_right = 0.0
use_pen(False)
# print('startplot:', 'r_left', 'r_right')
while pos_left < math.pi * 4:
    pos_left += math.pi * 0.002
    pos_right += math.pi * 0.005
    r_left = (math.sin(pos_left) + 1) / 2 * math.pi / 2
    r_right = (math.cos(pos_right) + 1) / 2 * math.pi / 2
    # print(r_left, r_right)
    set_left(r_left)
    set_right(r_right)
    if r_left < 45 and r_right > 45:
        use_pen(False)
        time.sleep(0.003)
    else:
        use_pen(True)
        time.sleep(0.01)

#%%
set_left(0)
set_right(0)
use_pen(False)
time.sleep(5)