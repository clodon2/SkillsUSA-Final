import arcade as arc
import Globals


# basic button, meant for demos
class BasicButton:
    def __init__(self, text, location, size=(400, 100),
                 color=arc.csscolor.BLACK, textcolor=arc.csscolor.WHITE,
                 tilt=0, id='none', font="Kenney Future Font"):
        self.id = id
        self.text = text

        size = (size[0] * Globals.SCREEN_PERCENTS[0], size[1] * Globals.SCREEN_PERCENTS[1])

        # scaling values
        base_b_size = (400, 100)
        b_scales = (size[0] / base_b_size[0], size[1] / base_b_size[1])
        b_scale = (b_scales[0] + b_scales[1]) / 2

        self.text_size = Globals.DEFAULT_FONT_SIZE * b_scale

        base = arc.create_rectangle_filled(location[0], location[1], size[0], size[1], color, tilt)
        self.basepoints = arc.get_rectangle_points(location[0], location[1], size[0], size[1], tilt)

        textstartx = location[0]
        textstarty = location[1] - self.text_size / 2
        text = arc.Text(text, textstartx, textstarty, textcolor, font_size=self.text_size,
                        font_name=font)
        text.x = location[0] - text.content_width/2

        self.buttonfull = [base, text]

    def update(self):
        for i in self.buttonfull:
            i.draw()

    def get_rect(self):
        return self.basepoints


# example class, may or may not work
class TexturedButton:
    def __init__(self, text, sprite, location,
                 textcolor=arc.csscolor.WHITE,
                 tilt=0, animated=False, scale=1,
                 font="Arial", font_size=Globals.DEFAULT_FONT_SIZE,
                 y_offset=0, id='none'):
        font_size = font_size * Globals.SCREEN_PERCENT

        self.animated = animated
        self.location = location
        self.scale = scale
        self.id = id

        textstartx = location[0]
        textstarty = location[1] - 13
        self.text = arc.Text(text, textstartx, textstarty,
                             textcolor, font_size=font_size,
                             font_name=font, bold=True)
        self.text.x = location[0] - (self.text.content_width/2)
        self.texttop = self.text.y + y_offset
        self.textbottom = self.texttop - 9

        if not self.animated:
            self.texture = arc.load_texture(sprite)
        else:
            self.animation = mf.load_animation_one(sprite)
            self.texture = self.animation[0]
            self.frame = 0
            self.highlighted = False

        self.rect = arc.get_rectangle_points(location[0], location[1],
                                             self.texture.width - 160, self.texture.height - 40)

    def update(self):
        if self.animated:
            if self.highlighted:
                self.text.y = self.textbottom
                if self.frame < len(self.animation) - 1:
                    self.frame += 1
                self.animation[self.frame].draw_scaled(self.location[0], self.location[1], self.scale)
            else:
                self.text.y = self.texttop
                self.animation[0].draw_scaled(self.location[0], self.location[1], self.scale)
            self.text.draw()
        else:
            self.animation.draw_scaled(self.location[0], self.location[1], self.scale)
            self.text.draw()

    def get_box(self):
        return self.rect


class BasicText:
    def __init__(self, text, location,
                 textsize=Globals.DEFAULT_FONT_SIZE,
                 text_color=arc.color.BLACK, font='arial'):
        self.text_size = textsize * Globals.SCREEN_PERCENT
        text_y = location[1] - self.text_size/2
        self.text = arc.Text(text, location[0], text_y,
                             text_color, self.text_size, font_name=font, multiline=True,
                             width=(Globals.SCREEN_WIDTH - (Globals.SCREEN_WIDTH / 20)))
        self.text.x = location[0] - self.text.content_width/2

    def update(self):
        self.text.draw()


