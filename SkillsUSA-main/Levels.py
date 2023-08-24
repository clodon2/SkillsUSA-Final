import arcade

import Globals
import arcade as arc
from random import randrange
from Automata import generate_random_grid, run_sim, generate_track
from Bots import BasicBot
from Player import BasicPlayer
from World_Objects import PowerUpBox, EndEntrance
from Misc_Functions import get_shade
from math import sin, cos


def new_track(game):
    game.scene = arc.Scene()

    # load in track
    game.scene.add_sprite_list("cells", use_spatial_hash=True)
    game.grid, game.track_points = generate_track(Globals.GRID_WIDTH, Globals.GRID_HEIGHT)

    load_track(game)

    # spawn in powerup boxes
    game.scene.add_sprite_list_after("power_boxes", "cells", use_spatial_hash=True)
    spawn_amount = int((len(game.track_points) - 1) / 4)

    for box in range(spawn_amount):
        box_point = randrange(2, len(game.track_points) - 1, 1)
        box = PowerUpBox()
        box.center_x = game.track_points[box_point][1] * Globals.CELL_WIDTH
        box.center_y = game.track_points[box_point][0] * Globals.CELL_HEIGHT
        game.scene.add_sprite("power_boxes", box)

    # spawn in end of level
    game.scene.add_sprite_list_after("exit", "cells")
    last_point = game.track_points[-1]

    end_level = EndEntrance()
    end_level.center_x = last_point[1] * Globals.CELL_WIDTH
    end_level.center_y = last_point[0] * Globals.CELL_HEIGHT

    game.scene.add_sprite("exit", end_level)

    # player
    game.scene.add_sprite_list_after("player", "cells")

    game.player = BasicPlayer()
    game.player.center_x = 2 * Globals.CELL_WIDTH
    game.player.center_y = (Globals.GRID_HEIGHT / 2) * Globals.CELL_HEIGHT + game.player.width
    game.scene.add_sprite("player", game.player)
    game.physics_engine = arc.PhysicsEngineSimple(game.player, game.scene.get_sprite_list("cells"))

    game.scene.add_sprite_list_after("bots", "player")

    # bots
    bot = BasicBot(walls=game.scene["cells"], track_points=game.track_points)
    bot.center_x = 2 * Globals.CELL_WIDTH
    bot.center_y = (Globals.GRID_HEIGHT / 2) * Globals.CELL_HEIGHT - bot.width
    game.scene.add_sprite("bots", bot)
    bot_physics = arc.PhysicsEngineSimple(bot, game.scene.get_sprite_list("cells"))
    game.bot_physics.append(bot_physics)

    game.scene.add_sprite_list_after("powerups", "bots")

    game.camera = arcade.Camera(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
    game.gui_camera = arcade.Camera(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)


def load_track(game):
    for r in range(len(game.grid)):
        for c in range(len(game.grid[0])):
            if game.grid[r][c] == 1:
                r_shade = get_shade(r, c, color_range=Globals.R_CELL_COLOR_RANGE)
                g_shade = get_shade(r, c, color_range=Globals.G_CELL_COLOR_RANGE)
                c_shade = get_shade(r, c, color_range=Globals.B_CELL_COLOR_RANGE)
                cell = arc.SpriteSolidColor(width=int(Globals.CELL_WIDTH), height=int(Globals.CELL_HEIGHT),
                                            color=(r_shade, g_shade, c_shade))
                cell.center_x = c * Globals.CELL_WIDTH + Globals.GRID_BL_POS[0]
                cell.center_y = r * Globals.CELL_HEIGHT + Globals.GRID_BL_POS[1]
                game.scene.add_sprite("cells", cell)


def setup_level(game):
    game.scene = arc.Scene()
    game.scene.add_sprite_list("cells", use_spatial_hash=True)
    game.grid = generate_random_grid(Globals.GRID_WIDTH, Globals.GRID_HEIGHT)

    for r in range(len(game.grid)):
        for c in range(len(game.grid[0])):
            if game.grid[r][c] == 1:
                cell = arc.SpriteSolidColor(width=Globals.CELL_WIDTH, height=Globals.CELL_HEIGHT, color=arc.color.BLUE)
                cell.center_x = c * Globals.CELL_WIDTH + Globals.GRID_BL_POS[0]
                cell.center_y = r * Globals.CELL_HEIGHT + Globals.GRID_BL_POS[1]
                game.scene.add_sprite("cells", cell)


def update_level(game):
    game.grid = run_sim(1, game.grid)

    game.scene.get_sprite_list("cells").clear()
    for r in range(len(game.grid)):
        for c in range(len(game.grid[0])):
            if game.grid[r][c] == 1:
                cell = arc.SpriteSolidColor(width=Globals.CELL_WIDTH, height=Globals.CELL_HEIGHT, color=arc.color.BLUE)
                cell.center_x = c * Globals.CELL_WIDTH + Globals.GRID_BL_POS[0]
                cell.center_y = r * Globals.CELL_HEIGHT + Globals.GRID_BL_POS[1]
                game.scene.add_sprite("cells", cell)
