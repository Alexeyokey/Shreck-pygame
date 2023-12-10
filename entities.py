import pygame, math, os


def collision_test(object_1, object_list, old_rect):
    collision_list = []
    for obj in object_list:
        if obj.get_rect().colliderect(object_1) and obj.get_rect() != old_rect:
            collision_list.append(obj.get_rect())
    return collision_list


class PhysicsObj(object):
    def __init__(self, x, y, x_size, y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y
        self.old_rect = self.rect.copy()

    def move(self, movement, objects):
        self.x += movement[0]
        self.rect.x = self.x
        block_hit_list = collision_test(self.rect, objects, self.old_rect)
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False, 'slant_bottom': False,
                           'data': []}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers = [False, False, False, False]
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([block, markers])
            self.x = self.rect.x
        self.y += movement[1]
        self.rect.y = self.y
        block_hit_list = collision_test(self.rect, objects, self.old_rect)
        for block in block_hit_list:
            markers = [False, False, False, False]
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([block, markers])
            self.y = self.rect.y
        self.old_rect = self.rect.copy()
        return collision_types


class Entity(pygame.sprite.Sprite):
    def __init__(self, rect, image_shape, *group):
        super().__init__(*group)
        x, y, width, height = rect
        self.rect = pygame.Rect(x, y, width, height)
        self.physic_obg = PhysicsObj(*self.rect)
        self.original_surf = pygame.Surface(image_shape)
        self.original_surf.set_colorkey(pygame.Color("black"))
        self.rotated_surf = self.original_surf.copy()
        self.direction = pygame.math.Vector2()
        self.last_direction = pygame.math.Vector2()
        self.last_direction.y = -1
        self.speed = 100

    def move(self, movement, objects):
        collisions = self.physic_obg.move(movement, objects)
        self.rect.x = self.physic_obg.x
        self.rect.y = self.physic_obg.y
        return collisions

    def set_speed(self, speed):
        self.speed = speed

    def get_rect(self):
        return self.rect

    def get_draw_rect(self):
        return self.rect

    def get_surf(self):
        return self.rotated_surf