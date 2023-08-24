import arcade as arc
import Globals
from Misc_Functions import load_animation_one
from math import cos, radians, sin


class DrillGui(arc.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arc.load_texture("Assets/Powerups/drill/drill1.png")
        self.color = arc.color.BLACK
        self.alpha = 99
        self.scale = .3
        self.center_x = x
        self.center_y = y

        self.activation_text = arc.Text("Space/X", self.left, self.bottom, font_name="ARCADECLASSIC")

    def toggle(self):
        if self.color == arc.color.BLACK:
            self.color = (255, 255, 255)
        else:
            self.color = arc.color.BLACK


class PowerUp(arc.Sprite):
    def __init__(self):
        super().__init__()
        self.type = "base"

        self.cur_frame = 0


class PowerUpBox(arc.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arc.load_texture("Assets/Powerups/drill_power_up_box.png")
        self.scale = .3


class Drill(PowerUp):
    def __init__(self, launch_angle):
        super().__init__()
        self.type = "drill"
        self.animation = load_animation_one("Assets/Powerups/drill")
        self.texture = arc.load_texture("Assets/Powerups/drill/drill1.png")
        self.set_hit_box(self.texture.hit_box_points)

        self.scale = .5
        self.angle = launch_angle + 90

        self.change_x = Globals.DRILL_SPEED
        self.change_y = Globals.DRILL_SPEED

        self.timer = 0

        self.k_bar_marg = Globals.CELL_WIDTH * 3

    def update(self):
        self.timer += 1
        self.center_x += -self.change_y * sin(radians(self.angle - 90))
        self.center_y += self.change_y * cos(radians(self.angle - 90))\

        # delete drill if too close to outside of track
        if not (self.k_bar_marg <= self.center_x <= (Globals.CELL_GRID_WIDTH - self.k_bar_marg)) or \
                not (self.k_bar_marg <= self.center_y <= (Globals.CELL_GRID_HEIGHT - self.k_bar_marg)):
            self.kill()

        # kill drill after a bit of time, could have it die in a dif way
        if self.timer >= 100:
            self.kill()

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_frame += .3
        self.texture = self.animation[round(round(self.cur_frame) % len(self.animation))]


class EndEntrance(arc.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arc.load_texture("Assets/Other/sunlight.png")
