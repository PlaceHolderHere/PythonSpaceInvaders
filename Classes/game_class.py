from Classes.player_class import Player
from Classes.alien_block_class import AlienBlock
from Classes.fortress_class import Fortress
from Classes.button_class import Button
import pygame
import random


def draw_text(win, text_x, text_y, msg, color):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 35)
    text = font.render(f'{str(msg)}', False, color)
    text_rect = text.get_rect(center=(text_x, text_y))

    win.blit(text, text_rect)


def get_lower_bound(lower_x, upper_x, block_size):
    return max(0, (upper_x - lower_x) // block_size)


def get_upper_bound(lower_x, upper_x, block_size, max_output):
    return min(max_output, (upper_x - lower_x) // block_size + 1)


class Game:
    def __init__(self):
        # CONSTANTS
        self.SCREEN_HEIGHT = 800
        self.SCREEN_WIDTH = 764
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.MIN_ALIEN_FIRING_CHANCE = 10
        self.MIN_ALIEN_MOVEMENT_TRIGGER = 40
        self.FPS = 60

        # Variables
        self.running = True
        self.score = 0
        self.level = 1
        self.current_menu = 'HOME'
        self.aliens_move_down = False
        self.new_level_animation_cooldown = 0
        self.new_level_animation_counter = 0
        self.new_level_blit_animation = False

        # Pygame Init
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Space Invaders by PlaceHolderHere")
        self.WIN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # SFX
        self.player_fire_SFX = pygame.mixer.Sound("SFX/player_fire.wav")
        self.player_death_SFX = pygame.mixer.Sound("SFX/player_death.wav")
        self.alien_death_SFX = pygame.mixer.Sound("SFX/alien_death.wav")

        # Sprites
        self.player_sprite = pygame.image.load('Sprites/Player.png')
        self.player_life_icon = pygame.transform.scale(self.player_sprite, (48, 48))
        self.player_bullet_sprite = pygame.image.load('Sprites/bullet.png')
        self.alien_sprite1 = pygame.image.load('Sprites/enemy1.png')
        self.alien_sprite2 = pygame.image.load('Sprites/enemy2.png')
        self.alien_sprite3 = pygame.image.load('Sprites/enemy3.png')
        self.alien_sprite4 = pygame.image.load('Sprites/enemy4.png')
        self.alien_bullet = pygame.image.load('Sprites/enemy_bullet.png')
        self.alien_sprites = (self.alien_sprite4, self.alien_sprite3, self.alien_sprite2, self.alien_sprite1,
                              self.alien_sprite1)

        # Buttons
        self.play_button = Button(382, 302, pygame.image.load("Buttons/Play.png"))
        self.controls_button = Button(382, 400, pygame.image.load("Buttons/Controls.png"))
        self.main_menu_button = Button(382, 124, pygame.image.load("Buttons/Main Menu.png"))
        self.resume_button = Button(382, 222, pygame.image.load("Buttons/Resume.png"))
        self.restart_button = Button(382, 320, pygame.image.load("Buttons/Restart.png"))
        self.quit_button = Button(382, 400, pygame.image.load("Buttons/Quit.png"))
        self.main_menu_defeat_button = Button(382, 352, pygame.image.load("Buttons/Main Menu.png"))
        self.retry_Button = Button(382, 448, pygame.image.load("Buttons/Retry.png"))

        # Game Objects
        self.player = Player(30, self.SCREEN_HEIGHT - 70, self.player_sprite, self.player_bullet_sprite)
        self.aliens = AlienBlock(60, ([100 + i * 70 for i in range(5)]), self.alien_sprites, self.alien_bullet, 90, 70,
                                 9, 1500)
        self.fortresses = [Fortress(75 + (i * 223), 550, 3) for i in range(3)]

    def process_key_binds(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN and self.current_menu == 'GAME':
                if event.key == pygame.K_s:
                    self.player.move_right = True
                elif event.key == pygame.K_a:
                    self.player.move_left = True
                elif event.key == pygame.K_SPACE:
                    if self.player.shoot():
                        self.player_fire_SFX.play()
                elif event.key == pygame.K_ESCAPE:
                    self.current_menu = 'PAUSED'

            elif event.type == pygame.KEYUP and self.current_menu == 'GAME':
                if event.key == pygame.K_s:
                    if self.player.alive:
                        self.player.move_right = False
                elif event.key == pygame.K_a:
                    if self.player.alive:
                        self.player.move_left = False

    def render_home_menu(self):
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 160, "Space Invaders by PlaceHolderHere", self.WHITE)

        # Buttons
        self.play_button.blit(self.WIN)
        self.controls_button.blit(self.WIN)

        if self.play_button.is_clicked():
            self.current_menu = 'GAME'

        elif self.controls_button.is_clicked():
            self.current_menu = 'CONTROLS'

    def render_controls_menu(self):
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 224, "Controls:", self.WHITE)
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 288, "A: Left", self.WHITE)
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 352, "S: Right", self.WHITE)
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 416, "Space: Shoot", self.WHITE)
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 480, "Escape: Pause", self.WHITE)

        self.main_menu_button.blit(self.WIN)
        if self.main_menu_button.is_clicked():
            self.current_menu = 'HOME'

    def player_respawn_animation(self):
        self.player.respawn_cooldown -= 1
        self.player.respawn_animation_counter += 1
        if self.player.respawn_animation_counter > 5:
            self.player.respawn_animation_counter = 0
            self.player.respawn_blit = not self.player.respawn_blit

        if self.player.respawn_blit:
            self.player.blit(self.WIN)

    def new_level_animation(self):
        self.new_level_animation_cooldown -= 1
        self.new_level_animation_counter += 1
        if self.new_level_animation_counter > 10:
            self.new_level_animation_counter = 0
            self.new_level_blit_animation = not self.new_level_blit_animation

        if self.new_level_blit_animation:
            self.player.blit(self.WIN)
            self.aliens.blit(self.WIN)
            for fort in self.fortresses:
                fort.blit(self.WIN)

    def border_collision(self, x, size_x):
        if x < 30:
            return {'collided': True, 'x': 30}
        elif x + size_x > self.SCREEN_WIDTH - 30:
            return {'collided': True, 'x': self.SCREEN_WIDTH - size_x - 30}
        return {'collided': False, 'x': x}

    def fortress_blast_collisions(self, bullet):
        for fort in self.fortresses:
            if bullet.is_colliding(fort.get_fortress_rect()):
                fort_shape = fort.shape
                lower_bullet_x_range = get_lower_bound(fort.x, bullet.x, fort.rect_size)
                upper_bullet_x_range = get_upper_bound(fort.x, bullet.x + bullet.size_x, fort.rect_size, fort.num_cols)
                for row_index in range(fort.num_rows - 1, 0, -1):
                    for col_index in range(lower_bullet_x_range, upper_bullet_x_range):
                        if fort_shape[row_index][col_index] == '1':
                            collide_x = fort.x + (col_index * fort.rect_size)
                            collide_y = fort.y + (row_index * fort.rect_size)
                            collide_block_rect = pygame.Rect(collide_x, collide_y, fort.rect_size, fort.rect_size)
                            if bullet.is_colliding(collide_block_rect):
                                blast_x = collide_x - bullet.blast_radius
                                blast_y = collide_y - bullet.blast_radius
                                blast_size_x = blast_x - fort.x
                                blast_size_y = blast_y - fort.y

                                # Blast Ranges
                                blast_lower_x_range = max(0, blast_size_x // fort.rect_size)
                                blast_upper_x_range = min(fort.num_cols, (
                                            blast_size_x + (2 * bullet.blast_radius)) // fort.rect_size + 1)

                                blast_lower_y_range = max(0, blast_size_y // fort.rect_size)
                                blast_upper_y_range = min(fort.num_rows, (
                                            blast_size_y + (2 * bullet.blast_radius)) // fort.rect_size + 1)

                                blast_x_range = range(blast_lower_x_range, blast_upper_x_range)
                                blast_y_range = range(blast_lower_y_range, blast_upper_y_range)

                                # Blast Radius Collisions
                                for blast_row_index in blast_y_range:
                                    for blast_col_index in blast_x_range:
                                        if fort_shape[blast_row_index][blast_col_index] == '1':
                                            x = fort.x + (blast_col_index * fort.rect_size)
                                            y = fort.y + (blast_row_index * fort.rect_size)
                                            if bullet.blast_calculation(collide_x, collide_y, x, y, fort.rect_size):
                                                fort_shape[blast_row_index][blast_col_index] = '0'

                                return {'collided': True}
        return {'collided': False}

    def process_player_bullet(self, bullet):
        bullet.move()
        if bullet.is_off_screen():
            return {'collided': True}

        # Other Bullet Collisions
        for row in self.aliens.alien_rows:
            for alien in row.aliens:
                if alien.alive:
                    if bullet.is_colliding(alien.get_rect()):
                        alien.alive = False
                        self.aliens.num_alive_aliens -= 1
                        self.score += 10
                        self.alien_death_SFX.play()
                        return {'collided': True}

        output = self.fortress_blast_collisions(bullet)
        bullet.blit(self.WIN)
        return output

    def game_reset(self):
        self.aliens_move_down = False
        self.new_level_animation_cooldown = 0
        self.new_level_animation_counter = 0
        self.new_level_blit_animation = False

        self.score = 0
        self.level = 1
        self.player.lives = 3
        self.player.reset(30, self.SCREEN_HEIGHT - 70)
        self.aliens.reset()
        for fortress in self.fortresses:
            fortress.reset_fortress()

    def render_game_menu(self):
        # HUD
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 40, self.score, self.WHITE)
        for life_index in range(self.player.lives):
            self.WIN.blit(self.player_life_icon, ((life_index * 56) + 56, 16))

        # Player Respawn Animation
        if self.player.respawn_cooldown > 0:
            self.player_respawn_animation()

        # New Level Animation
        elif self.new_level_animation_cooldown > 0:
            self.new_level_animation()

        # Player Processing
        else:
            if self.player.respawning:
                self.player.respawning = False
                self.player.reset(30, self.SCREEN_HEIGHT - 70)

            elif not self.player.alive:
                if self.player.lives < 0:
                    self.current_menu = 'DEAD'
                else:
                    self.aliens.clear_bullets()
                    self.player.alive = True
                    self.player.respawning = True
                    self.player.respawn_cooldown = 120
                    self.player.lives -= 1

            # Player Processing
            else:
                self.player.move()
                self.player.x = self.border_collision(self.player.x, self.player.size_x)['x']
                self.player.blit(self.WIN)

                for bullet_index, bullet in enumerate(self.player.bullets):
                    if self.process_player_bullet(bullet)['collided']:
                        self.player.bullets.pop(bullet_index)

            # Level Reset
            if self.aliens.num_alive_aliens <= 0:
                self.player.bullets.clear()
                self.new_level_animation_cooldown = 120
                self.level += 1
                self.aliens.global_firing_chance = max(self.MIN_ALIEN_FIRING_CHANCE,
                                                       self.aliens.global_firing_chance - (self.level * 10))
                self.aliens.movement_trigger = max(self.MIN_ALIEN_MOVEMENT_TRIGGER,
                                                   self.aliens.movement_trigger - ((self.level // 5) * 5))
                self.aliens.reset()
                # Fortress Reset
                for fortress in self.fortresses:
                    fortress.reset_fortress()

            # Alien Processing
            if self.aliens_move_down:
                self.aliens_move_down = False
                self.aliens.move_down()

            for alien_row_index, row in enumerate(self.aliens.alien_rows):
                for alien in row.aliens:
                    if alien.alive:
                        if alien.y > self.player.y:
                            self.current_menu = 'DEAD'

                        elif alien_row_index == 0:  # Topmost row of aliens
                            if self.border_collision(alien.x, alien.size_x)['collided']:
                                self.aliens_move_down = True

                        # Alien Firing
                        elif not alien.bullet_fired:
                            num_dead_aliens = self.aliens.TOTAL_NUM_ALIENS - self.aliens.num_alive_aliens
                            firing_chance = max(self.MIN_ALIEN_FIRING_CHANCE,
                                                self.aliens.global_firing_chance - (num_dead_aliens * 5))
                            if random.randint(0, firing_chance) == 0:
                                alien.shoot()

                    # Alien bullet processing
                    if alien.bullet_fired:
                        alien.bullet.move()
                        if alien.bullet.y > self.SCREEN_HEIGHT:
                            alien.bullet_fired = False
                        else:
                            # Player Collisions
                            if alien.bullet.is_colliding(self.player.get_rect()):
                                self.player.alive = False
                                alien.bullet_fired = False
                                self.player_death_SFX.play()

                            # Fortress Collisions
                            if self.fortress_blast_collisions(alien.bullet)['collided']:
                                alien.bullet_fired = False

                        alien.bullet.blit(self.WIN)
            self.aliens.blit(self.WIN)
            for fortress in self.fortresses:
                fortress.blit(self.WIN)

    def render_paused_game_menu(self):
        self.main_menu_button.blit(self.WIN)
        self.resume_button.blit(self.WIN)
        self.restart_button.blit(self.WIN)
        self.quit_button.blit(self.WIN)

        if self.main_menu_button.is_clicked():
            self.game_reset()
            self.current_menu = 'HOME'
            return True

        elif self.resume_button.is_clicked():
            self.current_menu = 'GAME'
            return True

        elif self.restart_button.is_clicked():
            self.game_reset()
            self.current_menu = 'GAME'
            return True

        elif self.quit_button.is_clicked():
            self.running = False
            return True

    def render_game_over_menu(self):
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 220, "GAME OVER", self.RED)
        draw_text(self.WIN, self.SCREEN_WIDTH // 2, 280, f"Final Score: {self.score}", self.WHITE)

        # Buttons
        self.main_menu_defeat_button.blit(self.WIN)
        self.retry_Button.blit(self.WIN)
        if self.main_menu_defeat_button.is_clicked():
            self.game_reset()
            self.current_menu = 'HOME'
        elif self.retry_Button.is_clicked():
            self.game_reset()
            self.current_menu = 'GAME'

    def update(self):
        pygame.time.Clock().tick(self.FPS)
        self.process_key_binds()
        self.WIN.fill((0, 0, 0))

        if self.current_menu == 'HOME':
            self.render_home_menu()

        elif self.current_menu == 'CONTROLS':
            self.render_controls_menu()

        elif self.current_menu == 'GAME':
            self.render_game_menu()

        elif self.current_menu == 'PAUSED':
            self.render_paused_game_menu()

        elif self.current_menu == 'DEAD':
            self.render_game_over_menu()

        pygame.display.update()
