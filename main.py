import pygame
import numpy
import entities
import handle_collision
import level

pygame.init()
screen = pygame.display.set_mode((800, 600))

ball_image = pygame.image.load('images/ball.png')
ball_image = pygame.transform.smoothscale(ball_image, (30, 30))
shuriken_image = pygame.image.load('images/shuriken.png')
shuriken_image = pygame.transform.smoothscale(shuriken_image, (30, 30))

font = pygame.font.Font('font/GothicA1-Black.ttf', 32)
textWin = font.render('Level Passed', True, (0, 255, 0), (0, 0, 0))
textWinRect = textWin.get_rect()
textWinRect.center = (400, 100)

textFailed = font.render('Level Failed', True, (0, 255, 0), (0, 0, 0))
textFailedRect = textFailed.get_rect()
textFailedRect.center = (400, 100)

textChamp = font.render('You Win', True, (0, 255, 0), (0, 0, 0))
textChampRect = textChamp.get_rect()
textChampRect.center = (400, 100)

textMenu = font.render('Press space to start', True, (0, 255, 0), (0, 0, 0))
textMenuRect = textMenu.get_rect()
textMenuRect.center = (400, 100)

fire = False
running = True
level_uploaded = False
win = False
ticking = True
timer = True
removeProjectile = False
select = "shuriken"
what_level = 1
number_of_projectiles = 3
projectile = -1
entity_list = []
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))
    clock.tick(60)
    if not level_uploaded:
        number_of_projectiles = 3
        level_uploaded = True
        if what_level == 1:
            ent = level.level1(screen)
            for e in ent:
                entity_list.append(e)
        elif what_level == 2:
            ent = level.level2(screen)
            for e in ent:
                entity_list.append(e)
        elif what_level == 3:
            ent = level.level3(screen)
            for e in ent:
                entity_list.append(e)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not fire:
                entity_list[0].update_angle(-numpy.pi / 100)
            if event.key == pygame.K_RIGHT and not fire:
                entity_list[0].update_angle(numpy.pi / 100)
            if event.key == pygame.K_SPACE and not fire:
                fire = True
            if event.key == pygame.K_1 and not fire:
                select = "shuriken"
            if event.key == pygame.K_2 and not fire:
                select = "ball"
            if event.key == pygame.K_r:
                entity_list.clear()
                level_uploaded = False
                fire = False
                projectile = -1
                number_of_projectiles = 3
                what_level = 1
                projectile = -1
            if event.key == pygame.K_p:
                ticking = False
            if event.key == pygame.K_n:
                removeProjectile = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                entity_list[0].update_angle(0)
            if event.key == pygame.K_p:
                ticking = True
    if fire:
        top = entity_list[0].getTop()
        bottom = entity_list[0].getBottom()
        top[0] = top[0] - bottom[0]
        top[1] = top[1] - bottom[1]
        top = top / top.magnitude()
        if projectile == -1:
            if select == "ball":
                entity_list.append(entities.Ball(entity_list[0].arrow_coordinates[3][0],
                                                 entity_list[0].arrow_coordinates[3][1], 10, (top[0] * 3, top[1] * 3),
                                                 screen))
            elif select == "shuriken":
                entity_list.append(
                    entities.Shuriken(entity_list[0].arrow_coordinates[3][0], entity_list[0].arrow_coordinates[3][1],
                                      (top[0] * 3, top[1] * 3), screen))
            projectile = entity_list[-1]
    if select == "ball":
        screen.blit(ball_image, (0, 0))
    elif select == "shuriken":
        screen.blit(shuriken_image, (0, 0))
    for e1 in entity_list:
        if e1 == entity_list[0]:
            continue
        for e2 in entity_list:
            if e2 == entity_list[0]:
                continue
            if e1 == e2:
                continue
            if entities.collision(e1, e2, screen):
                if (isinstance(e1, entities.Wall) and isinstance(e2, entities.Shuriken) and e1.is_strong) \
                        or (isinstance(e1, entities.Shuriken) and isinstance(e2, entities.Wall) and e2.is_strong):
                    handle_collision.strong_wall_shuriken_collision(e1, e2, entity_list)
                    fire = False
                    number_of_projectiles = number_of_projectiles - 1
                    projectile = -1
                elif (isinstance(e1, entities.Wall) and isinstance(e2, entities.Shuriken) and e1.is_strong == False) \
                        or (
                        isinstance(e1, entities.Shuriken) and isinstance(e2, entities.Wall) and e2.is_strong == False):
                    handle_collision.weak_wall_shuriken_collision(e1, e2, entity_list)
                    fire = False
                    number_of_projectiles = number_of_projectiles - 1
                    projectile = -1
                elif (isinstance(e1, entities.Wall) and isinstance(e2, entities.Ball)) \
                        or (isinstance(e1, entities.Ball) and isinstance(e2, entities.Wall)):
                    handle_collision.wall_ball_collision(e1, e2)
                elif (isinstance(e1, entities.Square) and (
                        isinstance(e2, entities.Shuriken) or isinstance(e2, entities.Ball))) \
                        or (isinstance(e2, entities.Square) and (
                        isinstance(e1, entities.Shuriken) or isinstance(e1, entities.Ball))):
                    win = True
                    ret = handle_collision.target_projectile_collision(e1, e2)
                    entity_list.remove(ret)
    for e in entity_list:
        if (isinstance(e, entities.Ball) or isinstance(e, entities.Shuriken))\
                and (e.check_coordinates() or removeProjectile):
            entity_list.remove(e)
            projectile = -1
            number_of_projectiles = number_of_projectiles - 1
            removeProjectile = False
            fire = False
        if ticking:
            e.tick()
        e.render()
    if number_of_projectiles == 0 and not win:
        screen.blit(textFailed, textFailedRect)
        entity_list.clear()
        level_uploaded = False
        fire = False
        projectile = -1
        number_of_projectiles = 3
        what_level = 1
        pygame.display.update()
        start_ticks = pygame.time.get_ticks()
        timer = True
        while timer:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 1:
                timer = False
    elif win:
        if what_level == 3:
            screen.blit(textChamp, textChampRect)
            what_level = 1
        else:
            screen.blit(textWin, textWinRect)
            what_level = what_level + 1
        entity_list.clear()
        level_uploaded = False
        fire = False
        projectile = -1
        number_of_projectiles = 3
        win = False
        pygame.display.update()
        start_ticks = pygame.time.get_ticks()
        timer = True
        while timer:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 1:
                timer = False
    else:
        output = 'Level: ' + str(what_level)
        textLevel = font.render(output, True, (0, 255, 0), (0, 0, 128))
        textLevelRect = textLevel.get_rect()
        textLevelRect.center = (700, 25)

        output = 'Bullets: ' + str(number_of_projectiles)
        textBullets = font.render(output, True, (0, 255, 0), (0, 0, 128))
        textBulletsRect = textBullets.get_rect()
        textBulletsRect.center = (700, 60)

        screen.blit(textLevel, textLevelRect)
        screen.blit(textBullets, textBulletsRect)
        pygame.display.update()
