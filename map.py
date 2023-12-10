import pygame


class Block:
    def __init__(self, surface, through=False):
        super().__init__()
        self.__through = through
        self.__surface = surface
        self.__rect = self.__surface.get_rect()
        # self.__surface.blit(image, (0, 0))

    def get_through(self):
        return self.__through

    def get_surf(self):
        return self.__surface


class Layer:
    def __init__(self, layer):
        self.__layer = layer
        self.__map_layer = [[None] * self.__layer.width for _ in range(self.__layer.height)]
        for x, y, surf in layer.tiles():
            self.__map_layer[y][x] = Block(surf, True)
        self.__surf_width = surf.get_width()
        self.__surf_height = surf.get_height()

    def surf_size(self):
        return self.__surf_width, self.__surf_height

    def width(self):
        return self.__layer.width

    def __getitem__(self, key):
        return self.__map_layer[key]

    def height(self):
        return self.__layer.height


class Map:
    def __init__(self, layers):
        self.__layers = []
        for i in layers:
            self.__layers.append(Layer(i))

    def get_layers(self):
        return self.__layers

