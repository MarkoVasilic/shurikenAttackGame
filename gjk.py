import pygame

ORIGIN = pygame.Vector2(0, 0)

def cross_product(v1, v2):
    x0 = v1[0]
    x1 = v1[1]
    x1y0 = x1 * v2[0]
    x0y1 = x0 * v2[1]
    return (x1 * (x1y0 - x0y1), x0 * (x0y1 - x1y0))


def normalize(v):
    return v / v.magnitude()

def support_function_polygon(points : [], d : pygame.Vector2):
    maxV = points[0].dot(d)
    retV = points[0]
    for v in points:
        newV = v.dot(d)
        if maxV < newV:
            maxV = newV
            retV = v
    
    return retV

def support_function_circle(circle : (pygame.Vector2, float), d : pygame.Vector2):
    retV = circle[0] + circle[1] * d.normalize()
    return retV

def support_point(s1, s2, d):
    a = s1[2](s1[1], d) - s2[2](s2[1], -d)
    return a

def gjk(s1, s2):
    if s1[0] == s2[0]:
        return True
    d = pygame.Vector2(-1, -1)
    simplex = [support_point(s1, s2, d)]
    d = ORIGIN - simplex[0]
    for i in range(100):
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
        cross = cross_product(AB, AO)
        d[0] = cross[0]
        d[1] = cross[1]
    else:
        simplex.pop(0)
        d[0] = AO[0]
        d[1] = AO[1]
    return False

def triangleCase(simplex, d):
    C, B, A = simplex
    AB, AC, AO = B - A, C - A, -A
    if AB.dot(AO) >= 0:
        cross = cross_product(AB, AO)
        if AC.dot(cross) >= 0:
            cross = cross_product(AC, AO)
            if AB.dot(cross) >= 0:
                return True
            else:
                simplex.pop(1)
                d[0] = cross[0]
                d[1] = cross[1]
        else:
            simplex.pop(1)
            d[0] = cross[0]
            d[1] = cross[1]
    else:
        if AC.dot(AO) >= 0:
            cross = cross_product(AC, AO)
            if AB.dot(cross) >= 0:
                return True
            else:
                simplex.pop(1)
                d[0] = cross[0]
                d[1] = cross[1]
        else:
            simplex.pop(1)
            simplex.pop(0)
            d[0] = AO[0]
            d[1] = AO[1]
    return False
