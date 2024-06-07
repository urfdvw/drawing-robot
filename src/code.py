import time
import board
from connected_variables import ConnectedVariables

from drawing_robot import DrawingRobot, drawGcode

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
cv.define('file', '')

while True:
    if cv.read('file'):
        # try:
        drawGcode(robot, cv.read('file') + '.gcode')
        # except:
        #     pass
        cv.write('file', '')
    else:
        pos = cv.read('draw_pos')
        robot.move_xy(bool(pos['z']), pos['x'], pos['y'])