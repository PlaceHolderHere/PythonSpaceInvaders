import pygame


class Button:
    def __init__(self, center_x, center_y, image):
        self.transparency = 200
        self.clicked = False
        self.image = image
        self.x = center_x - (image.get_width() // 2)
        self.y = center_y - (image.get_height() // 2)
        self.rect = pygame.rect.Rect(self.x, self.y, image.get_width(), image.get_height())

    def blit(self, win):
        self.image.set_alpha(self.transparency)
        win.blit(self.image, self.rect)

    def is_clicked(self):
        if self.mouse_is_hovering():
            if pygame.mouse.get_pressed()[0] == 1:
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
