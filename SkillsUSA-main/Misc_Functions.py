import arcade as arc
import Globals
from random import randrange
from os import walk
from math import sqrt, sin


# basically just the randrange function, but automatically puts the lower value first
def easy_randrange(value1, value2, step=1):
    if value1 > value2:
        return randrange(value2, value1, step)
    elif value1 < value2:
        return randrange(value1, value2, step)
    else:
        return value1


# use for sets of animations that DO NOT need to be flipped horizontally
def load_animation_one(path):
    frames = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image_texture = arc.load_texture(full_path)
            frames.append(image_texture)
    return frames


# Check if point is within bounds of rectangle.
def IsRectCollidingWithPoint(rect, point):
    if rect[3][0] >= point[0] >= rect[0][0] and rect[1][1] >= point[1] >= rect[0][1]:
        return True
    else:
        return False


def get_closest_wall(object, walls):
    closest_wall = walls[0]
    closest_wall_dist = sqrt(abs(object.center_y - walls[0].center_y)**2 + abs(object.center_x - walls[0].center_x)**2)
    for wall in walls:
        wall_dist = sqrt(abs(object.center_y - wall.center_y) ** 2 + abs(object.center_x - wall.center_x) ** 2)
        if wall_dist < closest_wall_dist:
            closest_wall = wall
            closest_wall_dist = wall_dist

    return closest_wall


def get_turn_multiplier(speed):
    return speed / (Globals.PLAYER_MAX_SPEED / 1.5)


def get_shade(r, c, color_range):
    cell_shade = int((sin(r / Globals.CELL_COLOR_GRANULARITY) + sin(c / Globals.CELL_COLOR_GRANULARITY) + 2)
                     / 4 * (color_range[1] - color_range[0])) + color_range[0]
    return cell_shade
