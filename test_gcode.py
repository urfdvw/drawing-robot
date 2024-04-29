def p2(x):
    """Power of 2."""
    return x * x

last_pen = False
last_x = 0
last_y = 0

min_x = float('inf')
max_x = float('-inf')
min_y = float('inf')
max_y = float('-inf')

target_min_x = -20
target_max_x = 10
target_min_y = 50
target_max_y = 80
with open('owl.gcode') as f:
    for line in f:
        commands = line.strip().split(' ')
        if commands[0] == 'G0' or commands[0] == 'G1':
            x = float(commands[1][1:])
            y = float(commands[2][1:])
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)

print('startplot:', 'x', 'y')
with open('owl.gcode') as f:
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
            print(x, y)
            last_x = x
            last_y = y
        if commands[0] == 'G0':
            # print('startplot:', 'x', 'y')
            pass
        if commands[0] == 'G1':
            pass