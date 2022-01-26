import gjk
import pygame
import numpy as np


def rk4It(xi, yi, h, f):
    k1 = f(xi, yi)
    k2 = f(xi + h / 2, yi + 0.5 * k1 * h)
    k3 = f(xi + h / 2, yi + 0.5 * k2 * h)
    k4 = f(xi + h, yi + k3 * h)
    return yi + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def collision(A, B, screen):
    if isinstance(A, Ball):
        pA = [A.get_center(), (A.get_center(), A.get_radius()), gjk.support_function_circle]
    elif isinstance(A, Square) or isinstance(A, Wall):
        pA = [A.get_center(), A.get_coordinates(), gjk.support_function_polygon]

    if isinstance(B, Ball):
        pB = [B.get_center(), (B.get_center(), B.get_radius()), gjk.support_function_circle]
    elif isinstance(B, Square) or isinstance(B, Wall):
        pB = [B.get_center(), B.get_coordinates(), gjk.support_function_polygon]

    if isinstance(A, Shuriken) and (isinstance(B, Ball) or isinstance(B, Square) or isinstance(B, Wall)):
        pA = [A.get_center(), [], gjk.support_function_polygon]
        for blade in A.blades:
            pA[1] = blade
            if gjk.gjk(pA, pB):
                return True
        return False
    elif isinstance(B, Shuriken) and (isinstance(A, Ball) or isinstance(A, Square) or isinstance(A, Wall)):
        pB = [B.get_center(), [], gjk.support_function_polygon]
        for blade in B.blades:
            pB[1] = blade
            if gjk.gjk(pA, pB):
                return True
        return False
    elif (isinstance(B, Ball) or isinstance(B, Square) or isinstance(B, Wall)) and (isinstance(A, Ball) or isinstance(A, Square) or isinstance(A, Wall)):
        return gjk.gjk(pA, pB)


class Arrow:

    def __init__(self, bottom1: pygame.Vector2, bottom2: pygame.Vector2, bottom3: pygame.Vector2,
                 middle1: pygame.Vector2, middle2: pygame.Vector2, middle3: pygame.Vector2, middle4: pygame.Vector2,
                 top: pygame.Vector2, rotation_angle: int, screen):

        self.arrow_coordinates = [bottom1, middle2, middle1, top, middle4, middle3, bottom3, bottom2]
        self.rotation_angle = rotation_angle
        self.screen = screen
        self.firstCoordinate = top
        self.age = 0

    def angle_between_two_vectors(self, v1, v2):
        origin = pygame.Vector2(400, 600)
        return (v1 - origin).angle_to(v2 - origin)

    def rotation_around_vector(self, v1, v2, deg):
        return (v2 - v1).rotate_rad(deg) + v1

    def rotation_around_vector_array(self, deg):
        new_coordinates = []
        for v in self.arrow_coordinates:
            new_coordinates.append(self.rotation_around_vector(self.arrow_coordinates[-1], v, deg))
        return new_coordinates

    def update_angle(self, deg):
        self.rotation_angle = deg

    def update_coordinates(self):
        temp_arrow_coordinates = self.rotation_around_vector_array(self.rotation_angle)
        vector_arrow = temp_arrow_coordinates[3]
        if 83 > self.angle_between_two_vectors(self.firstCoordinate, vector_arrow) > -83:
            self.arrow_coordinates = self.rotation_around_vector_array(self.rotation_angle)

    def getTop(self):
        temp = pygame.Vector2(self.arrow_coordinates[3])
        return temp

    def getBottom(self):
        temp = pygame.Vector2(self.arrow_coordinates[-1])
        return temp

    def tick(self):
        self.age = self.age + 1
        self.update_coordinates()

    def render(self):
        pygame.draw.polygon(self.screen, (69, 0, 0), self.arrow_coordinates)


