import random
import pygame
from map import Map
from spritesheet import SpriteSheet
from pytmx.util_pygame import load_pygame
from gui_elements import Button
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_q,
    KEYDOWN,
    QUIT,
)
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#
# def is_the_direction(direction):
#     global current_animation_index
#     if current_direction == direction:
#         current_animation_index += 1
#         if current_animation_index > 7:
#             current_animation_index = 0
#     else:
#         current_animation_index = 0


def main():
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, speed, direction):
            super(Bullet, self).__init__()
            self.direction = direction
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((210, 210, 210))
            self.rect = self.surf.get_rect()
            self.rect.center = player.rect.center
            self.speed = speed

        def update(self, dt):
            self.rect.center += self.direction * self.speed * dt
            # if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            #     self.kill()

        def get_surf(self):
            return self.surf

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, speed):
            super(Enemy, self).__init__()
            self.hp = 100
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((255, 0, 0))
            self.rect = self.surf.get_rect()
            self.epsilon = 100
            x, y = player.rect.center
            x, y = x - self.epsilon, y - self.epsilon
            safe_rect = pygame.Rect(x, y, 2 * self.epsilon, 2 * self.epsilon)
            not_safe = pygame.Rect(random.randint(20, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT), self.rect.w, self.rect.h)
            while safe_rect.colliderect(not_safe):
                not_safe = pygame.Rect(random.randint(20, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT), self.rect.w, self.rect.h)
            self.rect = not_safe
            self.speed = speed

        def update(self, dt):
            x, y = self.rect.center
            x_player, y_player = player.rect.center
            epsilon = self.speed
            dif_x = x_player - x
            dif_y = y_player - y
            if abs(dif_x) > epsilon:
                if dif_x < 0:
                    dif_x = -epsilon
                else:
                    dif_x = epsilon
            if abs(dif_y) > epsilon:
                if dif_y < 0:
                    dif_y = -epsilon
                else:
                    dif_y = epsilon
            if abs(dif_x) > epsilon * dt:
                dif_x = epsilon * dt if dif_x > 0 else -epsilon * dt
            else:
                dif_x = dif_x * dt
            if abs(dif_y) > epsilon * dt:
                dif_y = epsilon * dt if dif_y > 0 else -epsilon * dt
            else:
                dif_y = dif_y * dt
            self.rect.move_ip(dif_x, dif_y)

        def get_surf(self):
            return self.surf

    class Player(pygame.sprite.Sprite):
        def __init__(self, stylesheet):
            super(Player, self).__init__()
            self.hp = 100
            self.stylesheet = stylesheet
            self.surf = pygame.Surface((40, 55))
            self.surf.set_colorkey(pygame.Color("black"))
            self.rect = self.surf.get_rect()
            self.direction = pygame.math.Vector2()
            self.last_direction = pygame.math.Vector2()
            self.last_direction.y = -1
            self.speed = 100
            self.current_frame_row = 0
            self.current_frame_col = 0
            self.timer_animation = pygame.time.get_ticks()
            self.main_player_frames = player_frames_right
            self.frame = self.main_player_frames[self.current_frame_row][self.current_frame_col]

        def update(self, dt):
            if self.direction.x or self.direction.y:
                self.last_direction = self.direction.copy()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.current_frame_row = 1
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.current_frame_row = 1
                self.direction.y = 1
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.main_player_frames = player_frames_right
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.main_player_frames = player_frames_left
            else:
                self.direction.x = 0
            if not self.direction.x and not self.direction.y:
                self.current_frame_row = 0
                self.current_frame_col = 0
            if self.last_direction != self.direction:
                self.timer_animation = pygame.time.get_ticks()
            if pygame.time.get_ticks() >= self.timer_animation:
                self.timer_animation += 150
                self.current_frame_col = (self.current_frame_col + 1) % 4
                self.frame = self.main_player_frames[self.current_frame_row][self.current_frame_col]
            self.rect.center += self.direction * self.speed * dt
            self.surf.fill((0, 0, 0))
            self.surf.blit(self.frame, (-25, -30))

        def get_surf(self):
            return self.surf

    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2(0, 0)
            self.half_w = self.display_surface.get_size()[0] // 2
            self.half_h = self.display_surface.get_size()[1] // 2
            self.add_x = 0
            self.add_y = 0

        def center_target_camera(self, target):
            x, y = target.direction.x, target.direction.y
            if (target.direction != (0, 0) and
                    (abs(self.add_x) < abs(target.direction.x * 50) or target.last_direction.x != target.direction.x)):
                self.add_x += x * 3
            if target.direction != (0, 0) and (abs(self.add_y) < abs(
                    target.direction.y * 50) or target.last_direction.y != target.direction.y):
                self.add_y += y * 3
            self.offset.x = target.rect.centerx - self.half_w + self.add_x
            self.offset.y = target.rect.centery - self.half_h + self.add_y

        def custom_draw(self, layers, player):
            camera_group.center_target_camera(player)
            for layer in layers:
                for row in range(layer.height()):
                    for col in range(layer.width()):
                        if layer[row][col]:
                            size = layer.surf_size()
                            dest = (col * size[0], row * size[1])
                            self.display_surface.blit(layer[row][col], dest - self.offset)
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.get_surf(), offset_pos)
            # self.center_target_camera(player)
            # # self.box_target_camera(player)
            # # self.keyboard_control()
            # self.mouse_control()
            # self.zoom_keyboard_control()
            #
            # self.internal_surf.fill('#71ddee')
            #
            # # ground
            # ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
            # self.internal_surf.blit(self.ground_surf, ground_offset)
            #
            # # active elements
            # for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            #     offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            #     self.internal_surf.blit(sprite.image, offset_pos)
            #
            # scaled_surf = pygame.transform.scale(self.internal_surf,
            #                                      self.internal_surface_size_vector * self.zoom_scale)
            # scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))
            #
            # self.display_surface.blit(scaled_surf, scaled_rect)


    running = True

    player_sprite_sheet = SpriteSheet(
        pygame.image.load("sprites/camelot_ [version 1.0]/arthurPendragon_.png").convert_alpha())
    player_frames_right = []
    player_frames_left = []
    for row in range(8):
        player_frames_right.append([])
        for col in range(4):
            player_frames_right[row].append(player_sprite_sheet.get_image((col, row), 32, 32, 3, pygame.Color("black")))
    for row in range(8):
        player_frames_left.append([])
        for col in range(4, 8):
            player_frames_left[row].append(player_sprite_sheet.get_image((col, row), 32, 32, 3, pygame.Color("black")))
    player = Player(player_sprite_sheet)
    enemies = pygame.sprite.Group()
    camera_group = CameraGroup()
    bullets = pygame.sprite.Group()
    camera_group.add(player)
    player.rect.move_ip(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    n_enemies = 1
    game_over = 0
    tmx_data = load_pygame('map/map.tmx')
    map = Map(tmx_data)
    f1 = pygame.font.Font(None, 144)
    f2 = pygame.font.Font(None, 72)
    text1 = f1.render('Game Over', 1, (255, 255, 255))
    text2 = f2.render('Retry', 1, (255, 255, 255))
    button = Button()
    button_size = (200, 100)
    button.create_button(screen, (255, 255, 255), SCREEN_WIDTH // 2 - button_size[0] // 2, SCREEN_HEIGHT // 2 + 100, button_size, text2, 1)
    while running:
        dt = clock.tick(60)
        dt = dt / 1000
        screen.fill((75, 122, 71))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        if not game_over:
            pressed_keys = pygame.key.get_pressed()
            # if pygame.time.get_ticks() > timer:
            #     timer += 1000
            #     n_enemies += 1
            #     for i in range(n_enemies):
            #         enemy = Enemy(100)
            #         enemies.add(enemy)
            #         camera_group.add(enemy)
            if pressed_keys[K_q]:
                last_direction = player.last_direction.copy()
                bullet = Bullet(200, last_direction)
                bullets.add(bullet)
                camera_group.add(bullet)
            camera_group.update(dt)
            camera_group.custom_draw(map.get_layers(), player)
            for i in enemies:
                if pygame.sprite.spritecollideany(i, bullets):
                    i.kill()
            if pygame.sprite.spritecollideany(player, enemies):
                player.hp -= 100
                if player.hp <= 0:
                    player.kill()
                    game_over = 1
        else:
            screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2 - text1.get_height() // 2))
            button.draw_button()
            if pygame.mouse.get_pressed()[0]:
                if button.pressed(pygame.mouse.get_pos()):
                    running = False
                    main()
        pygame.display.flip()



if __name__ == "__main__":
    main()
    pygame.quit()