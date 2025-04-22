class Player:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.size_x = sprite.get_width()
        self.size_y = sprite.get_height()
        self.move_left = False
        self.move_right = False
        self.alive = True
        self.lives = 3

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def move(self):
        # Moving
        if self.move_right:
            self.x += 5
        if self.move_left:
            self.x -= 5
