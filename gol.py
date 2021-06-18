import pygame
import random
from collections import namedtuple
import numpy as np

pygame.init()

Point = namedtuple('Point', ['x', 'y'])
SPEED = 1000

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class GOL:
    def __init__(self, w=640, h=480):
        self.BLOCK_SIZE = 32

        self.w = w
        self.h = h

        self.ROWS = self.w//self.BLOCK_SIZE
        self.COLS = self.h//self.BLOCK_SIZE

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()
        self.grid = np.zeros([self.ROWS, self.COLS], dtype=np.bool8)
        self.activate(2, 13)
        self.activate(3, 13)
        self.activate(4, 13)
        self.activate(4, 12)
        self.activate(3, 11)

    def activate(self, x, y):
        self.grid[x, y] = True

    def draw_block(self, x, y):
        rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
        pygame.draw.rect(self.display, BLUE1, rect)

    def _update_ui(self):
        self.display.fill(BLACK)

        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x, y] == True:
                    self.draw_block(x, y)

        pygame.display.flip()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._update_ui()
        self.clock.tick(SPEED)
        self.generate()
        return False

    def generate(self):
        self.fix_scale()
        new_grid = self.grid.copy()
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                count_live_neighbours = self.get_count_live_neighbours(x, y)
                if self.grid[x, y] == True:
                    if count_live_neighbours == 2 or count_live_neighbours == 3:
                        pass #Continue living
                    elif count_live_neighbours < 2:
                        new_grid[x, y] = False #Underpopulation
                    elif count_live_neighbours > 3:
                        new_grid[x, y] = False #Overpopulation
                else:
                    if count_live_neighbours == 3:
                        new_grid[x, y] = True #Reproduction
        self.grid = new_grid

    def get_count_live_neighbours(self, x, y):
        neighbours = 0
        DIRS = [(0, 1), (1, 1), (1, 0), (1, -1), (0,-1),(-1, -1), (-1,0), (-1, 1)]
        for d in DIRS:
            new_x = x + d[0]
            new_y = y + d[1]
            if new_x >= 0 and new_x < self.grid.shape[0] \
                    and new_y >= 0 and new_y < self.grid.shape[1] \
                    and self.grid[new_x, new_y] == True:
                neighbours = neighbours + 1

        return neighbours

    def fix_scale(self):
        if self.does_corner_exists():
            if self.BLOCK_SIZE == 1:
                print("Can't zoom out any further")
                pygame.quit()
                quit()

            self.BLOCK_SIZE = self.BLOCK_SIZE // 2

            prev_rows = self.ROWS
            prev_cols = self.COLS

            self.ROWS = self.ROWS * 2
            self.COLS = self.COLS * 2

            new_grid = np.zeros([self.ROWS, self.COLS], dtype=np.bool8)

            start_row = prev_rows // 2
            end_row = start_row + prev_rows

            start_col = prev_cols // 2
            end_col = start_col + prev_cols

            new_grid[start_row:end_row, start_col :end_col] = self.grid
            self.grid = new_grid


    def does_corner_exists(self):
        corner_y = self.COLS - 1
        corner_x = self.ROWS - 1
        
        for x in range(self.ROWS):
            if self.grid[x,0] == True or self.grid[x, corner_y] == True:
                return True
            
        for y in range(self.COLS):
            if self.grid[0,y] == True or self.grid[corner_x, y] == True:
                return True
    
        return False