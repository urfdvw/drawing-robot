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
    - drift: + 13
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

#%%
servo_pen.angle = 0
r1 = 0.0
r2 = 0.0
# print('startplot:', 'p1', 'p2')
while r1 < math.pi * 4:
    r1 += math.pi * 0.002
    r2 += math.pi * 0.005
    p1 = (math.sin(r1) + 1) / 2 * 90
    p2 = (math.cos(r2) + 1) / 2 * 90
    # print(p1, p2)
    servo_left.angle = p1
    servo_right.angle = p2 + 13
    if p1 < 45 and p2 > 45:
        servo_pen.angle = 0
        time.sleep(0.001)
    else:
        servo_pen.angle = 60
        time.sleep(0.01)

servo_pen.angle = 0
time.sleep(5)