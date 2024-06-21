import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_events_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events_keydown(event, game_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT: 
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_events(game_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_events_keydown(event, game_settings,
                                 screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_events_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)

def update_screen(game_settings, screen, stats, scoreboard, ship, aliens,
                  bullets, play_button):
    screen.fill(game_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(game_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullets_aliens_collisions(game_settings, screen, stats, sb, ship,
                                    aliens, bullets)

def fire_bullet(game_settings, screen, ship, bullets):
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(game_settings, screen, ship, aliens):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens(game_settings, alien_width)
    number_rows = get_number_rows(game_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number,
                         row_number)

def get_number_aliens(game_settings, alien_width):
    available_space_x = game_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def create_alien(game_settings, screen, aliens, alien_number, row_number):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(game_settings, ship_height, alien_height):
    available_space_y = (game_settings.screen_height - (3*alien_height) -
                         ship_height)
    number_rows = int(available_space_y / (2*alien_height)) 
    return number_rows

def update_aliens(game_settings, stats, sb, screen, ship, aliens, bullets):
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(game_settings, stats, sb, screen, ship, aliens,
                        bullets)

def check_fleet_edges(game_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break

def change_fleet_direction(game_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1

def check_bullets_aliens_collisions(game_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens,
                                            game_settings.bullets_disappear_on_collision,
                                            True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(game_settings, screen, ship, aliens)

def ship_hit(game_settings, stats, sb, screen, ship, aliens, bullets):
    if stats.ships_left <= 1:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        return

    stats.ships_left -= 1
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(game_settings, screen, ship, aliens)
    ship.center_ship()
    sleep(0.5)

def check_aliens_bottom(game_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, sb, screen, ship, aliens, bullets)
            break

def check_play_button(game_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        game_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        aliens.empty()
        bullets.empty()

        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
