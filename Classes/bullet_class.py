from pygame import Rect


class Bullet:
    def __init__(self, x, y, vel_y, sprite):
        self.x = x
        self.y = y
        self.vel_y = vel_y
        self.sprite = sprite
        self.size_x = sprite.get_width()
        self.size_y = sprite.get_height()
        self.blast_radius = 8

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.y += self.vel_y

    def is_colliding(self, collide_rect):
        self_rect = Rect(self.x, self.y, self.size_x, self.size_y)
        return self_rect.colliderect(collide_rect)

    def blast_calculation(self, rect_x, rect_y, rect_width, rect_height):
        circle_x = self.x + (self.size_x // 2)
        circle_y = 0
        if self.vel_y < 0:
            circle_y = self.y

        elif self.vel_y > 0:
            circle_y = self.y + (self.size_y // 2)

        # Finds the closest corner to the circle's center
        closest_x = max(rect_x, min(circle_x, rect_x + rect_width))
        closest_y = max(rect_y, min(circle_y, rect_y + rect_height))

        x_difference = closest_x - circle_x
        y_difference = closest_y - circle_y

        # checks if difference from circle center to rectangle less than or equal to the radius
        return (x_difference ** 2 + y_difference ** 2) <= (self.blast_radius ** 2)  # Pythagorean's theorem
