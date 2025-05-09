from Classes.alien_row_class import AlienRow


# length of alien_sprites and y_values must be equal
class AlienBlock:
    def __init__(self, start_x, y_values, alien_sprites, bullet_sprite, movement_trigger, spacing, row_length,
                 global_firing_chance):
        self.start_x = start_x
        self.y_values = y_values
        self.movement_trigger = movement_trigger
        self.spacing = spacing
        self.global_firing_chance = global_firing_chance
        self.row_length = row_length
        self.TOTAL_NUM_ALIENS = row_length * len(y_values)
        self.num_alive_aliens = self.TOTAL_NUM_ALIENS
        self.alien_rows = [AlienRow(start_x, y_values[i], alien_sprites[i], bullet_sprite, movement_trigger, spacing,
                                    row_length, i * 10) for i in range(len(y_values))]

    def blit(self, win):
        for row in self.alien_rows:
            row.blit(win)

    def move_down(self):
        for row in self.alien_rows:
            row.move_down()

    def reset(self):
        for row_index, alien_row in enumerate(self.alien_rows):
            self.num_aliens = self.row_length * len(self.y_values)
            alien_row.movement_trigger = self.movement_trigger
            alien_row.reset()
