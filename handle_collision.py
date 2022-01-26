import pygame

import entities


def line_between_two_points(v1, v2):
    # ax0 + by0 + c = 0
    if v1[0] == v2[0]:
        c = -v1[0]
        a = 1
        b = 0
    elif v1[1] == v2[1]:
        c = -v2[1]
        a = 0
        b = 1
    else:
        a = -(v1[1] - v2[1]) / (v1[0] - v2[0])
        c = -(v1[0] * v2[1] - v2[0] * v1[1]) / (v1[0] - v2[0])
        b = 1
    return a, b, c


def intersection_between_two_lines(l1, l2):
    v = pygame.Vector2(0, 0)
    if l1[0] * l2[1] - l2[0] * l1[1] == 0:
        return None
    v[0] = (l1[1] * l2[2] - l2[1] * l1[2]) / (l1[0] * l2[1] - l2[0] * l1[1])
    v[1] = (l1[2] * l2[0] - l2[2] * l1[0]) / (l1[0] * l2[1] - l2[0] * l1[1])
    return v


def point_of_collision(ball, wall):
    for side in wall.get_sides():
        B = (side[0] + side[1]) / 2
        a = line_between_two_points(side[0], side[1])
        b = line_between_two_points(ball.get_center(), wall.get_center())
        A = intersection_between_two_lines(a, b)
        if A is None:
            continue
        BCW = wall.get_center() - B
        CKA = A - ball.get_center()
        if BCW.dot(CKA) > 0:
            angle = BCW.angle_to(CKA)
            CKA = CKA.rotate(-angle).normalize() * ball.radius
            return CKA + ball.get_center()
    return None


def new_way(ball, point):
    CKA = point - ball.get_center()
    angle = CKA.angle_to(ball.velocity)
    if abs(angle) < 90:
        new_velocity = -ball.velocity.rotate(-angle * 2)
        ball.velocity[0] = new_velocity[0]
        ball.velocity[1] = new_velocity[1]


def strong_wall_shuriken_collision(e1, e2, entity_list):
    if isinstance(e1, entities.Shuriken):
        shuriken = e1
    else:
        shuriken = e2
    shuriken.velocity = (0, 0)
    shuriken.angular_velocity = (0, 0)
    start_ticks = pygame.time.get_ticks()
    timer = True
    while timer:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 1:
            timer = False
    entity_list.remove(shuriken)


def weak_wall_shuriken_collision(e1, e2, entity_list):
    entity_list.remove(e1)
    entity_list.remove(e2)


def wall_ball_collision(e1, e2):
    if isinstance(e1, entities.Ball):
        point = point_of_collision(e1, e2)
        new_way(e1, point)
    else:
        point = point_of_collision(e2, e1)
        new_way(e2, point)


def target_projectile_collision(e1, e2):
    if isinstance(e1, entities.Shuriken):
        shuriken = e1
        ball = False
    elif isinstance(e2, entities.Shuriken):
        shuriken = e2
        ball = False
    elif isinstance(e1, entities.Ball):
        ball = e1
        shuriken = False
    elif isinstance(e2, entities.Ball):
        ball = e2
        shuriken = False
    if not ball:
        shuriken.velocity = (0, 0)
        shuriken.angular_velocity = (0, 0)
    else:
        ball.velocity = (0, 0)
    if ball == False:
        return shuriken
    else:
        return ball
