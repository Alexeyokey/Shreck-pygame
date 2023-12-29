import random
import pygame
import math
from map import Map
from entities import PhysicsObj, Entity
from particles import create_particles
from scripts import get_angle_between, load_image
from sprite_tools import Sprite, Animation
from levels import first_level, second_level, third_level
from pytmx.util_pygame import load_pygame
from gui_elements import Button
from pygame.locals import (K_t, K_r, K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_q, KEYDOWN, QUIT)
import pygame_gui

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme_for_button.json')
pygame.mixer.music.load('shrek_09. Smash Mouth - All Star.mp3')
pygame.mixer.music.play()
vol = 0
sensitivity = 0.00001
sensitivity_multiplier = 1


def start():
    global manager, sensitivity
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')

    welcome = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 190), (800, 100)),
        text="Welcome to Shreck",
        manager=manager,
        object_id="#label"
    )

    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 340), (400, 100)),
        text='START',
        manager=manager,
        object_id="#button"
    )

    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 490), (400, 100)),
        text='SETTINGS',
        manager=manager,
        object_id="#button"
    )

    rating_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 640), (400, 100)),
        text='Rating',
        manager=manager,
        object_id="#button"
    )

    clock = pygame.time.Clock()
    menu = True
    while menu:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    menu = False
            elif event.type == QUIT:
                menu = False
            if event.type == pygame.MOUSEMOTION:
                axis_values = event.rel
                axis_values = [value * sensitivity for value in axis_values]
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_btn:
                        menu = False
                        main()
                    elif event.ui_element == settings_btn:
                        menu = False
                        settings()
                    elif event.ui_element == rating_btn:
                        menu = False
                        rating()
            manager.process_events(event)
        background_image = pygame.image.load("28360f8f3ee5caa2969db8131e70a01c.jpg").convert()
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()


def settings():
    global manager, vol, sensitivity, sensitivity_multiplier
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')

    setting_lbl = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 100), (800, 100)),
        text="Settings",
        manager=manager,
        object_id="#label"
    )

    sound_lbl = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 190), (800, 100)),
        text="Sound",
        manager=manager,
        object_id="#little_label"
    )

    sub_volume = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((130+345, 290), (100, 100)),
        text='-',
        manager=manager,
        object_id="#button"
    )

    mute_volume = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((240+345, 290), (100, 100)),
        text='OFF',
        manager=manager,
        object_id="#button"
    )

    add_volume = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350+345, 290), (100, 100)),
        text='+',
        manager=manager,
        object_id="#button"
    )

    sensitivity_lbl = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 390), (800, 100)),
        text="Sensitivity",
        manager=manager,
        object_id="#little_label"
    )

    add_sensitivity = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 490), (100, 100)),
        text='+',
        manager=manager,
        object_id="#button"
    )

    sub_sensitivity = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 490), (100, 100)),
        text='-',
        manager=manager,
        object_id="#button"
    )

    clock = pygame.time.Clock()
    setting = True
    while setting:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    setting = False
                    start()
            elif event.type == QUIT:
                setting = False
            if event.type == pygame.MOUSEMOTION:
                axis_values = event.rel
                axis_values = [value * sensitivity for value in axis_values]
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == sub_volume:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
                        vol = pygame.mixer.music.get_volume()
                    elif event.ui_element == mute_volume:
                        if pygame.mixer.music.get_volume() != 0:
                            pygame.mixer.music.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(vol)
                    elif event.ui_element == add_volume:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                        vol = pygame.mixer.music.get_volume()
                    elif event.ui_element == add_sensitivity:
                        if sensitivity + 1 <= 10:
                            sensitivity += 1
                    elif event.ui_element == sub_sensitivity:
                        if sensitivity - 1 <= 0:
                            sensitivity -= 1
            manager.process_events(event)
        background_image = pygame.image.load("28360f8f3ee5caa2969db8131e70a01c.jpg").convert()
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()

