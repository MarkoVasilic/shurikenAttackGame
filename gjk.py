import pygame

ORIGIN = pygame.Vector2(0, 0)

def cross_product(v1, v2, v3):
    newV1 = pygame.Vector3(v1[0], v1[1], 0)
    newV2 = pygame.Vector3(v2[0], v2[1], 0)
    newV3 = pygame.Vector3(v3[0], v3[1], 0)
    cross1 = newV1.cross(newV2)
    cross2 = cross1.cross(newV3)
    ret = pygame.Vector2(cross2[0], cross2[1])
    return ret


def normalize(v):
    return v / v.magnitude()

def support_point(s1, s2, d):
    return s1.support_function(d) - s2.support_function(-d)

def gjk(s1, s2):
    d = normalize(s1.get_center() - s2.get_center())
    simplex = [support_point(s1, s2, d)]
    d = ORIGIN - simplex[0]
    while True:
        A = support_point(s1, s2, d)
        if A.dot(d) < 0:
            return False
        simplex.append(A)
        if handleSimplex(simplex, d):
            return True

def handleSimplex(simplex, d):
    if len(simplex) == 2:
        return lineCase(simplex, d)
    else:
        return triangleCase(simplex, d)

def lineCase(simplex, d):
    B, A = simplex
    AB, AO = B - A, ORIGIN - A
    if AB.dot(AO) >= 0:
        d = cross_product(AB, AO, AB)
    else:
        simplex.pop(0)
        d = AO
    return False

def triangleCase(simplex, d):
    C, B, A = simplex
    AB, AC, AO = B - A, C - A, ORIGIN - A
    if AB.dot(AO) >= 0:
        cross = cross_product(AB, AO, AB)
        if AC.dot(cross) >= 0:
            cross = cross_product(AC, AO, AC)
            if AB.dot(cross) >= 0:
                return True
            else:
                simplex.pop(1)
                d = cross
        else:
            simplex.pop(1)
            d = cross
    else:
        if AC.dot(AO) >= 0:
            cross = cross_product(AC, AO, AC)
            if AB.dot(cross) >= 0:
                return True
            else:
                simplex.pop(1)
                d = cross
        else:
            simplex.pop(1)
            simplex.pop(0)
            d = AO
    return False
