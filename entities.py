import pygame, math, os


def collision_test(object_1, object_list, old_rect):
    collision_list = []
    for obj in object_list:
        if obj.get_rect().colliderect(object_1) and obj.get_rect() != old_rect:
            collision_list.append(obj)
    return collision_list


class Block(pygame.sprite.Sprite):
    def __init__(self, surface, x, y, collision=False):
        super().__init__()
        self.collision = collision
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x * self.surface.get_width(), y * self.surface.get_height())
        if collision:
            self.physic_obj = PhysicsObj(*self.rect)

    def get_through(self):
        return self.collision

    def get_rect(self):
        return self.rect

    def get_surf(self):
        return self.surface


class PhysicsObj:
    def __init__(self, x, y, x_size, y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = x
        self.y = y
        self.old_rect = self.rect.copy()

    def move(self, movement, objects):
        self.old_rect = self.rect.copy()
        self.x += int(movement[0])
        self.rect.x = self.x
        block_hit_list = collision_test(self.rect, objects, self.old_rect)
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False, 'slant_bottom': False,
                           'data': []}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for sprite in block_hit_list:
            sprite_obj = sprite.physic_obj
            markers = [False, False, False, False]
                # collision on the right
            if self.rect.right >= sprite_obj.rect.left and self.old_rect.right <= sprite_obj.old_rect.left:
                self.rect.right = sprite_obj.rect.left
                self.x = self.rect.x
                collision_types['right'] = True
                markers[0] = True

            # collision on the left
            if self.rect.left <= sprite_obj.rect.right and self.old_rect.left >= sprite_obj.old_rect.right:
                self.rect.left = sprite_obj.rect.right
                self.x = self.rect.x
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([sprite_obj.rect, markers, sprite])
        self.y += int(movement[1])
        self.rect.y = self.y
        block_hit_list = collision_test(self.rect, objects, self.old_rect)
        for sprite in block_hit_list:
            sprite_obj = sprite.physic_obj
            markers = [False, False, False, False]
            if self.rect.bottom >= sprite_obj.rect.top and self.old_rect.bottom <= sprite_obj.old_rect.top:
                self.rect.bottom = sprite_obj.rect.top
                self.y = self.rect.y
                collision_types['bottom'] = True
                markers[2] = True
                # collision on the top
            if self.rect.top <= sprite_obj.rect.bottom and self.old_rect.top >= sprite_obj.old_rect.bottom:
                self.rect.top = sprite_obj.rect.bottom
                self.y = self.rect.y
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([sprite_obj.rect, markers, sprite])
        return collision_types


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, hp, rect, image_shape, group_to_collide, *group):
        super().__init__(*group)
        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(*rect)
        self.physic_obj = PhysicsObj(*rect)
        self.original_surf = pygame.Surface(image_shape)
        self.original_surf.set_colorkey(pygame.Color("black"))
        self.group_to_collide = pygame.sprite.Group(*group_to_collide)
        self.direction = pygame.math.Vector2((0, 0))
        self.speed = speed
        self.sprite = None
        self.cur_speed = speed
        self.additional_force = pygame.Vector2((0, 0))
        self.hp = hp
        self.set_cur_speed(self.speed)

    def move(self, movement, objects):
        movement = pygame.Vector2(movement) + self.additional_force
        collisions = self.physic_obj.move(movement, objects)
        self.rect.x = self.physic_obj.rect.x
        self.rect.y = self.physic_obj.rect.y
        self.additional_force[0] = self.additional_force[0] / 2
        self.additional_force[1] = self.additional_force[1] / 2
        return collisions

    def set_cur_speed(self, speed):
        self.cur_speed = speed

    def get_rect(self):
        return self.rect

    def draw(self, surface, rect):
        self.sprite.draw(surface, rect)

    def get_draw_rect(self):
        return self.physic_obj.rect
