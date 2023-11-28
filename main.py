import random
import pygame
from map import Map
from spritesheet import SpriteSheet
from pytmx.util_pygame import load_pygame
from gui_elements import Button
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
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


def main():
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, speed, direction, group):
            super().__init__(group)
            self.direction = direction
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((210, 210, 210))
            self.rect = self.surf.get_rect()
            self.rect.center = player.rect.center
            self.speed = speed

        def update(self, dt):
            self.rect.center += self.direction * self.speed * dt

        def get_surf(self):
            return self.surf

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, speed, group):
            super().__init__(group)
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
            if abs(x_player - x) <= 400 and abs(y_player - y) <= 400:
                epsilon = self.speed
                dif_x = x_player - x
                dif_y = y_player - y
                if abs(dif_x) > epsilon * dt or abs(dif_x) > epsilon:
                    dif_x = epsilon if dif_x > 0 else -epsilon
                else:
                    dif_x = dif_x * dt
                if abs(dif_y) > epsilon * dt or abs(dif_y) > epsilon:
                    dif_y = epsilon if dif_y > 0 else -epsilon
                else:
                    dif_y = dif_y * dt
                dif_x, dif_y = dif_x * dt, dif_y * dt
                self.rect.move_ip(dif_x, dif_y)

        def get_surf(self):
            return self.surf

    class Player(pygame.sprite.Sprite):
        def __init__(self, stylesheet, group):
            super().__init__(group)
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
            self.current_frame_row = 1
            if keys[pygame.K_w]:
                self.current_frame_row = 1
                self.direction.y = -1
            elif keys[pygame.K_s]:
                self.current_frame_row = 1
                self.direction.y = 1
            else:
                self.direction.y = 0
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.main_player_frames = player_frames_right
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.main_player_frames = player_frames_left
            else:
                self.direction.x = 0
            if not self.direction.x and not self.direction.y:
                self.current_frame_row = 0
                self.current_frame_col = 0
            if self.last_direction != self.direction:
                self.timer_animation = pygame.time.get_ticks()
                self.current_frame_col = 0
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
            self.offset
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

        def custom_draw(self, layers, player):
            camera_group.target_camera(player)
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
    enemies = pygame.sprite.Group()
    camera_group = CameraGroup()
    bullets = pygame.sprite.Group()
    player = Player(player_sprite_sheet, camera_group)
    player.rect.move_ip(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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
            elif event.type == QUIT:
                running = False
        if not game_over:
            pressed_keys = pygame.key.get_pressed()
            if pygame.time.get_ticks() > timer:
                timer += 10000
                n_enemies += 1
                for i in range(n_enemies):
                    enemy = Enemy(100, camera_group)
                    enemies.add(enemy)
            if pressed_keys[K_q]:
                last_direction = player.last_direction.copy()
                bullet = Bullet(200, last_direction, camera_group)
                bullets.add(bullet)
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
            f1 = pygame.font.Font(None, 144)
            f2 = pygame.font.Font(None, 72)
            button = Button()
            button_size = (200, 100)
            game_over_text = f1.render('Game Over', 1, (255, 255, 255))
            retry_text = f2.render('Retry', 1, (255, 255, 255))
            button.create_button(screen, (255, 255, 255), SCREEN_WIDTH // 2 - button_size[0] // 2,
                                 SCREEN_HEIGHT // 2 + 100, button_size, retry_text, 1)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            button.draw_button()
            if pygame.mouse.get_pressed()[0]:
                if button.pressed(pygame.mouse.get_pos()):
                    running = False
                    main()
        pygame.display.flip()



if __name__ == "__main__":
    main()
    pygame.quit()