class Wall:
    def __init__(self, top_left: pygame.Vector2, top_right: pygame.Vector2, bottom_left: pygame.Vector2,
                 bottom_right: pygame.Vector2, screen, color, is_strong):

        self.coordinates = [top_left, top_right, bottom_right, bottom_left]
        self.screen = screen
        self.age = 0
        self.color = color
        self.is_strong = is_strong

    def get_sides(self):
        return [
            (self.coordinates[0], self.coordinates[1]),
            (self.coordinates[0], self.coordinates[3]),
            (self.coordinates[2], self.coordinates[1]),
            (self.coordinates[2], self.coordinates[3])
        ]

    def get_center(self):
        return pygame.Vector2((self.coordinates[0][0] + self.coordinates[2][0]) / 2,
                              (self.coordinates[0][1] + self.coordinates[2][1]) / 2)

    def get_coordinates(self):
        return self.coordinates

    def tick(self):
        self.age = self.age + 1

    def render(self):
        pygame.draw.polygon(self.screen, self.color,
                            [self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3]])


class Square:
    def __init__(self, top_left: pygame.Vector2, top_right: pygame.Vector2, bottom_left: pygame.Vector2,
                 bottom_right: pygame.Vector2, move_pattern, screen):

        self.coordinates = [top_left, top_right, bottom_right, bottom_left]
        self.screen = screen
        self.age = 0

        self.move_pattern = move_pattern
        self.move_pattern_index = 0
        self.move_pattern_time = 0
        if len(self.move_pattern) > 0:
            self.velocity = (pygame.Vector2(move_pattern[0][0]) - pygame.Vector2(self.get_center())) / move_pattern[0][
                1]
        else:
            self.velocity = pygame.Vector2((0, 0))

    def get_center(self):
        return pygame.Vector2((self.coordinates[0][0] + self.coordinates[2][0]) / 2,
                              (self.coordinates[0][1] + self.coordinates[2][1]) / 2)

    def get_coordinates(self):
        return self.coordinates

    def move(self):
        if len(self.move_pattern) > 0:
            if self.move_pattern[self.move_pattern_index][1] < self.move_pattern_time:
                self.move_pattern_index = (self.move_pattern_index + 1) % len(self.move_pattern)
                self.velocity = (pygame.Vector2(self.move_pattern[self.move_pattern_index][0]) - pygame.Vector2(
                    self.get_center())) / self.move_pattern[self.move_pattern_index][1]
                self.move_pattern_time = 0

            self.move_pattern_time += 1

        self.coordinates[0][0] = rk4It(self.age, self.coordinates[0][0], 1, lambda t, x: self.velocity[0])
        self.coordinates[0][1] = rk4It(self.age, self.coordinates[0][1], 1, lambda t, x: self.velocity[1])

        self.coordinates[1][0] = rk4It(self.age, self.coordinates[1][0], 1, lambda t, x: self.velocity[0])
        self.coordinates[1][1] = rk4It(self.age, self.coordinates[1][1], 1, lambda t, x: self.velocity[1])

        self.coordinates[2][0] = rk4It(self.age, self.coordinates[2][0], 1, lambda t, x: self.velocity[0])
        self.coordinates[2][1] = rk4It(self.age, self.coordinates[2][1], 1, lambda t, x: self.velocity[1])

        self.coordinates[3][0] = rk4It(self.age, self.coordinates[3][0], 1, lambda t, x: self.velocity[0])
        self.coordinates[3][1] = rk4It(self.age, self.coordinates[3][1], 1, lambda t, x: self.velocity[1])

    def tick(self):
        self.age = self.age + 1
        self.move()

    def render(self):
        pygame.draw.polygon(self.screen, (0, 255, 0),
                            [self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3]])


