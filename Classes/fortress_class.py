import pygame


class Fortress:
    def __init__(self, start_x, start_y, rect_size):
        self.start_x = start_x
        self.start_y = start_y
        self.rect_size = rect_size
        self.fortress = []
        self.reset_fortress()
        self.size_x = len(self.fortress[0]) * self.rect_size
        self.size_y = len(self.fortress) * self.rect_size
        self.num_rows = len(self.fortress)
        self.num_cols = len(self.fortress[0])
        self.rect = pygame.Rect(self.start_x, self.start_y, self.size_x, self.size_y)

    def blit(self, win):
        for row_index, row in enumerate(self.fortress):
            for block_index, block in enumerate(row):
                if block == '1':
                    pygame.draw.rect(win, (0, 255, 0), (
                        self.start_x + (self.rect_size * block_index), self.start_y + (self.rect_size * row_index),
                        self.rect_size, self.rect_size))

    def get_fortress_rect(self):
        return self.rect

    def reset_fortress(self):
        self.fortress = []
        with open('fortress_shape.txt') as fortress:
            for row in fortress:
                fort_row = list(row)
                self.fortress.append(fort_row[0:len(fort_row) - 1])