def start_menu(view):
    # Setup the Cameras
    view.camera = arc.Camera(view.width, view.height)
    # needed to load buttons and text
    view.text_list = []
    view.button_list = []

    # example stuff
    startbutton = BasicButton("START", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 2),
                                 size=(300, 110), id='start', font="ARCADECLASSIC")
    controlsbutton = BasicButton("CONTROLS", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 4.5),
                                    size=(300, 110), id='controls', font="ARCADECLASSIC")

    title = BasicText("Cave Racer", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 1.2),
                      textsize=60, font="ARCADECLASSIC", text_color=arc.color.WHITE)

    # should probably make an easier way to do this
    view.button_list.append(startbutton)
    view.button_list.append(controlsbutton)
    view.text_list.append(title)

    view.mouse_pos = 0, 0
    view.window.set_mouse_visible(True)


def controls_menu(view):
    # Setup the Cameras
    view.camera = arc.Camera(view.width, view.height)
    # needed to load buttons and text
    view.text_list = []
    view.button_list = []

    # example stuff
    startbutton = BasicButton("BACK", location=(50 * Globals.SCREEN_PERCENT, Globals.SCREEN_HEIGHT / 1.12),
                                 size=(100, 100), id='back', font="ARCADECLASSIC")

    title = BasicText("Controls", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 1.2),
                      textsize=60, font="ARCADECLASSIC", text_color=arc.color.WHITE)

    text_objs = [
                 BasicText("Forward - W/Up Arrow/Right Trigger",
                           location=(Globals.MID_SCREEN, 500 * Globals.SCREEN_PERCENTS[1]),
                           textsize=30, font="ARCADECLASSIC", text_color=arc.color.WHITE),

                 BasicText("Backward - S/Down Arrow/Left Trigger",
                           location=(Globals.MID_SCREEN, 450 * Globals.SCREEN_PERCENTS[1]),
                           textsize=30, font="ARCADECLASSIC", text_color=arc.color.WHITE),

                 BasicText("Right - D/Right Arrow/Left Joystick",
                           location=(Globals.MID_SCREEN, 400 * Globals.SCREEN_PERCENTS[1]),
                           textsize=30, font="ARCADECLASSIC", text_color=arc.color.WHITE),

                 BasicText("Left - A/Right Arrow/Left Joystick",
                           location=(Globals.MID_SCREEN, 350 * Globals.SCREEN_PERCENTS[1]),
                           textsize=30, font="ARCADECLASSIC", text_color=arc.color.WHITE),

                 BasicText("Powerup - Space/X (left) button",
                           location=(Globals.MID_SCREEN, 300 * Globals.SCREEN_PERCENTS[1]),
                           textsize=30, font="ARCADECLASSIC", text_color=arc.color.WHITE),
    ]

    # should probably make an easier way to do this
    view.button_list.append(startbutton)
    view.text_list.append(title)
    view.text_list.extend(text_objs)

    view.mouse_pos = 0, 0
    view.window.set_mouse_visible(True)


def win_menu(view):
    # Setup the Cameras
    view.camera = arc.Camera(view.width, view.height)
    # needed to load buttons and text
    view.text_list = []
    view.button_list = []

    title = BasicText("Well done, Cave Master! \n + 5000 points", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 1.2),
                      textsize=60, font="ARCADECLASSIC", text_color=arc.color.WHITE)

    exit_button = BasicButton("Back To Main Menu", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 3),
                              size=(300, 110), id='back', font="ARCADECLASSIC")

    view.button_list.append(exit_button)
    view.text_list.append(title)


def loss_menu(view):
    # Setup the Cameras
    view.camera = arc.Camera(view.width, view.height)
    # needed to load buttons and text
    view.text_list = []
    view.button_list = []

    title = BasicText("You were eliminated from the race, -1000 points", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 1.2),
                      textsize=60, font="ARCADECLASSIC", text_color=arc.color.WHITE)

    exit_button = BasicButton("Back To Main Menu", location=(Globals.MID_SCREEN, Globals.SCREEN_HEIGHT / 3),
                              size=(300, 110), id='back', font="ARCADECLASSIC")

    view.button_list.append(exit_button)
    view.text_list.append(title)
