import pygame


class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.transparency = 200
        self.clicked = False
        self.button_cooldown = 0
        self.image = image
        self.rect = pygame.rect.Rect(x, y, image.get_width(), image.get_height())

    def draw(self, win):
        self.image.set_alpha(self.transparency)
        win.blit(self.image, self.rect)

    def is_clicked(self):
        if self.mouse_is_hovering():
            if pygame.mouse.get_pressed()[0] == 1 and self.button_cooldown <= 0:
                self.button_cooldown = 15
                return True

            else:
                return False

    def mouse_is_hovering(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            self.transparency = 255
            return True
        else:
            self.transparency = 200
            return False
