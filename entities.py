import pygame
import numpy as np


def rk4It(xi, yi, h, f):
    k1 = f(xi, yi)
    k2 = f(xi + h/2, yi + 0.5*k1*h)
    k3 = f(xi + h/2, yi + 0.5*k2*h)
    k4 = f(xi + h, yi + k3*h)
    return yi + h/6*(k1 + 2*k2 + 2*k3 + k4)

class Arrow:

    def __init__(self, bottom1: pygame.Vector2, bottom2: pygame.Vector2, bottom3: pygame.Vector2, middle1: pygame.Vector2, middle2: pygame.Vector2, middle3: pygame.Vector2, middle4: pygame.Vector2, top: pygame.Vector2, rotation_angle: int, screen):

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
        pygame.draw.polygon(self.screen, (69, 0, 0), self.arrow_coordinates)

class Square:
    def __init__(self, top_left: pygame.Vector2, top_right: pygame.Vector2, bottom_left: pygame.Vector2, bottom_right: pygame.Vector2, screen):

        self.coordinates = [top_left, top_right, bottom_right, bottom_left]
        self.screen = screen
        self.age = 0

    def get_center(self):
        return pygame.Vector2((self.coordinates[0][0] + self.coordinates[2][0]) / 2, (self.coordinates[0][1] + self.coordinates[2][1]) / 2)

    def support_function(self, d):
        maxV = self.coordinates[0].dot(d)
        retV = self.coordinates[0]
        for v in self.coordinates:
            newV = v.dot(d)
            if maxV < newV:
                maxV = newV
                retV = v
        return retV

    def tick(self):
        self.age = self.age + 1
        pygame.draw.polygon(self.screen, (0, 255, 0), [self.coordinates[0], self.coordinates[1], self.coordinates[2], self.coordinates[3]])


class Ball:
    
    def __init__(self, x: float, y:  float, r: float, v: (float, float), screen):        # konstruktor uzima parametre x, y, poluprecnik, brzina, screen (pygame.display)
        
        self.center = np.array((x,y), float)
        self.screen = screen
        self.radius = r
        self.velocity = np.array(v)
        self.age = 0

    def update_pos(self):       # metoda za azuriranje polozaja pomocu rk4
        self.center[0] = rk4It(self.age, self.center[0], 1, lambda t, x : self.velocity[0])
        self.center[1] = rk4It(self.age, self.center[1], 1, lambda t, y : self.velocity[1])

    def update_velocity(self, newV):
        self.velocity = newV

    def set_center(self, x, y):
        self.center = np.array((x, y), float)

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


class Shuriken:
    def __init__(self, x : float, y : float, v : (float, float), screen):       # konstruktor uzima parametre x, y, brzina, screen (pygame.display)
        
        self.center = np.array((x, y), float)
        self.screen = screen
        self.blade_from_center = np.array([np.array((-20, -20)),
                                np.array((-20, -20)) + np.array((0, -100)),
                                np.array((20, -20)) + np.array((0, -80)),
                                np.array((20, -20))
                                ])
        self.angle = 0
        self.angular_velocity = np.pi/180
        self.age = 0
        self.velocity = np.array(v)
        
        self.update_rotation_matrices()

        # lista svih ostrica surikena
        self.blades = []
        # u listu se dodaje 4 ostrice koje se crtaju redom po rotaciji, for petlja prolazi kroz sve 4 rotacije ostrica i za svaku nacrta sva 4 temena poligona ostrice
        for i in range(0,4):
            self.blades.append(np.array([self.center + self.rotation_matrices[i].dot(self.blade_from_center[0]),
                                        self.center + self.rotation_matrices[i].dot(self.blade_from_center[1]),
                                        self.center + self.rotation_matrices[i].dot(self.blade_from_center[2]),
                                        self.center + self.rotation_matrices[i].dot(self.blade_from_center[3])
                                        ]))

    def update_velocity(self, newV):
        self.velocity = newV

    def set_center(self, x, y):
        self.center = np.array((x, y), float)

    def get_center(self):
        c = pygame.Vector2(self.center[0], self.center[1])
        return c

    def support_function(self, d):
        vector2Blades = []
        for b in self.blades:
            for c in b:
                v2 = pygame.Vector2(c[0], c[1])
                vector2Blades.append(v2)
        maxV = vector2Blades[0].dot(d)
        retV = vector2Blades[0]
        for v in vector2Blades:
            newV = v.dot(d)
            if maxV < newV:
                maxV = newV
                retV = v
        return retV

    def update_pos(self):       # metoda za azuriranje polozaja pomocu rk4
        self.center[0] = rk4It(self.age, self.center[0], 1, lambda t, x : self.velocity[0])
        self.center[1] = rk4It(self.age, self.center[1], 1, lambda t, y : self.velocity[1])

    def update_angle(self):     # metoda za azuriranje ugla rotacije pomocu rk4
        self.angle = rk4It(self.age, self.angle, 1, lambda t, theta : self.angular_velocity)

    def update_rotation_matrices(self):     # metoda za azuriranje rotacionih matrica na osnovu trenutnog ugla
        
        # matrice se odredjuju pomocu formule rotacione matrice, razmaknute su za po 90 stepeni
        # [[cos(x)   -sin(x)]
        #  [sin(x)   cos(x)]]
        self.rotation_matrices = [np.array([[np.cos(self.angle),-np.sin(self.angle)],[np.sin(self.angle), np.cos(self.angle)]]),
                                np.array([[np.cos(self.angle+np.pi/2),-np.sin(self.angle+np.pi/2)],[np.sin(self.angle+np.pi/2), np.cos(self.angle+np.pi/2)]]),
                                np.array([[np.cos(self.angle+np.pi),-np.sin(self.angle+np.pi)],[np.sin(self.angle+np.pi), np.cos(self.angle+np.pi)]]),
                                np.array([[np.cos(self.angle+3*np.pi/2),-np.sin(self.angle+3*np.pi/2)],[np.sin(self.angle+3*np.pi/2), np.cos(self.angle+3*np.pi/2)]]),
                            ]
        
    # metoda za azuriranje poligona koji sacinjavaju suriken
    def update_polygons(self):
        
        self.update_rotation_matrices()
        
        # poligoni ostrica se azuriraju analogno prvoj kreaciji u konstruktoru
        for i in range(0,4):
            self.blades[i] = np.array([self.center + self.rotation_matrices[i].dot(self.blade_from_center[0]),
                                        self.center + self.rotation_matrices[i].dot(self.blade_from_center[1]),
                                        self.center + self.rotation_matrices[i].dot(self.blade_from_center[2]),
                                        self.center + self.rotation_matrices[i].dot(self.blade_from_center[3])
                                        ])

    def tick(self):
        self.age = self.age + 1
        self.update_pos()
        self.update_angle()
        self.update_polygons()
        for i in self.blades :
            pygame.draw.polygon(self.screen, (0, 0, 69), i)
            for j in i:
                pygame.draw.line(self.screen, (100, 0, 0), self.center, j)
