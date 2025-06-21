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

    def update(self):
        pygame.time.Clock().tick(self.FPS)
        self.process_key_binds()
        self.WIN.fill((0, 0, 0))

        if self.current_menu == 'HOME':
            self.render_home_menu()

        elif self.current_menu == 'CONTROLS':
            self.render_controls_menu()

        pygame.display.update()