def end(score):
    global manager
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 190), (800, 100)),
        text=f"Total score: {score}",
        manager=manager,
        object_id="#label"
    )

    retry = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 340), (400, 100)),
        text='RETRY',
        manager=manager,
        object_id="#button"
    )

    back_to_menu = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 490), (400, 100)),
        text='BACK TO MENU',
        manager=manager,
        object_id="#button"
    )

    clock = pygame.time.Clock()
    finish = True
    while finish:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    finish = False
                    start()
            elif event.type == QUIT:
                finish = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == retry:
                        finish = False
                        main()
                    elif event.ui_element == back_to_menu:
                        finish = False
                        start()
            manager.process_events(event)
        background_image = pygame.image.load("28360f8f3ee5caa2969db8131e70a01c.jpg").convert()
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()

def rating():
    global manager
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')
    background_image = pygame.image.load("28360f8f3ee5caa2969db8131e70a01c.jpg").convert()

    welcome = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 190), (880, 100)),
        text="Rating",
        manager=manager,
        object_id="#label"
    )

    bg_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((190, 490), (900, 30)),
        manager=manager,
        object_id="#bg_panel"
    )

    real = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((190, 490), (int(open('score.txt', 'r').readlines()[0]) / 30_000 * 900, 30)),
        manager=manager,
        object_id="#real"
    )

    img = pygame.image.load('rating_photo/bronze.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((300, 350), (100, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/silver.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((400, 550), (110, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/gold.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((500, 350), (105, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/platinum.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((600, 550), (100, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/diamond.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((700, 350), (100, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/champion.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((800, 550), (120, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/grand_champion.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((900, 350), (135, 100)),
        image_surface=img,
        manager=manager
    )

    img = pygame.image.load('rating_photo/ssl.png')
    bronze = pygame_gui.elements.UIImage(
        relative_rect=pygame.Rect((1000, 550), (150, 100)),
        image_surface=img,
        manager=manager
    )

    effect_color = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 0), (1280, 720)),
        text='',
        manager=manager,
        object_id="#effect_color"
    )

    clock = pygame.time.Clock()
    rat = True
    while rat:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    rat = False
                    start()
            elif event.type == QUIT:
                rat = False
        background_image = pygame.image.load("28360f8f3ee5caa2969db8131e70a01c.jpg").convert()
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()



