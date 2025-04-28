import pygame


class Fortress:
    def __init__(self, start_x, start_y, rect_size):
        self.start_x = start_x
        self.start_y = start_y
        self.rect_size = rect_size
        self.fortress_shape = [[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                               ]
        self.fortress = []

    def blit(self, win):
        for row_index, row in enumerate(self.fortress_shape):
            for block_index, block in enumerate(row):
                if block == 1:
                    pygame.draw.rect(win, (0, 255, 0), (
                        self.start_x + (self.rect_size * block_index), self.start_y + (self.rect_size * row_index),
                        self.rect_size, self.rect_size))
