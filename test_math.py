import math

def p2(x):
    """Power of 2."""
    return x * x
    
x0, y0 = 0, 40

a, b, c, d = 23.2, 30.0, 60.0, 12.5

k1A = (a - x0) / y0
k0A = (p2(c + d) + p2(a) - p2(b) - p2(x0) - p2(y0)) / (-2 * y0)
print(k1A, k0A)
aA = 1 + p2(k1A)
bA = 2 * (-a + k1A * k0A)
cA = p2(a) + p2(k0A) - p2(b)

under_root_A = p2(bA) - 4 * aA * cA
if under_root_A < 0:
    print('no solution to given position')
    # return
xA = (-bA + math.sqrt(under_root_A))/(2 * aA)
yA = k1A * xA  + k0A
angle_left = math.atan2(yA, xA - a)
print(xA, yA)
print(angle_left / math.pi * 180)

x1 = (x0 - xA) * c / (c + d) + xA
y1 = (y0 - yA) * c / (c + d) + yA

k1B = (-a - x1) / y1
k0B = (p2(c) + p2(-a) - p2(b) - p2(x1) - p2(y1)) / (-2 * y1)
print(k1B, k0B)
aB = 1 + p2(k1B)
bB = 2 * (a + k1B * k0B)
cB = p2(-a) + p2(k0B) - p2(b)

under_root_B = p2(bB) - 4 * aB * cB
if under_root_B < 0:
    print('no solution to given position')
    # return
xB = (-bB - math.sqrt(under_root_B))/(2 * aB)
yB = k1B * xB  + k0B
angle_right = math.atan2(yB, -xB - a)
print(xB, yB)
print(angle_right / math.pi * 180)