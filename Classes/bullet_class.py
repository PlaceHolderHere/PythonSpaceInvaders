from pygame import Rect


class Bullet:
    def __init__(self, x, y, vel_y, sprite):
        self.x = x
        self.y = y
        self.vel_y = vel_y
        self.sprite = sprite
        self.size_x = sprite.get_width()
        self.size_y = sprite.get_height()

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.y += self.vel_y

    def is_colliding(self, collide_rect):
        self_rect = Rect(self.x, self.y, self.size_x, self.size_y)
        return self_rect.colliderect(collide_rect)
