import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 250)
COLOR_RED = (255, 0, 0)

# Створення основного вікна гри
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Завантаження фону та інших зображень
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

# Ініціалізація розмірів та руху головного героя
player = pygame.image.load('player.png').convert_alpha()
player_size = player.get_size()
player_rect = player.get_rect()
player_rect.centery = main_display.get_rect().centery
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

# Функції для створення ворогів та бонусів
def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, 
                             random.randint(enemy.get_height(), HEIGHT - enemy.get_height()), 
                             *enemy.get_size())
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha() 
    bonus_width = bonus.get_width()
    bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width), 
                             -bonus.get_height(), 
                             *bonus.get_size())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

# Задання кастомних подій pygame
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True

# Головний цикл гри
while playing:
    # Встановлення кадрової частоти гри
    FPS.tick(120)

    # Обробка подій pygame
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    # Переміщення фону
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    # Виведення фону на екран
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    # Обробка натискання клавіш для руху гусенята
    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    # Обробка колізій з ворогами
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            # Гравець зіткнувся з ворогом, гра закінчилась
            game_over = True
            if game_over:
                game_over_font = pygame.font.SysFont('Verdana', 60)
                game_over_text = game_over_font.render('GAME OVER!', True, COLOR_BLACK)
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                main_display.blit(game_over_text, text_rect)

                # Виведення рахунку гравця
                score_font = pygame.font.SysFont('Verdana', 40)
                score_text = score_font.render('Your score: ' + str(score) + ' points!', True, COLOR_BLACK)
                score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                main_display.blit(score_text, score_rect)

                pygame.display.flip()
                pygame.time.delay(3000)
                playing = False

    # Обробка колізій з бонусами
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            # Гравець зібрав бонус, отримує очки
            score += 1
            bonuses.pop(bonuses.index(bonus))

    # Виведення рахунку на екран
    main_display.blit(FONT.render('Score: ' + str(score), True, COLOR_BLACK), (WIDTH-150, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    # Видалення ворогів та бонусів, які вийшли за межі вікна
    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

