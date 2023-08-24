# functions and stuff for generation
import arcade

from Globals import *
from Misc_Functions import easy_randrange
from random import choice, randrange
from copy import deepcopy


def generate_track_grid(height, width):
    # creates starting track grid, 0 = dead cell 1 = alive cell
    grid = create_grid(height, width)
    grid, targets = track_kill(grid)
    return grid, targets


def generate_random_grid(width, height):
    # generates grid with random dead cells
    grid = create_grid(width, height)
    grid = random_kill(grid)
    return grid


def create_grid(width, height):
    grid = []

    # generate rows
    for w in range(width):
        grid.append([])
        # generate columns
        for h in range(height):
            grid[w].append(1)

    return grid


def random_kill(grid):
    rows = len(grid)
    columns = len(grid[0])
    # amount of cells to kill
    deaths = round(RANDOM_DEATH_PERCENT * (rows * columns))
    # choose random cells to kill
    for i in range(deaths):
        grid[randrange(0, rows, 1)][randrange(0, columns, 1)] = 0

    return grid


def track_kill(grid):
    rows = len(grid)
    mid_row = rows / 2
    columns = len(grid[0]) - 1

    # start area
    if type(mid_row) == float:
        mid_row = int(mid_row)
        row_range = (mid_row - 3, mid_row + 4)
        column_range = (0, 10)
        for r in range(row_range[0], row_range[1], 1):
            for current_column in range(column_range[0], column_range[1]):
                grid[r][current_column] = 0
    elif type(mid_row) == int:
        row_range = (mid_row - 3, mid_row + 3)
        column_range = (0, 10)
        for r in range(row_range[0], row_range[1], 1):
            for current_column in range(column_range[0], column_range[1]):
                grid[r][current_column] = 0
    else:
        column_range = (0, 10)

    usable_columns = columns - column_range[1]

    current_column = column_range[1]
    targets = []
    last_target = (int(mid_row), 0)
    for p in range(TRACK_KILL_POINT_AMOUNT + 1):
        # calculate where a point should be
        if p == 0:
            target_point = (int(mid_row), current_column)
        else:
            target_point = (randrange(2, rows - 2, 1), current_column)
        current_column += int(usable_columns/TRACK_KILL_POINT_AMOUNT)

        targets.append(target_point)
        # generate points on cell grid to create paths between
        for rr in range(-1, 1, 1):
            for rc in range(-1, 1, 1):
                grid[target_point[0] + rr][target_point[1] + rc] = 0

        # draw beginning lines between points
        # get slope of points
        slope = (target_point[0] - last_target[0])/(target_point[1] - last_target[1])
        # go through all Xs between points
        for x in range(last_target[1], target_point[1]):
            # calculate Y of point based on point-slope form
            point_y = (slope * (x - last_target[1])) + last_target[0]
            # delete cells in an area around and on the calculated point, randomly
            for delete_x in range(-5, 5):
                for delete_y in range(-5, 5):
                    # make sure point wont be outside of grid bounds
                    if (rows - 2) > (delete_y + int(point_y)) > 0 and columns > (x + delete_x) > 0:
                        death_chance = randrange(0, 100)
                        if (death_chance / 100) <= TRACK_KILL_DEATH_PERCENT:
                            grid[int(point_y) + delete_y][x + delete_x] = 0

        last_target = target_point

        # old generation
        '''''
        # randomly kill cells between the last point and the current one
        square_length = abs(target_point[0] - last_target[0])
        square_width = abs(target_point[1] - last_target[1])
        short_width = False
        short_length = False

        if square_width < 4:
            short_width = True
            square_width = 4

        if square_length < 4:
            short_length = True
            square_length = 4

        square_area = square_length * square_width

        death_amount = int(TRACK_KILL_DEATH_PERCENT * square_area)
        for i in range(death_amount):
            if short_length:
                kill_r = easy_randrange(last_target[0], (target_point[0] + randrange(-2, 2)))
            else:
                kill_r = easy_randrange(last_target[0], target_point[0])

            if short_width:
                kill_c = easy_randrange(last_target[1], (target_point[1] + randrange(-2, 2)))
            else:
                kill_c = easy_randrange(last_target[1], target_point[1])
            grid[kill_r][kill_c] = 0

        last_target = target_point
    '''''
    return grid, targets


# needs to check in a square around the cell for "alive" aka "1" neighbors
def count_alive_neighbors(cell, grid):
    neighbors = 0
    c_row = cell[0]
    c_column = cell[1]
    
    for r in range(-1, 2):
        for c in range(-1, 2):
            neighbor = ((c_row + r), (c_column + c))
            if r == 0 and c == 0:
                continue
            elif neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] > (len(grid) - 1) or neighbor[1] > (len(grid[0]) - 1):
                neighbors += 1
            elif grid[neighbor[0]][neighbor[1]] == 1:
                neighbors += 1

    return neighbors


def run_sim_step(grid):
    new_grid = deepcopy(grid)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            neighbors = count_alive_neighbors((r, c), grid)
            if grid[r][c] == 1:
                if neighbors > MAX_NEIGHBORS_DEATH or neighbors < MIN_NEIGHBORS_DEATH:
                    new_grid[r][c] = 0
            elif grid[r][c] == 0:
                if neighbors > MIN_NEIGHBORS_BIRTH:
                    new_grid[r][c] = 1

    return new_grid


def run_sim(step_num, grid):
    for i in range(step_num):
        grid = run_sim_step(grid)

    return grid


def generate_track(width=105, height=70):
    grid, targets = generate_track_grid(height, width)
    grid = run_sim(5, grid)
    return grid, targets
