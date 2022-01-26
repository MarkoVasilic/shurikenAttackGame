import pygame
import entities

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
top_left = pygame.Vector2(370, 220)
top_right = pygame.Vector2(430, 220)
bottom_left = pygame.Vector2(370, 280)
bottom_right = pygame.Vector2(430, 280)



def level1(screen):
    entity_list = [entities.Arrow(bottom1, bottom2, bottom3, middle1, middle2, middle3, middle4, topArrow, 0, screen),
                   entities.Square(top_left, top_right, bottom_left, bottom_right, [((30, 250), 200), ((770, 250), 200)], screen),
                   entities.Wall(pygame.Vector2(0, 350), pygame.Vector2(160, 350),
                                 pygame.Vector2(0, 360), pygame.Vector2(160, 360),
                                 screen, (169, 169, 169), True),
                   entities.Wall(pygame.Vector2(320, 350), pygame.Vector2(480, 350),
                                 pygame.Vector2(320, 360), pygame.Vector2(480, 360),
                                 screen, (169, 169, 169), True),
                   entities.Wall(pygame.Vector2(640, 350), pygame.Vector2(800, 350),
                                 pygame.Vector2(640, 360), pygame.Vector2(800, 360),
                                 screen, (169, 169, 169), True)]
    return entity_list


def level2(screen):
    entity_list = [entities.Arrow(bottom1, bottom2, bottom3, middle1, middle2, middle3, middle4, topArrow, 0, screen),
                   entities.Square(top_left, top_right, bottom_left, bottom_right, [((30, 250), 200), ((770, 250), 200)], screen),
                   entities.Wall(pygame.Vector2(0, 350), pygame.Vector2(160, 350),
                                 pygame.Vector2(0, 360), pygame.Vector2(160, 360),
                                 screen, (169, 169, 169), True),
                   entities.Wall(pygame.Vector2(160, 345), pygame.Vector2(320, 345),
                                 pygame.Vector2(160, 350), pygame.Vector2(320, 350),
                                 screen, (211, 211, 211), False),
                   entities.Wall(pygame.Vector2(320, 350), pygame.Vector2(480, 350),
                                 pygame.Vector2(320, 360), pygame.Vector2(480, 360),
                                 screen, (169, 169, 169), True),
                   entities.Wall(pygame.Vector2(480, 345), pygame.Vector2(640, 345),
                                 pygame.Vector2(480, 350), pygame.Vector2(640, 350),
                                 screen, (211, 211, 211), False),
                   entities.Wall(pygame.Vector2(640, 350), pygame.Vector2(800, 350),
                                 pygame.Vector2(640, 360), pygame.Vector2(800, 360),
                                 screen, (169, 169, 169), True)]
    return entity_list

def create_new_wall(center, width, height, rotation = 0):
    coordinates = [pygame.Vector2(-width/2, -height/2), pygame.Vector2(-width/2, height/2),
                   pygame.Vector2(width/2, -height/2), pygame.Vector2(width/2, height/2)]
    output = []
    for c in coordinates:
        output.append(c.rotate(rotation) + center)

    return output

def level3(screen):
    rotated_coordinates = create_new_wall(pygame.Vector2(650, 250), 160, 10, 60)
    entity_list = [entities.Arrow(bottom1, bottom2, bottom3, middle1, middle2, middle3, middle4, topArrow, 0, screen),
                   entities.Square(top_left, top_right, bottom_left, bottom_right, [((30, 250), 200), ((400, 250), 200)], screen),
                   entities.Wall(pygame.Vector2(0, 350), pygame.Vector2(160, 350),
                                 pygame.Vector2(0, 360), pygame.Vector2(160, 360),
                                 screen, (169, 169, 169), True),
                   entities.Wall(pygame.Vector2(160, 340), pygame.Vector2(320, 340),
                                 pygame.Vector2(160, 350), pygame.Vector2(320, 350),
                                 screen, (169, 169, 169), True),
                   entities.Wall(pygame.Vector2(320, 350), pygame.Vector2(480, 350),
                                 pygame.Vector2(320, 360), pygame.Vector2(480, 360),
                                 screen, (169, 169, 169), True),
                   entities.Wall(rotated_coordinates[0], rotated_coordinates[1],
                                 rotated_coordinates[2], rotated_coordinates[3],
                                 screen, (169, 169, 169), True)]
    return entity_list
