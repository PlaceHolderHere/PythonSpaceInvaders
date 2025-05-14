from Classes.bullet_class import Bullet
from pygame import Rect


class Player:
    def __init__(self, x, y, sprite, bullet_sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.size_x = sprite.get_width()
        self.size_y = sprite.get_height()
        self.bullet_sprite = bullet_sprite
        self.move_left = False
        self.move_right = False
        self.alive = True
        self.lives = 3
        self.bullets = []
        self.firing_cooldown = 30
        self.firing_speed = 30

    def blit(self, win):
        self.firing_cooldown += 1
        if self.firing_cooldown >= self.firing_speed:
            self.firing_cooldown = self.firing_speed
        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        # Moving
        if self.move_right:
            self.x += 5
        if self.move_left:
            self.x -= 5

    def shoot(self):
        if self.firing_cooldown >= self.firing_speed:
            self.firing_cooldown = 0
            self.bullets.append(
                Bullet(self.x + (self.size_x // 2) - (self.bullet_sprite.get_width() // 2), self.y, -10,
                       self.bullet_sprite))

    def get_rect(self):
        return Rect(self.x, self.y, self.size_x, self.size_y)
