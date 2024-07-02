import pygame
from random import randrange as rnd
from math import sqrt
from time import sleep
import sys
import json
import os

def detect_collision(dx,dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    
    return dx, dy

font_size = 20

width, height = 1200, 900
fps = 60

paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 20
ball_speed = 6
ball_rect = int(sqrt(ball_radius * 2))
ball = pygame.Rect(rnd(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
dx, dy = 1, -1

score = 0

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

game_moment = True

LEVEL = 1

pygame.init()
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


sc.fill(pygame.Color('Black'))
word = 'LEVEl ' + str(LEVEL)

font = pygame.font.SysFont('stxingkai', font_size * 4)
text = font.render(word, True, pygame.Color('white'))
text_rect = text.get_rect()

text_x = sc.get_width() / 2 - text_rect.width / 2
text_y = sc.get_height() / 2 - text_rect.height / 2

sc.blit(text, (text_x, text_y))

pygame.display.flip()

sleep(2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if os.stat("all_score.json").st_size == 0:
                with open("send.json", "w+") as file2:
                    file2.write("[]")
            with open("all_score.json", "r") as file:
                l = list(json.load(file))
            l.append(score)
            with open("all_score.json", "w+") as file:
                json.dump(l, file,ensure_ascii=True)
            
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if os.stat("all_score.json").st_size == 0:
                with open("send.json", "w+") as file2:
                    file2.write("[]")
            with open("all_score.json", "r") as file:
                l = list(json.load(file))
            l.append(score)
            with open("all_score.json", "w+") as file:
                json.dump(l, file,ensure_ascii=True)

            fps = 60

            paddle_w = 330
            paddle_h = 35
            paddle_speed = 15
            paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)

            ball_radius = 20
            ball_speed = 6
            ball_rect = int(sqrt(ball_radius * 2))
            ball = pygame.Rect(rnd(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
            dx, dy = 1, -1

            block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
            color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

            score = 0

    sc.fill(pygame.Color('black'))
    
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]

    pygame.draw.rect(sc, pygame.Color('orange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_radius or ball.centerx > width - ball_radius:
        dx = -dx
    elif ball.centery < ball_radius:
        dy = -dy
    elif ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
    
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)

        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)

        score += 1

        fps += 2

    with open("all_score.json", "r") as file:
        l = list(json.load(file))


    high_score = "High score: " + str(max(l))
    word_score = "Score: " + str(score)

    font_score = pygame.font.SysFont('stxingkai', font_size * 2)
    
    text_score = font_score.render(word_score, True, pygame.Color('orange'))
    text_high_score = font_score.render(high_score, True, pygame.Color('orange'))

    text_score_x = 0
    text_score_y = sc.get_height() / 2
    text_high_score_y = sc.get_height() / 2 + font_size * 2

    sc.blit(text_score, (text_score_x, text_score_y))
    sc.blit(text_high_score, (text_score_x, text_high_score_y))
    
    if ball.bottom > height:
        sc.fill(pygame.Color('black'))

        word = 'GAME OVER!'
        word1= 'Нажмите ПРОБЕЛ для продолжения'

        font1 = pygame.font.SysFont('stxingkai', font_size)
        font = pygame.font.SysFont('stxingkai', font_size * 4)

        
        text2 = font1.render(word1, True, pygame.Color('white'))
        text = font.render(word, True, pygame.Color('white'))

        text_rect = text.get_rect()
        text_rect1 = text2.get_rect()

        text_x = sc.get_width() / 2 - text_rect.width / 2
        text_y = sc.get_height() / 2 - text_rect.height / 2
        text_x1 = (sc.get_width() / 2 - text_rect1.width / 2)
        text_y1 = (sc.get_height() / 2 - text_rect1.height / 2) + 60
        
        sc.blit(text, (text_x, text_y))
        sc.blit(text2, (text_x1, text_y1))

        game_moment = False

        pygame.display.flip()

    elif not len(block_list):
        ball_speed = 0
        
        LEVEL += 1

        if LEVEL == 10:
            sc.fill(pygame.Color('black'))

            word = 'YOU WIN!'
            word1= 'Нажмите ПРОБЕЛ для продолжения'

            font1 = pygame.font.SysFont('stxingkai', font_size)
            font = pygame.font.SysFont('stxingkai', font_size * 4)

            
            text2 = font1.render(word1, True, pygame.Color('white'))
            text = font.render(word, True, pygame.Color('white'))

            text_rect = text.get_rect()
            text_rect1 = text2.get_rect()

            text_x = sc.get_width() / 2 - text_rect.width / 2
            text_y = sc.get_height() / 2 - text_rect.height / 2
            text_x1 = (sc.get_width() / 2 - text_rect1.width / 2)
            text_y1 = (sc.get_height() / 2 - text_rect1.height / 2) + 60
            
            sc.blit(text, (text_x, text_y))
            sc.blit(text2, (text_x1, text_y1))

            pygame.display.flip()
        else:
            sc.fill(pygame.Color('Black'))
            word = 'LEVEl' + str(LEVEL)

            font = pygame.font.SysFont('stxingkai', font_size * 4)
            text = font.render(word, True, pygame.Color('white'))

            text_rect = text.get_rect()

            text_x = sc.get_width() / 2 - text_rect.width / 2
            text_y = sc.get_height() / 2 - text_rect.height / 2

            sc.blit(text, (text_x, text_y))
            
            fps = 60

            paddle_w = 330
            paddle_h = 35
            paddle_speed = 15
            paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)

            ball_radius = 20
            ball_speed = 6 + LEVEL
            ball_rect = int(sqrt(ball_radius * 2))
            ball = pygame.Rect(rnd(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
            dx, dy = 1, -1

            block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4 + (LEVEL - 1))]
            color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4 + (LEVEL - 1))]

            pygame.display.flip()

            sleep(2)




    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    elif key[pygame.K_RIGHT] and paddle.right < width:
        paddle.right += paddle_speed

    pygame.display.update()
    clock.tick(fps)
