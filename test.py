import numpy as np
import pygame
import gjk

pygame.init()

screen = pygame.display.set_mode((800, 600))
triangle_coordinates = [pygame.Vector2(50, 100), pygame.Vector2(300, 250), pygame.Vector2(100, 50)]
square_coordinates = [pygame.Vector2(200, 200), pygame.Vector2(200, 250), pygame.Vector2(250, 250),
                      pygame.Vector2(300, 200)]

def rk4It(xi, yi, h, f):
    k1 = f(xi, yi)
    k2 = f(xi + h/2, yi + 0.5*k1*h)
    k3 = f(xi + h/2, yi + 0.5*k2*h)
    k4 = f(xi + h, yi + k3*h)
    return yi + h/6*(k1 + 2*k2 + 2*k3 + k4)

class Triangle:
    def __init__(self, input):
        self.k = [input[0], input[1], input[2]]

    def draw_triangle(self):
        pygame.draw.polygon(screen, (0, 255, 0), [self.k[0], self.k[1], self.k[2]])

    def center(self):
        return pygame.Vector2((self.k[0][0] + self.k[1][0] + self.k[2][0]) / 3, (self.k[0][1] + self.k[1][1] + self.k[2][1]) / 3)

    def draw_center(self):
        pygame.draw.circle(screen, (0, 0, 0), self.center(), 1)

    def support_function(self, d):
        maxV = self.k[0].dot(d)
        retV = self.k[0]
        for v in self.k:
            newV = v.dot(d)
            if maxV < newV:
                maxV = newV
                retV = v
        return retV

class Square:
    def __init__(self, input):
        self.k = [input[0], input[1], input[2], input[3]]

    def get_center(self):
        return pygame.Vector2((self.k[0][0] + self.k[2][0]) / 2, (self.k[0][1] + self.k[2][1]) / 2)

    def draw_square(self):
        pygame.draw.polygon(screen, (0, 255, 0), [self.k[0], self.k[1], self.k[2], self.k[3]])

    def draw_center(self):
        pygame.draw.circle(screen, (0, 0, 0), self.get_center(), 1)

    def support_function(self, d):
        maxV = self.k[0].dot(d)
        retV = self.k[0]
        for v in self.k:
            newV = v.dot(d)
            if maxV < newV:
                maxV = newV
                retV = v
        print(retV)
        return retV


class Ball:

    def __init__(self, x: float, y: float, r: float, v: (float, float),
                 screen):  # konstruktor uzima parametre x, y, poluprecnik, brzina, screen (pygame.display)

        self.center = np.array((x, y), float)
        self.screen = screen
        self.radius = r
        self.velocity = np.array(v)
        self.age = 0

    def update_pos(self):  # metoda za azuriranje polozaja pomocu rk4
        self.center[0] = rk4It(self.age, self.center[0], 1, lambda t, x: self.velocity[0])
        self.center[1] = rk4It(self.age, self.center[1], 1, lambda t, y: self.velocity[1])

    def update_velocity(self, newV):
        self.velocity = newV

    def get_center(self):
        c = pygame.Vector2(self.center[0], self.center[1])
        return c

    def support_function(self, d):
        c = self.get_center()
        retV = c + self.radius * d
        return retV.normalize()

    def tick(self):
        self.age = self.age + 1
        self.update_pos()
        pygame.draw.circle(self.screen, (69, 0, 0), self.center, self.radius)


def cross_product(v1, v2, v3):
    newV1 = pygame.Vector3(v1[0], v1[1], 0)
    newV2 = pygame.Vector3(v2[0], v2[1], 0)
    newV3 = pygame.Vector3(v3[0], v3[1], 0)
    print(newV1, newV2, newV3)
    cross1 = newV1.cross(newV2)
    print(cross1)
    cross2 = cross1.cross(newV1)
    ret = pygame.Vector2(cross2[0], cross2[1])
    return ret


running = True
triangle = Triangle(triangle_coordinates)
square = Square(square_coordinates)
ball = Ball(500, 500, 10, (0, 0), screen)
a = triangle_coordinates[2].normalize() - triangle_coordinates[0].normalize()
b = pygame.Vector2(-triangle_coordinates[2][0], - -triangle_coordinates[2][1]).normalize()
print(gjk.gjk(square, ball))
print(np.array((100, 100)))
print(pygame.Vector2(100, 100))

while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    triangle.draw_triangle()
    triangle.draw_center()
    square.draw_square()
    square.draw_center()
    ball.tick()
    pygame.draw.circle(screen, (0, 0, 0), [0.0894427, 0.0894427], 1)
    pygame.display.update()
