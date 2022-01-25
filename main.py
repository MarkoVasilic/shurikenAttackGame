import numpy as np
import pygame
import numpy
import entities
import gjk

pygame.init()
screen = pygame.display.set_mode((800, 600))

# arrow coordinates
bottom1 = pygame.Vector2(398, 600)
bottom2 = pygame.Vector2(400, 600)
bottom3 = pygame.Vector2(402, 600)
middle1 = pygame.Vector2(392, 550)
middle2 = pygame.Vector2(398, 550)
middle3 = pygame.Vector2(402, 550)
middle4 = pygame.Vector2(408, 550)
topArrow = pygame.Vector2(400, 540)

# square coordinates
top_left = pygame.Vector2(370, 270)
top_right = pygame.Vector2(430, 270)
bottom_left = pygame.Vector2(370, 330)
bottom_right = pygame.Vector2(430, 330)

fire = False
running = True
ball_image = pygame.image.load('images/ball.png')
ball_image = pygame.transform.smoothscale(ball_image, (30, 30))
shuriken_image = pygame.image.load('images/shuriken.png')
shuriken_image = pygame.transform.smoothscale(shuriken_image, (30, 30))

entity_list = []
entity_list.append(entities.Square(top_left, top_right, bottom_left, bottom_right, [((5, 0), 30), ((-5,0), 30)], screen))
shuriken = entities.Shuriken(400, 600, (0, 0), screen)
ball = entities.Ball(400, 600, 10, (0, 0), screen)
clock = pygame.time.Clock()
select = "shuriken"
arrow = entities.Arrow(bottom1, bottom2, bottom3, middle1, middle2, middle3, middle4, topArrow, 0, screen)
entity_list.append(arrow)
projectile = -1
ticking = True
while running:

    screen.fill((255, 255, 255))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and fire == False:
                arrow.update_angle(-numpy.pi / 100)
            if event.key == pygame.K_RIGHT and fire == False:
                arrow.update_angle(numpy.pi / 100)
            if event.key == pygame.K_SPACE and fire == False:
                fire = True
            if event.key == pygame.K_1 and fire == False:
                select = "shuriken"
            if event.key == pygame.K_2 and fire == False:
                select = "ball"
            if event.key == pygame.K_r:
                fire = False
                entity_list.remove(projectile)
                projectile = -1
            if event.key == pygame.K_p:
                ticking = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                arrow.update_angle(0)
            if event.key == pygame.K_p:
                ticking = True
    if fire:
        top = arrow.getTop()
        bottom = arrow.getBottom()
        top[0] = top[0] - bottom[0]
        top[1] = top[1] - bottom[1]
        top = top / top.magnitude()
        if projectile == -1 :
            if select == "ball":
               # entity_list.append(entities.Ball(topArrow[0], topArrow[1], 5, (top[0], top[1]), screen))
               entity_list.append(entities.Ball(400, 600, 10, (top[0], top[1]), screen))
            elif select == "shuriken":
                entity_list.append(entities.Shuriken(400, 600, (top[0], top[1]), screen))
            projectile = entity_list[-1]
    if select == "ball":
        screen.blit(ball_image, (0, 0))
    elif select == "shuriken":
        screen.blit(shuriken_image, (0, 0))
    for e in entity_list:
        if ticking:
            e.tick()
        e.render()
    for e1 in entity_list:
        if e1 == arrow:
            continue
        for e2 in entity_list:
            if e2 == arrow:
                continue
            if e1 == e2:
                continue
            if entities.collision(e1, e2, screen):
                print("COLLISION")
            else :
                print("NO")
    # print(gjk.gjk(shuriken, ball))
    pygame.display.update()
