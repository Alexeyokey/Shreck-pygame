import math
import os
import sys
import pygame


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

def load_image(name, colorkey=None, scale=None, flip=None):
    fullname = os.path.join('sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    if flip:
        image = pygame.transform.flip(image, *flip)
    return image


def get_angle_between(coords1, coords2):
    dif_x, dif_y = coords1[0] - coords2[0], coords1[1] - coords2[1]
    return math.atan2(dif_y, dif_x)


def magnitude(coords):
    x, y = coords
    distance = math.sqrt(x * x + y * y)
    return distance

def scale_to(vector, magnitude, my_magnitude):
    vector[0] *= magnitude / my_magnitude
    vector[1] *= magnitude / my_magnitude
    return vector