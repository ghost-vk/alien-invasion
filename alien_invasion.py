from time import sleep

import pygame
from pygame.sprite import Group

from button import Button
from settings import Settings
from game_stats import GameStats
from ship import Ship
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))

    pygame.display.set_caption("Alien Invasion")
    play_button = Button(settings, screen, "PLAY")

    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    ship = Ship(settings, screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(settings, screen, ship, aliens)

    while True:
        gf.check_events(settings, screen, stats, sb, play_button, ship, aliens,
                        bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(settings, stats, sb, screen, ship, aliens,
                             bullets)

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)
        sleep(0.01)

run_game()
