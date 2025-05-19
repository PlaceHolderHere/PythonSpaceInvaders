from Classes.bullet_class import Bullet
from pygame import Rect


class Alien:
    def __init__(self, x, y, sprite, movement_delay, movement_trigger, bullet_sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.size_x = sprite.get_width()
        self.size_y = sprite.get_height()
        self.x_vel = 12
        self.movement_timer = movement_delay
        self.movement_trigger = movement_trigger
        self.alive = True
        self.bullet_fired = False
        self.bullet = Bullet(x, -200, 0, bullet_sprite)

    def blit(self, win):
        self.movement_timer += 1
        if self.movement_timer >= self.movement_trigger:
            self.move()
            self.movement_timer = 0

        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.x += self.x_vel

    def move_down(self):
        self.x_vel *= -1
        self.y += 12

    def shoot(self):
        self.bullet_fired = True
        self.bullet.x = self.x + (self.bullet.size_x // 2)
        self.bullet.y = self.y + self.bullet.size_y
        self.bullet.vel_y = 4

    def get_rect(self):
        return Rect(self.x, self.y, self.size_x, self.size_y)
