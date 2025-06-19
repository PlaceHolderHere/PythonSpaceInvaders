import pygame


class Fortress:
    def __init__(self, start_x, start_y, rect_size):
        self.x = start_x
        self.y = start_y
        self.rect_size = rect_size
        self.shape = []
        self.reset_fortress()
        self.size_x = len(self.shape[0]) * self.rect_size
        self.size_y = len(self.shape) * self.rect_size
        self.num_rows = len(self.shape)
        self.num_cols = len(self.shape[0])
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def blit(self, win):
        for row_index, row in enumerate(self.shape):
            for block_index, block in enumerate(row):
                if block == '1':
                    pygame.draw.rect(win, (0, 255, 0), (
                        self.x + (self.rect_size * block_index), self.y + (self.rect_size * row_index),
                        self.rect_size, self.rect_size))

    def get_fortress_rect(self):
        return self.rect

    def reset_fortress(self):
        self.shape = []
        with open('fortress_shape.txt') as fortress:
            for row in fortress:
                fort_row = list(row)
                self.shape.append(fort_row[0:len(fort_row) - 1])
