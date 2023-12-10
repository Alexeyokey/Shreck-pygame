import random
import pygame
import math
from map import Map
from entities import PhysicsObj, Entity
from scripts import get_angle_between, load_image
from spritesheet import SpriteSheet, Sprite, Animation
from pytmx.util_pygame import load_pygame
from gui_elements import Button
from pygame.locals import (K_t, K_r, K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_q, KEYDOWN, QUIT)

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def start():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu = False
            elif event.type == QUIT:
                menu = False
        main_font = pygame.font.Font(None, 72)
        game_over = pygame.font.Font(None, 144).render('Welcome to Shrek', 1, (255, 255, 255))
        retry = (main_font.render('START', 1, (255, 255, 255)), (200, 100), "start")
        back_to_menu = (main_font.render('SETTINGS', 1, (255, 255, 255)), (400, 100), "settings")
        buttons = {}
        for index, i in enumerate([retry, back_to_menu]):
            button = Button()
            button_size = (400, 100)
            button.create_button(screen, (255, 255, 255), SCREEN_WIDTH // 2 - button_size[0] // 2,
                                 SCREEN_HEIGHT // 2 + index * 150, button_size, i[0], 1)
            button.draw_button()
            buttons[i[2]] = button
        screen.blit(game_over, (
            SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - game_over.get_height() // 2 - 100))
        if buttons['start'].pressed(pygame.mouse.get_pos()):
            menu = False
            main()
        elif buttons['settings'].pressed(pygame.mouse.get_pos()):
            pass
        pygame.display.flip()


def main():
    class Enemy(Entity):
        def __init__(self, coords, speed, image_shape, *group):
            super().__init__((coords[0], coords[1], image_shape[0], image_shape[1]), image_shape, *group)
            self.surf = pygame.Surface(image_shape)
            self.surf.set_colorkey((0, 0, 0))
            self.rect = pygame.Rect((coords[0], coords[1], image_shape[0], image_shape[1]))
            self.rect.topleft = coords
            self.hp = 100
            self.set_speed(speed)
            self.sprite = Sprite(8)
            wait_right = Animation.from_path('sprites/knight_wait.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0), scale=2.5)
            wait_left = Animation.from_path('sprites/knight_wait.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0), scale=2.5)
            run_right = Animation.from_path('sprites/knight_run.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0), scale=2.5)
            run_left = Animation.from_path('sprites/knight_run.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0), scale=2.5)
            self.sprite.add_animation({"wait_right": wait_right, "wait_left": wait_left,
                                        "run_right": run_right, "run_left": run_left}, loop=True)
            left_or_right = random.randint(0, 1)
            self.sprite.start_animation("wait_left" if left_or_right else "wait_right", restart_if_active=True)

        def update(self, dt):
            x, y = self.rect.center
            x_player, y_player = player.rect.center
            self.sprite.update(dt)
            if abs(x_player - x) <= 400 and abs(y_player - y) <= 400:
                speed = self.speed
                dif_x = x_player - x
                dif_y = y_player - y
                if abs(dif_x) > speed * dt or abs(dif_x) > speed:
                    dif_x = speed if dif_x > 0 else -speed
                else:
                    dif_x = dif_x * dt
                if abs(dif_y) > speed * dt or abs(dif_y) > speed:
                    dif_y = speed if dif_y > 0 else -speed
                else:
                    dif_y = dif_y * dt
                if dif_x > 0:
                    self.sprite.start_animation("run_right", restart_if_active=False)
                elif dif_x <= 0:
                    self.sprite.start_animation("run_left", restart_if_active=False)
                dif_x, dif_y = dif_x * dt, dif_y * dt
                self.move((dif_x, dif_y), [player, *enemies])

        def get_draw_rect(self):
            return pygame.Rect(self.rect.x - 20, self.rect.y - 30, self.rect.w, self.rect.h)

    class Player(Entity):
        def __init__(self, rect, image_shape, *group):
            super().__init__(rect, image_shape, *group)
            self.animation_flag = True
            self.bow = None
            self.sword = None
            self.hp = 100
            self.sprite = Sprite(8)
            wait_right = Animation.from_path('sprites/shreck_wait.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                             scale=2)
            wait_left = Animation.from_path('sprites/shreck_wait.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0),
                                            scale=2)
            run_right = Animation.from_path('sprites/shreck_run.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                            scale=2)
            run_left = Animation.from_path('sprites/shreck_run.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0),
                                           scale=2)
            self.sprite.add_animation({"wait_right": wait_right, "wait_left": wait_left,
                                        "run_right": run_right, "run_left": run_left}, loop=True)
            self.sprite.start_animation("wait_left")

        def update(self, dt):
            if self.direction.x or self.direction.y:
                self.last_direction = self.direction.copy()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.sprite.start_animation("run_right", restart_if_active=False)
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.sprite.start_animation("run_left", restart_if_active=False)
                self.direction.x = -1
            else:
                self.direction.x = 0
            movement = self.direction * self.speed * dt
            self.move(movement, enemies)
            self.animation(dt)

        def animation(self, dt):
            mouse_pos = camera_group.screen_to_wordl(pygame.mouse.get_pos())
            # if not self.direction.x and not self.direction.y:
            #     print(self.last_direction.x)
            #     self.sprite.start_animation("wait_right", restart_if_active=False) if self.last_direction.x == 1 else self.sprite.start_animation("wait_left", restart_if_active=False)
            if mouse_pos[0] > self.rect.centerx:
                if self.sprite.active_animation_key[-4:] == "left" and not self.direction.x and not self.direction.y:
                    self.sprite.start_animation('wait_right', restart_if_active=False)
            if mouse_pos[0] < self.rect.centerx:
                if self.sprite.active_animation_key[-5:] == "right" and not self.direction.x and not self.direction.y:
                    self.sprite.start_animation('wait_left', restart_if_active=False)
            self.sprite.update(dt)
            # print(self.last_direction, self.direction, self.animation_flag, self.current_frame_col)

        def get_draw_rect(self):
            return pygame.Rect(self.rect.x - 45, self.rect.y - 38, self.rect.w, self.rect.h)

    class Weapon(pygame.sprite.Sprite):
        def __init__(self, image, entity, *group):
            super().__init__(*group)
            self.entity = entity
            self.group = group
            self.image = image
            self.image.set_colorkey((0, 0, 0))
            self.image.fill((210, 210, 210))
            self.rotated_surf = self.image.copy()
            self.rect = self.rotated_surf.get_rect()
            self.rect.center = self.entity.rect.center
            self.timer = pygame.time.get_ticks()
            self.angle = 0

        def update(self, dt) -> None:
            self.angle = get_angle_between(camera_group.screen_to_wordl(pygame.mouse.get_pos()),
                                           self.entity.rect.center)
            self.rotated_surf = pygame.transform.rotate(self.image, -math.degrees(self.angle))
            rect = self.rotated_surf.get_rect(center=self.entity.rect.center)
            self.rect = rect

        def get_rect(self):
            return self.rect

        def draw(self, sreen, rect):
            sreen.blit(self.rotated_surf, rect)

        def get_draw_rect(self):
            return self.rect

        def get_surf(self):
            return self.rotated_surf

    class Sword(Weapon):

        def attack(self):
            if self.timer < pygame.time.get_ticks():
                self.timer = pygame.time.get_ticks() + 1000
                coords = pygame.Vector2(self.entity.rect.center)
                coords[0] += math.cos(self.angle) * 50
                coords[1] += math.sin(self.angle) * 50
                Bullet(0, (40, 40), coords, 0, 0.2, pygame.Surface((40, 40)), self.group, bullets)

        def update(self, dt):
            origin = self.entity.rect.center
            self.angle = get_angle_between(camera_group.screen_to_wordl(pygame.mouse.get_pos()),
                                           self.entity.rect.center)
            angle = math.degrees(self.angle) + 135
            image_rect = self.image.get_rect(
                topleft=(origin[0] - self.image.get_width(), origin[1] - self.image.get_height()))
            if angle >= 35 and angle <= 210:
                angle -= 65
            offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(angle)
            rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
            self.rotated_surf = pygame.transform.rotate(self.image, -angle)
            self.rect = self.rotated_surf.get_rect(center=rotated_image_center)
            self.rect.centerx += math.cos(self.angle) * 20
            self.rect.centery += math.sin(self.angle) * 20

    class Bow(Weapon):
        def shoot(self, speed):
            if self.timer < pygame.time.get_ticks():
                self.timer = pygame.time.get_ticks() + 1000
                image = load_image("arrow.png", (255, 255, 255))
                image = pygame.transform.scale(image, (30, 15))
                Bullet(speed, (30, 15), self.rect.center, self.angle, 10, image, self.group, bullets)

    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2(0, 0)
            self.half_w = self.display_surface.get_size()[0] // 2
            self.half_h = self.display_surface.get_size()[1] // 2
            self.add_x = 0
            self.add_y = 0

        def target_camera(self, target):
            center_offset = pygame.Vector2(target.rect.centerx - self.half_w, target.rect.centery - self.half_h)
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) + center_offset
            x, y = target.rect.centerx, target.rect.centery
            self.offset.x = target.rect.centerx - self.half_w - (x - mouse_pos.x) * 0.3
            self.offset.y = target.rect.centery - self.half_h - (y - mouse_pos.y) * 0.3

        def custom_draw(self, screen, layers, player):
            self.target_camera(player)
            for layer in layers:
                for row in range(layer.height()):
                    for col in range(layer.width()):
                        if layer[row][col]:
                            size = layer.surf_size()
                            dest = (col * size[0], row * size[1])
                            self.display_surface.blit(layer[row][col].get_surf(), dest - self.offset)
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.get_draw_rect().topleft - self.offset
                sprite.draw(self.display_surface, offset_pos)
                self.display_surface.blit(sprite.get_surf(), offset_pos)
                real_pos = sprite.get_rect().topleft - self.offset
                coords = (real_pos[0], real_pos[1], sprite.rect.w, sprite.rect.h)
                pygame.draw.rect(screen, (255, 255, 255), coords, 1)


        def screen_to_wordl(self, coords):
            return coords + self.offset

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, speed, size, coords, angle, time_disappear, image, *group):
            super().__init__(*group)
            self.x, self.y = coords
            self.angle = angle
            self.time_disappear = pygame.time.get_ticks() + time_disappear * 1000
            self.surf = image
            self.surf = pygame.transform.rotate(self.surf, -math.degrees(angle))
            if not self.surf.get_colorkey():
                self.surf.set_colorkey((0, 0, 0))
            self.rect = self.surf.get_rect()
            self.rect.center = coords
            self.speed = speed

        def update(self, dt):
            self.x += math.cos(self.angle) * self.speed * dt
            self.y += math.sin(self.angle) * self.speed * dt
            self.rect.center = (self.x, self.y)
            if self.time_disappear <= pygame.time.get_ticks():
                self.kill()

        def get_rect(self):
            return self.rect

        def get_draw_rect(self):
            return self.rect

        def draw(self, sreen, rect):
            sreen.blit(self.surf, rect)
        def get_surf(self):
            return self.surf


    running = True
    enemies = pygame.sprite.Group()
    camera_group = CameraGroup()
    bullets = pygame.sprite.Group()
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 38, 55), (64, 64), camera_group)
    player.set_speed(120)
    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    n_enemies = 1
    game_over = 0
    tmx_data = load_pygame('map/map.tmx')
    map = Map(tmx_data)
    # pygame.event.set_grab(True)
    while running:
        dt = clock.tick(60)
        dt = dt / 1000
        screen.fill((75, 122, 71))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_r:
                    if not player.bow:
                        if player.sword:
                            player.sword.kill()
                            player.sword = None
                        player.bow = Bow(pygame.Surface((15, 40)), player, camera_group)
                    else:
                        player.bow.kill()
                        player.bow = None
                elif event.key == K_t:
                    if not player.sword:
                        if player.bow:
                            player.bow.kill()
                            player.bow = None
                        player.sword = Sword(pygame.Surface((10, 50)), player, camera_group)
                    else:
                        player.sword.kill()
                        player.sword = None
            elif event.type == QUIT:
                running = False
        if not game_over:
            pressed_keys = pygame.key.get_pressed()
            if pygame.time.get_ticks() > timer:
                timer += 100000
                # n_enemies += 1
                for i in range(n_enemies):
                    Enemy((300, 300), 100, (40, 40), camera_group, enemies)
            if pressed_keys[K_q] and player.bow:
                player.bow.shoot(500)
            if pressed_keys[K_q] and player.sword:
                player.sword.attack()
            camera_group.update(dt)
            camera_group.custom_draw(screen, map.get_layers(), player)
            for i in enemies:
                if pygame.sprite.spritecollideany(i, bullets):
                    i.kill()
            # if pygame.sprite.spritecollideany(player, enemies):
            #     player.hp -= 100
            if player.hp <= 0:
                player.kill()
                game_over = 1
        else:
            main_font = pygame.font.Font(None, 72)
            game_over = pygame.font.Font(None, 144).render('Game Over', 1, (255, 255, 255))
            retry = (main_font.render('Retry', 1, (255, 255, 255)), (200, 100), "retry")
            back_to_menu = (main_font.render('Back to menu', 1, (255, 255, 255)), (400, 100), "back")
            buttons = {}
            for index, i in enumerate([retry, back_to_menu]):
                button = Button()
                button_size = (400, 100)
                button.create_button(screen, (255, 255, 255), SCREEN_WIDTH // 2 - button_size[0] // 2,
                                     SCREEN_HEIGHT // 2 + index * 150, button_size, i[0], 1)
                button.draw_button()
                buttons[i[2]] = button
            screen.blit(game_over, (
                SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - game_over.get_height() // 2 - 100))
            if buttons['retry'].pressed(pygame.mouse.get_pos()):
                running = False
                main()
            elif buttons['back'].pressed(pygame.mouse.get_pos()):
                running = False
                start()
        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()