class Ball:

    def __init__(self, x: float, y: float, r: float, v: (float, float),
                 screen):  # konstruktor uzima parametre x, y, poluprecnik, brzina, screen (pygame.display)

        self.center = pygame.Vector2((x, y))
        self.screen = screen
        self.radius = r
        self.velocity = pygame.Vector2(v)
        self.age = 0

    def update_pos(self):  # metoda za azuriranje polozaja pomocu rk4
        self.center.x = rk4It(self.age, self.center.x, 1, lambda t, x: self.velocity.x)
        self.center.y = rk4It(self.age, self.center.y, 1, lambda t, y: self.velocity.y)

    def update_velocity(self, newV: pygame.Vector2):
        self.velocity = newV

    def set_center(self, x, y):
        self.center = pygame.Vector2(x, y)

    def get_radius(self):
        return self.radius

    def get_center(self):
        c = pygame.Vector2(self.center.x, self.center.y)
        return c

    def check_coordinates(self):
        if self.center[0] < 0 or self.center[0] > 800 or self.center[1] < 0 or self.center[1] > 600:
            return True
        else:
            return False

    def tick(self):
        self.age = self.age + 1
        self.update_pos()

    def render(self):
        pygame.draw.circle(self.screen, (69, 0, 0), self.center, self.radius)


class Shuriken:
    def __init__(self, x: float, y: float, v: (float, float),
                 screen):  # konstruktor uzima parametre x, y, brzina, screen (pygame.display)

        self.center = pygame.Vector2(x, y)
        self.screen = screen
        self.blade_from_center = [pygame.Vector2((-5, -5)),
                                  pygame.Vector2((-5, -5)) + pygame.Vector2((0, -20)),
                                  pygame.Vector2((5, -5)) + pygame.Vector2((0, -10)),
                                  pygame.Vector2((5, -5))
                                  ]
        self.angle = 0
        self.angular_velocity = np.pi / 180
        self.age = 0
        self.velocity = pygame.Vector2(v)

        # lista svih ostrica surikena
        self.blades = []
        # u listu se dodaje 4 ostrice koje se crtaju redom po rotaciji, for petlja prolazi kroz sve 4 rotacije ostrica i za svaku nacrta sva 4 temena poligona ostrice
        for i in range(0, 4):
            self.blades.append([self.center + self.blade_from_center[0].rotate_rad(self.angle + i * (np.pi / 2)),
                                self.center + self.blade_from_center[1].rotate_rad(self.angle + i * (np.pi / 2)),
                                self.center + self.blade_from_center[2].rotate_rad(self.angle + i * (np.pi / 2)),
                                self.center + self.blade_from_center[3].rotate_rad(self.angle + i * (np.pi / 2))
                                ])

    def update_velocity(self, newV):
        self.velocity = newV

    def set_center(self, x, y):
        self.center = pygame.Vector2((x, y))

    def get_center(self):
        return pygame.Vector2(self.center[0], self.center[1])

    def check_coordinates(self):
        if self.center[0] < 0 or self.center[0] > 800 or self.center[1] < 0 or self.center[1] > 600:
            return True
        else:
            return False

    def update_pos(self):  # metoda za azuriranje polozaja pomocu rk4
        self.center[0] = rk4It(self.age, self.center[0], 1, lambda t, x: self.velocity[0])
        self.center[1] = rk4It(self.age, self.center[1], 1, lambda t, y: self.velocity[1])

    def update_angle(self):  # metoda za azuriranje ugla rotacije pomocu rk4
        if self.angular_velocity != (0, 0):
            self.angle = rk4It(self.age, self.angle, 1, lambda t, theta: self.angular_velocity)

    # metoda za azuriranje poligona koji sacinjavaju suriken
    def update_polygons(self):

        # poligoni ostrica se azuriraju analogno prvoj kreaciji u konstruktoru
        for i in range(0, 4):
            self.blades[i] = [self.center + self.blade_from_center[0].rotate_rad(self.angle + i * (np.pi / 2)),
                              self.center + self.blade_from_center[1].rotate_rad(self.angle + i * (np.pi / 2)),
                              self.center + self.blade_from_center[2].rotate_rad(self.angle + i * (np.pi / 2)),
                              self.center + self.blade_from_center[3].rotate_rad(self.angle + i * (np.pi / 2))
                              ]

    def tick(self):
        self.age = self.age + 1
        self.update_pos()
        self.update_angle()
        self.update_polygons()

    def render(self):
        for i in self.blades:
            pygame.draw.polygon(self.screen, (0, 0, 69), i)
            for j in i:
                pygame.draw.line(self.screen, (100, 0, 0), self.center, j)
