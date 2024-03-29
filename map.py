import pygame
from entities import Block


class Layer:
    def __init__(self, layer, collision=False, start_pos=(0, 0)):
        self.__layer = layer
        self.__map_layer = [[None] * self.__layer.width for _ in range(self.__layer.height)]
        for x, y, surf in layer.tiles():
            surf = pygame.transform.scale(surf, (surf.get_width() * 1.7, surf.get_height() * 1.7))
            self.__map_layer[y][x] = Block(surf, x, y, surf.get_width(), surf.get_height(), start_pos, collision=collision)

    def width(self):
        return self.__layer.width

    def __getitem__(self, key):
        return self.__map_layer[key]

    def height(self):
        return self.__layer.height


class Map:
    def __init__(self, layers):
        self.general_layers = []
        self.collision_layers = []
        for i in layers:
            if i.name[0:7] == "collide":
                layer = Layer(i, collision=True)
                self.collision_layers.append(layer)
                self.general_layers.append(layer)
            elif i.name == "center":
                layer = Layer(i, collision=False, start_pos=(17 * 1.75, 17 * 1.75))
                self.general_layers.append(layer)
            else:
                self.general_layers.append(Layer(i))

    def get_layers(self):
        return self.general_layers

    def get_collision_layers(self):
        return self.collision_layers