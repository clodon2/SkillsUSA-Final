import arcade as arc
import Globals
from math import sin, cos, radians, degrees, sqrt, atan2, pi, copysign


class Car(arc.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        self.center_x = -self.change_y * sin(radians(self.angle))

        self.center_y = self.change_y * cos(radians(self.angle))


class BasicBot(arc.Sprite):
    def __init__(self, walls, track_points):
        super().__init__("./Assets/Enemy/enemycar.png")

        self.scale = .3 * Globals.SCREEN_PERCENT
        self.angle = -90

        self.desired_angle = 0

        self.walls = walls
        self.track_points = track_points
        self.last_track_point = -1

        self.wall_closeness = Globals.CELL_HEIGHT * 1.5

        self.speed = 0

        self.max_speed = Globals.BOT_MAX_SPEED

    def accelerate(self):
        '''
        if self.change_y < self.max_speed:
            self.change_y += 2
        '''
        self.change_y = self.max_speed

    def update(self):
        if self.last_track_point + 1 == len(self.track_points):
            self.last_track_point -= 1

        next_track_point = self.track_points[self.last_track_point + 1]
        next_track_point_pos = (next_track_point[1] * Globals.CELL_WIDTH + Globals.GRID_BL_POS[1],
                                next_track_point[0] * Globals.CELL_HEIGHT + Globals.GRID_BL_POS[0])

        if sqrt(abs(next_track_point_pos[0] - self.center_x)**2 + abs(next_track_point_pos[1] - self.center_y)**2)\
                < 10 * Globals.CELL_HEIGHT:
            self.last_track_point += 1

        self.angle %= 360

        desired_angle = atan2(next_track_point_pos[1] - self.center_y, next_track_point_pos[0] - self.center_x)

        self.desired_angle = desired_angle  # for debugging

        angle = self.angle - degrees(desired_angle - (pi/2)) - 360

        if angle < -Globals.BOT_MIN_TURN_ANGLE:
            self.angle += Globals.PLAYER_ROTATION_SPEED
        elif angle > Globals.BOT_MIN_TURN_ANGLE:
            self.angle -= Globals.PLAYER_ROTATION_SPEED

        self.accelerate()

        self.center_x += -self.change_y * sin(radians(self.angle))
        self.center_y += self.change_y * cos(radians(self.angle))

        # Keep in bounds
        if self.center_x < 0:
            self.center_x = 0
        if self.center_y < 0:
            self.center_y = 0

        if self.center_x > Globals.CELL_GRID_WIDTH:
            self.center_x = Globals.CELL_GRID_WIDTH
        if self.center_y > Globals.CELL_GRID_HEIGHT:
            self.center_y = Globals.CELL_GRID_HEIGHT

        self.change_x = 0
        self.change_y = 0
