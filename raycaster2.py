import math
try:
    import casioplot
except:
    import casioplotemulator as casioplot

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)
    __rmul__ = __mul__

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def angleForDisplay(self):
        sign = 1
        if self.y < 0: sign = -1
        # calculate angle between self and <0, 1>
        return math.acos(self.x / self.magnitude()) * sign

WIDTH = 128
HEIGHT = 64
MIDDLE_X = 64
MIDDLE_Y = 32

FOV = math.pi / 3

map_nodes = []
player_pos = Vector2(0, 0)
player_rot = 0

for i in range(12):
    map_nodes.append(Vector2(2.5 * math.cos(math.pi / 6 * i), 2.5 * math.sin(math.pi / 6 * i)))

# for i in range(50):
#     map_nodes.append(Vector2(4.5 * math.cos(math.pi / 25 * i), 4.5 * math.sin(math.pi / 25 * i)))

def modAngle(raw_angle):
    return raw_angle % (-2 * math.pi) if raw_angle < 0 else raw_angle % (2 * math.pi)

def angleDiff(a, b):
    raw_difference = b - a
    return (raw_difference + math.pi) % (2 * math.pi) - math.pi

def angleBetweenDisplay(v1, v2):
    return angleDiff(v1.angleForDisplay(), v2.angleForDisplay())

def angleRelativeToPlayer(v2):
    return angleDiff(player_rot, v2.angleForDisplay())

def inView(angle):
    return modAngle(abs(angle)) <= FOV

def distance(_from, to):
    return (to - _from).magnitude()

def heightMultiplier(pos, local_theta):
    return 1 / (distance(pos, player_pos) * math.cos(local_theta))

def drawLine(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    sx = -1
    if x0 < x1: sx = 1
    dy = -abs(y1 - y0)
    sy = -1
    if y0 < y1: sy = 1
    error = dx + dy
    
    while True:
        # if x0 > WIDTH or x0 < 0 or y0 > HEIGHT or y0 < 0: break
        towards_nothing_x = (sx > 0 and x0 > WIDTH) or (sx < 0 and x0 < 0)
        towards_nothing_y = (sy > 0 and y0 > HEIGHT) or (sy < 0 and y0 < 0)
        if towards_nothing_x or towards_nothing_y: break
        casioplot.set_pixel(x0, y0)
        if x0 == x1 and y0 == y1: break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1: break
            error = error + dy
            x0 += sx
        if e2 <= dx:
            if y0 == y1: break
            error = error + dx
            y0 += sy

def update():
    global player_rot
    casioplot.clear_screen()
    # casioplot.set_pixel(1,1)
    # drawLine(0, 0, 5, 3)

    on_screen = 0
    on_screen_coords = []
    angles = []

    prev_x = None
    prev_height = None
    prev_inview = False
    for node in map_nodes:
        raw_angle = angleRelativeToPlayer(node - player_pos)
        x = int(MIDDLE_X + raw_angle / FOV * WIDTH / 2)
        height = int(heightMultiplier(node, raw_angle) * HEIGHT / 2)
        inview = inView(raw_angle)

        if inview:
            on_screen += 1
            on_screen_coords.append(x)
            casioplot.set_pixel(x, MIDDLE_Y)
            for i in range(height):
                casioplot.set_pixel(x, MIDDLE_Y + i)
                casioplot.set_pixel(x, MIDDLE_Y - i)
        if prev_x != None and (inview or prev_inview):
            drawLine(prev_x, MIDDLE_Y + prev_height, x, MIDDLE_Y + height)
            drawLine(prev_x, MIDDLE_Y - prev_height, x, MIDDLE_Y - height)
        prev_x, prev_height = x, height
        prev_inview = inview

    print("rendering...")
    casioplot.show_screen()
    print(on_screen_coords)
    player_rot += 0.075
    player_rot = modAngle(player_rot)

drawLine

# casioplot.set_pixel(0, 0)
# casioplot.set_pixel(1, 1)
# casioplot.set_pixel(0, 1)
# casioplot.show_screen()

import time
while True:
    update()
    time.sleep(0.1)