def main():
    class Enemy(Entity):
        def __init__(self, speed, hp, coords, image_shape, groups_to_collide, *group):
            super().__init__(speed, hp, (coords[0], coords[1], image_shape[0], image_shape[1]), image_shape, groups_to_collide, *group)
            self.surf = pygame.Surface(image_shape)
            self.surf.set_colorkey((0, 0, 0))
            self.rect = pygame.Rect((coords[0], coords[1], image_shape[0], image_shape[1]))
            self.rect.topleft = coords
            self.sprite = Sprite(8)
            self.sword = None
            self.bow = None
            self.death_flag = False
            wait_right = Animation.from_path('sprites/knight_wait.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                             scale=2.5)
            wait_left = Animation.from_path('sprites/knight_wait.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0),
                                            scale=2.5)
            run_right = Animation.from_path('sprites/knight_run.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                            scale=2.5)
            run_left = Animation.from_path('sprites/knight_run.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0),
                                           scale=2.5)
            damage_right = Animation.from_path('sprites/knight_damage.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                           scale=2.5)
            damage_left = Animation.from_path('sprites/knight_damage.png', (4, 1), 4, reverse_x=True,
                                              colorkey=(0, 0, 0),
                                              scale=2.5)
            self.sprite.add_animation({"wait_r": wait_right, "wait_l": wait_left,
                                       "run_r": run_right, "run_l": run_left}, loop=True)
            self.sprite.add_animation({"damage_r": damage_right, "damage_l": damage_left}, loop=False)
            self.sprite.add_callback('damage_r', self.change_state)
            self.sprite.add_callback('damage_r', self.check_death_and_kill)
            self.sprite.add_callback('damage_l', self.change_state)
            self.sprite.add_callback('damage_l', self.check_death_and_kill)
            left_or_right = random.randint(0, 1)
            self.cur_state = 'wait'
            self.direction = 'l' if left_or_right else 'r'
            self.sprite.start_animation("wait_l" if left_or_right else "wait_r", restart_if_active=True)

        def update(self, dt):
            x, y = self.rect.center
            x_player, y_player = player.rect.center
            self.sprite.update(dt)
            dif_x, dif_y = 0, 0
            if self.bow and abs(x_player - x) <= 200 and abs(y_player - y) <= 200 or self.sword or self.death_flag:
                speed = self.cur_speed
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
                dif_x, dif_y = dif_x * dt, dif_y * dt
                if self.bow or self.death_flag:
                    dif_x, dif_y = -dif_x, -dif_y
                self.move((dif_x, dif_y), self.groups_to_collide, 10)
            self.animation(dif_x, dif_y)

        def animation(self, dif_x, dif_y):
            if dif_x or dif_y:
                self.state = 'run'
            if self.get_rect().centerx <= player.get_rect().centerx:
                self.direction = 'r'
            elif self.get_rect().centerx > player.get_rect().centerx:
                self.direction = 'l'
            self.sprite.start_animation(self.cur_state + '_' + self.direction, restart_if_active=False)

        def move(self, movement, objects, tolerance=5):
            collisions = self.physic_obg.move(movement, objects, tolerance)
            self.rect.x = self.physic_obg.x
            self.rect.y = self.physic_obg.y
            return collisions

        # def delay_kill(self, time):
        #
        #     self.death_flag = True
        def get_hit(self, angle, damage):
            self.hp -= damage
            self.move((math.cos(angle) * 10, math.sin(angle) * 10), self.groups_to_collide)
            self.cur_state = 'damage'

        def change_state(self, state='run'):
            self.cur_state = state

        def check_death_and_kill(self):
            if self.death_flag:
                self.kill()

        def death(self):
            if enemy.sword:
                enemy.sword.kill()
                enemy.sword = None
            if enemy.bow:
                enemy.bow.kill()
                enemy.bow = None
            self.death_flag = True

        def get_draw_rect(self):
            return pygame.Rect(self.rect.x - 20, self.rect.y - 30, self.rect.w, self.rect.h)

    class Player(Entity):
        def __init__(self, speed, hp, rect, image_shape, groups_to_collide, *group):
            super().__init__(speed, hp, rect, image_shape, groups_to_collide, *group)
            self.animation_flag = True
            self.particle_flag = False
            self.last_direction = [0, 0]
            self.bow = None
            self.sword = None
            self.sprite = Sprite(8)
            self.particle_time_start = None
            self.particle_color = "#ffb476"
            wait_r = Animation.from_path('sprites/shreck_wait.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                         scale=2)
            wait_l = Animation.from_path('sprites/shreck_wait.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0),
                                         scale=2)
            run_r = Animation.from_path('sprites/shreck_run.png', (4, 1), 4, reverse_x=False, colorkey=(0, 0, 0),
                                        scale=2)
            run_l = Animation.from_path('sprites/shreck_run.png', (4, 1), 4, reverse_x=True, colorkey=(0, 0, 0),
                                        scale=2)
            self.sprite.add_animation({"wait_r": wait_r, "wait_l": wait_l,
                                       "run_r": run_r, "run_l": run_l}, loop=True)
            self.sprite.start_animation("wait_l")

        def update(self, dt):
            def start_particle_effect_if(last_direction, direction):
                if last_direction != direction:
                    self.particle_flag = True
                    self.particle_time_start = pygame.time.get_ticks()
            direction_restrict = 100
            direction_add = 5
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if self.direction.y > -direction_restrict:
                    self.direction.y -= direction_add
                start_particle_effect_if(self.last_direction[1], -1)
                self.last_direction[1] = -1
                self.sprite.start_animation(f"run_{self.sprite.active_animation_key[-1]}", restart_if_active=False)
            elif keys[pygame.K_s]:
                if self.direction.y < direction_restrict:
                    self.direction.y += direction_add
                start_particle_effect_if(self.last_direction[1], 1)
                self.last_direction[1] = 1
                self.sprite.start_animation(f"run_{self.sprite.active_animation_key[-1]}", restart_if_active=False)
            else:
                if self.direction.y != 0:
                    self.direction.y -= direction_add if self.direction.y > 0 else -direction_add
                self.last_direction[1] = 0
            if keys[pygame.K_d]:
                if self.direction.x < direction_restrict:
                    self.direction.x += direction_add
                start_particle_effect_if(self.last_direction[0], 1)
                self.last_direction[0] = 1
                self.sprite.start_animation("run_r", restart_if_active=False)
            elif keys[pygame.K_a]:
                if self.direction.x > -direction_restrict:
                    self.direction.x -= direction_add
                start_particle_effect_if(self.last_direction[0], -1)
                self.last_direction[0] = -1
                self.sprite.start_animation("run_l", restart_if_active=False)
            else:
                if self.direction.x != 0:
                    self.direction.x -= direction_add if self.direction.x > 0 else -direction_add
                self.last_direction[0] = 0
            movement = self.direction / direction_restrict * self.cur_speed * dt
            self.move(movement, self.groups_to_collide)
            self.animation(dt)
            self.particles(self.last_direction, 0.1)

        def particles(self, direction, duration):
            x_direction = -direction[0]
            y_direction = direction[1]
            if not y_direction:
                y_direction = 1
            if self.particle_flag and direction[0]:
                if pygame.time.get_ticks() - self.particle_time_start > duration * 1000:
                    self.particle_flag = False
                pos = self.rect.centerx + self.rect.w // 2 * x_direction, self.rect.centery + self.rect.h // 2
                create_particles(pos, camera_group.particle_player_color, ((3, 3), (4, 4)), range(200, 400), range(0, 100), x_direction, y_direction, 10, 0.1, particle_group)

        def animation(self, dt):
            self.sprite.update(dt)
            mouse_pos = camera_group.screen_to_wordl(pygame.mouse.get_pos())
            if mouse_pos[0] > self.rect.centerx:
                if not self.direction.x and not self.direction.y:
                    self.sprite.start_animation('wait_r', restart_if_active=False)
            if mouse_pos[0] < self.rect.centerx:
                if not self.direction.x and not self.direction.y:
                    self.sprite.start_animation('wait_l', restart_if_active=False)

        def move(self, movement, objects):
            collisions = self.physic_obg.move(movement, objects, 10)
            self.rect.x = self.physic_obg.x
            self.rect.y = self.physic_obg.y
            if pygame.sprite.spritecollideany(self, enemies):
                self.set_cur_speed(self.speed // 2)
            else:
                self.set_cur_speed(self.speed)

        def get_draw_rect(self):
            return pygame.Rect(self.rect.x - 45, self.rect.y - 38, self.rect.w, self.rect.h)

    class Weapon(pygame.sprite.Sprite):
        def __init__(self, image, entity, target, shot_delay, attacking_group, *group):
            super().__init__(*group)
            self.entity = entity
            self.target = target
            self.group = group
            self.attacking_group = attacking_group
            self.image = image
            self.image.set_colorkey((0, 0, 0))
            self.rotated_surf = self.image.copy()
            self.rect = self.rotated_surf.get_rect()
            self.rect.center = self.entity.rect.center
            self.shot_delay = shot_delay * 1000
            self.timer = pygame.time.get_ticks()
            self.angle = 0

        def get_rect(self):
            return self.rect

        def draw(self, sreen, rect):
            sreen.blit(self.rotated_surf, rect)

        def get_draw_rect(self):
            return self.rect

        def get_surf(self):
            return self.rotated_surf

    class Sword(Weapon):
        def __init__(self, image, entity, target, shot_delay, damage_area, attacking_group, *group):
            super().__init__(image, entity, target, shot_delay, attacking_group, *group)
            self.damage_area = damage_area
            self.sprite = Sprite(4)
            self.direction = 'right'
            self.state = 'idle'
            idle_left = Animation.from_path('sprites/sword.png', reverse_x=True, scale=2)
            idle_right = Animation.from_path('sprites/sword.png', reverse_x=False, scale=2)
            attack_right = Animation.from_path('sprites/attacking_sword.png', (4, 1), 4, reverse_x=False, scale=2)
            attack_left = Animation.from_path('sprites/attacking_sword_left.png', (4, 1), 4, reverse_x=False, scale=2, reverse_animation=True)
            self.sprite.add_animation({"idle_left": idle_left, "idle_right": idle_right}, loop=True, fps_override=1)
            self.sprite.add_animation({"attack_right": attack_right, "attack_left": attack_left}, loop=False)
            self.sprite.add_callback('attack_right', self.change_to_idle)
            self.sprite.add_callback('attack_left', self.change_to_idle)
            self.sprite.start_animation('idle_right')

        def change_to_idle(self):
            self.state = 'idle'

        def attack(self):
            if self.timer < pygame.time.get_ticks():
                self.state = 'attack'
                self.timer = pygame.time.get_ticks() + self.shot_delay
                coords = pygame.Vector2(self.entity.rect.center)
                coords[0] += math.cos(self.angle) * 60
                coords[1] += math.sin(self.angle) * 50
                Bullet(0, 100, "sword_attack", coords, self.angle, 0.02, pygame.Surface(self.damage_area), self.attacking_group, self.group)

        def update(self, dt):
            if not self.target:
                target = camera_group.screen_to_wordl(pygame.mouse.get_pos())
            else:
                target = self.target.get_rect().center
            origin_center = self.entity.get_rect().center
            self.angle = get_angle_between(target,
                                           self.entity.rect.center)
            angle = math.degrees(self.angle) + 145
            if angle > 55 and angle < 235:
                angle -= 100
                self.direction = 'right'
            else:
                self.direction = 'left'
            image_rect = self.image.get_rect(
                center=(origin_center[0], origin_center[1]))
            offset_center_to_pivot = pygame.math.Vector2(origin_center) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(angle)
            rotated_image_center = (origin_center[0] - rotated_offset.x, origin_center[1] - rotated_offset.y)
            self.rotated_surf = pygame.transform.rotate(self.image, -angle)
            self.rect = self.rotated_surf.get_rect(center=rotated_image_center)
            self.rect.centerx += math.cos(self.angle) * self.entity.rect.w
            self.rect.centery += math.sin(self.angle) * self.entity.rect.h
            self.sprite.start_animation(self.state + '_' + self.direction, restart_if_active=False)
            self.sprite.set_angle(-angle)
            self.sprite.update(dt)

        def draw(self, surface, rect):
            if self.state != 'attack' or self.direction == 'right':
                self.sprite.draw(surface, self.rect.topleft - camera_group.offset)
            else:
                coords = self.rect.topleft[0] - self.image.get_width(), self.rect.topleft[1]
                self.sprite.draw(surface, coords - camera_group.offset)

    class Bow(Weapon):
        def __init__(self, image, entity, target, shot_delay, arrow_speed, attacking_group, *group):
            super().__init__(image, entity, target, shot_delay, attacking_group, *group)
            self.sprite = Sprite(4)
            self.arrow_speed = arrow_speed
            idle = Animation.from_path('sprites/bow.png', (4, 1), 1, reverse_x=False, scale=2.5)
            attack = Animation.from_path('sprites/bow.png', (4, 1), 4, reverse_x=False, scale=2.5)
            self.sprite.add_animation({"idle": idle, "attack": attack})
            self.sprite.start_animation('idle')
            self.sprite.add_callback("attack", lambda: self.sprite.start_animation('idle'))
            self.sprite.add_callback("attack", lambda: self.shoot(self.arrow_speed))

        def bow_tense(self):
            if self.timer < pygame.time.get_ticks():
                self.sprite.start_animation("attack")
                self.timer = pygame.time.get_ticks() + self.shot_delay

        def shoot(self, speed):
            image = load_image("arrow.png", (255, 255, 255), (30, 10))
            Bullet(speed, 50, "arrow", self.rect.center, self.angle, 10, image, self.attacking_group, self.group)

        def update(self, dt):
            if not self.target:
                target = camera_group.screen_to_wordl(pygame.mouse.get_pos())
            else:
                target = self.target.get_rect().center
            self.angle = get_angle_between(target, self.entity.rect.center)
            self.rotated_surf = pygame.transform.rotate(self.image, -math.degrees(self.angle))
            rect = self.rotated_surf.get_rect(center=self.entity.rect.center)
            self.rect = rect
            self.sprite.update(dt)
            self.sprite.set_angle(-math.degrees(self.angle))

        def get_draw_rect(self):
            rect = self.rect
            return rect

        def draw(self, surface, coords):
            self.sprite.draw(surface, coords)

    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2(0, 0)
            self.half_w = self.display_surface.get_size()[0] // 2
            self.half_h = self.display_surface.get_size()[1] // 2
            self.add_x = 0
            self.add_y = 0
            self.particle_player_color = (210, 210, 210, 255)

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
                            if (player.get_rect().bottom // size[1], player.get_rect().centerx // size[0]) == (row, col):
                                self.particle_player_color = layer[row][col].get_surf().get_at((player.get_rect().centerx % size[0], player.get_rect().bottom % size[1]))
                            self.display_surface.blit(layer[row][col].get_surf(), dest - self.offset)
            for partickle in particle_group:
                offset_pos = partickle.get_draw_rect().topleft - self.offset
                partickle.draw(self.display_surface, offset_pos)
                # pygame.draw.rect(screen, (0, 0, 0), (*offset_pos, partickle.rect.w, partickle.rect.h), 1)
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.get_draw_rect().topleft - self.offset
                sprite.draw(self.display_surface, offset_pos)
                real_pos = sprite.get_rect().topleft - self.offset
                coords = (real_pos[0], real_pos[1], sprite.rect.w, sprite.rect.h)
                pygame.draw.rect(screen, (255, 255, 255), coords, 1)

        def screen_to_wordl(self, coords):
            return coords + self.offset

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, speed, damage, type, coords, angle, time_disappear, image, *group):
            super().__init__(*group)
            self.x, self.y = coords
            self.angle = angle
            self.type = type
            self.time_disappear = pygame.time.get_ticks() + time_disappear * 1000
            self.surf = image
            if type != 'sword_attack':
                self.surf = pygame.transform.rotate(self.surf, -math.degrees(angle))
            if not self.surf.get_colorkey():
                self.surf.set_colorkey((0, 0, 0))
            self.rect = self.surf.get_rect()
            self.rect.center = coords
            self.speed = speed
            self.damage = damage

        def update(self, dt):
            self.x += math.cos(self.angle) * self.speed * dt
            self.y += math.sin(self.angle) * self.speed * dt
            self.rect.center = (self.x, self.y)
            if self.time_disappear <= pygame.time.get_ticks():
                self.kill()

        def collide_action(self):
            if self.type == "arrow":
                self.kill()
            else:
                pass

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
    particle_group = CameraGroup()
    camera_group = CameraGroup()
    enemy_bullets = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    player = Player(200, 100, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 38, 55), (64, 64), [], camera_group)
    player.set_cur_speed(120)
    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    game_over = None
    tmx_data = load_pygame('map/map.tmx')
    map = Map(tmx_data)
    levels = iter([first_level(), second_level(), third_level()])
    screen_messages = []
    score = 0
    cur_level_counter = 0
    previous_time = pygame.time.get_ticks()
    player_movement_registered = False
    first_update = True
    while running:
        clock.tick(60)
        dt = (pygame.time.get_ticks() - previous_time) / 1000
        previous_time = pygame.time.get_ticks()
        screen.fill((75, 122, 71))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                player_movement_registered = True
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_r:
                    if not player.bow:
                        if player.sword:
                            player.sword.kill()
                            player.sword = None
                        player.bow = Bow(pygame.Surface((40, 40)), player, None, 1, 500, player_bullets, camera_group)
                    else:
                        player.bow.kill()
                        player.bow = None
                elif event.key == K_t:
                    if not player.sword:
                        if player.bow:
                            player.bow.kill()
                            player.bow = None
                        sword_image = pygame.Surface((16, 64))
                        player.sword = Sword(sword_image, player, None, 1, (70, 70), player_bullets, camera_group)
                    else:
                        player.sword.kill()
                        player.sword = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.bow:
                    player.bow.bow_tense()
                elif player.sword:
                    player.sword.attack()
            elif event.type == QUIT:
                running = False
        if not game_over:
            if not enemies:
                cur_level_counter += 1
                wave = pygame.font.Font(None, 144).render(f'wave {cur_level_counter}', 1, (255, 255, 255))
                wave_2 = pygame.font.Font(None, 150).render(f'wave {cur_level_counter}', 1, (0, 0, 0))
                pos = screen.get_size()[0] // 2 - wave.get_width() // 2, screen.get_size()[1] // 2 - wave.get_height() * 2.5
                pos_2 = screen.get_size()[0] // 2 - wave_2.get_width() // 2, screen.get_size()[1] // 2 - wave_2.get_height() * 2.5
                screen_messages.append(((wave_2, pos_2, pygame.time.get_ticks(), 5000), (wave, pos, pygame.time.get_ticks(), 5000)))
                cur_level = next(levels, "end")
                timer = pygame.time.get_ticks()
                if cur_level == "end":
                    game_over = "victory"
                player_movement_registered = False
                first_update = True
                if not game_over:
                    player.physic_obg.x = cur_level[2][0]
                    player.physic_obg.y = cur_level[2][1]
                    player.update(dt)
                    timer += cur_level[1] * 1000
                    for enemy_inf in cur_level[0]:
                        enemy = Enemy(enemy_inf[0], enemy_inf[1], enemy_inf[2], enemy_inf[3], [player, *enemies],
                                      camera_group, enemies)
                        if enemy_inf[-2] == "sword":
                            sword_image = pygame.Surface((16, 64))
                            enemy.sword = Sword(sword_image, enemy, player, enemy_inf[-1], (70, 70), enemy_bullets,
                                                camera_group)
                        elif enemy_inf[-2] == "bow":
                            enemy.bow = Bow(pygame.Surface((40, 40)), enemy, player, enemy_inf[-1], 300, enemy_bullets,
                                            camera_group)
            if not game_over:
                if player_movement_registered or first_update:
                    camera_group.update(dt)
                    first_update = False
                particle_group.update(dt)
                camera_group.custom_draw(screen, map.get_layers(), player)
                for enemy in enemies:
                    if enemy.sword:
                        enemy.sword.attack()
                    if enemy.bow:
                        enemy.bow.bow_tense()
                    if (collided_sprite := pygame.sprite.spritecollideany(enemy, player_bullets)):
                        enemy.get_hit(collided_sprite.angle, collided_sprite.damage)
                        collided_sprite.collide_action()
                    if enemy.hp <= 0 and not enemy.death_flag:
                       enemy.death()
                       score += 100
                if (bullet := pygame.sprite.spritecollideany(player, enemy_bullets)):
                    player.hp -= bullet.damage
                    bullet.kill()
                for i in enemy_bullets:
                    if (bullet := pygame.sprite.spritecollideany(i, player_bullets)) and (i.type == 'sword_attack' or bullet.type == 'sword_attack'):
                        i.kill()
                        bullet.kill()
                if player.hp <= 0:
                    player.kill()
                    game_over = "Game over"
                for message_box in screen_messages:
                    for message in message_box:
                        screen.blit(message[0], message[1])
                        if pygame.time.get_ticks() - message[2] >= message[3]:
                            screen_messages.remove(message_box)
                            break
        else:
            running = False
            sum_score = int(open('score.txt', 'r').readline()) + score
            open('score.txt', 'w').write(str(sum_score))
            end(score)
        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()