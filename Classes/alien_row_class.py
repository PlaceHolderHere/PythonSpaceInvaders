from Classes.alien_class import Alien


class AlienRow:
    def __init__(self, start_x, row_y, alien_sprite, bullet_sprite, movement_trigger, spacing, row_length,
                 movement_delay):
        self.start_x = start_x
        self.start_y = row_y
        self.movement_trigger = movement_trigger
        self.spacing = spacing
        self.row_length = row_length
        self.movement_delay = movement_delay
        self.aliens = [Alien(start_x + (i * spacing), row_y, alien_sprite,
                             movement_delay, movement_trigger, bullet_sprite)
                       for i in range(row_length)]

    def blit(self, win):
        for alien in self.aliens:
            if alien.alive:
                alien.blit(win)

    def move_down(self):
        for alien in self.aliens:
            if alien.alive:
                alien.move_down()

    def update_movement_trigger(self, updated_value):
        for alien in self.aliens:
            if alien.alive:
                alien.movement_trigger = updated_value

    def reset(self):
        for alien_index, alien in enumerate(self.aliens):
            alien.alive = True
            alien.x = self.start_x + (alien_index * self.spacing)
            alien.y = self.start_y
            alien.movement_trigger = self.movement_trigger
            alien.movement_timer = self.movement_delay
