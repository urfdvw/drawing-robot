import time
import math
import pwmio
from adafruit_motor import servo

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
        ]) * (0.2 if pen else 0.2)) # speed control
        
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
        
def drawGcode(robot, gcode_name):
    last_x = 0
    last_y = 0
    
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    
    target_min_x = -25
    target_max_x = 15
    target_min_y = 45
    target_max_y = 85
    try:
        open(gcode_name)
    except:
        print("no such file")
        return
    with open(gcode_name) as f:
        for line in f:
            commands = line.strip().split(' ')
            if commands[0] == 'G0' or commands[0] == 'G1':
                x = float(commands[1][1:])
                y = float(commands[2][1:])
                min_x = min(x, min_x)
                max_x = max(x, max_x)
                min_y = min(y, min_y)
                max_y = max(y, max_y)
                
    ratio = (max_y - min_y) / (max_x - min_x)
    target_ratio = (target_max_y - target_min_y) / (target_max_x - target_min_x)
    
    if target_ratio < ratio:
        target_max_x = (target_max_y - target_min_y) / ratio + target_min_x
    else:
        target_max_y = (target_max_x - target_min_x) * ratio + target_min_y
    # print(target_max_x, target_max_y)
    
    # print('startplot:', 'x', 'y')
    with open(gcode_name) as f:
        for line in f:
            commands = line.strip().split(' ')
            if commands[0] == 'G0' or commands[0] == 'G1':
                x = float(commands[1][1:]) 
                x = (x - min_x) / (max_x - min_x) * (target_max_x - target_min_x) + target_min_x
                y = float(commands[2][1:])
                y = (y - min_y) / (max_y - min_y) * (target_max_y - target_min_y) + target_min_y
                if commands[0] == 'G1':
                    if abs(p2(x - last_x) + p2(y - last_y)) < p2(0.5):
                        continue
                # print(x, y)
                last_x = x
                last_y = y
            if commands[0] == 'G0':
                robot.move_xy(False, x, y)
            if commands[0] == 'G1':
                robot.move_xy(True, x, y)
    robot.move(False, 0, 0)