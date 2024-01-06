import random
import pygame
import math
from map import Map
from entities import PhysicsObj, Entity
from particles import create_particles
from scripts import get_angle_between, load_image, magnitude, scale_to
from sprite_tools import Sprite, Animation
from levels import *
from pytmx.util_pygame import load_pygame
from gui_elements import Button
from pygame.locals import (K_t, K_r, K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_q, KEYDOWN, QUIT)
import pygame_gui
from pygame_gui.core import ObjectID

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme_for_button.json')
pygame.mixer.music.load('shrek_09. Smash Mouth - All Star.mp3')
vol = 1
sensitivity_multiplier = 1


def start():
    global manager
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')
    # pygame.mixer.music.play() # Пока в разработке на 0 потом на 1 поставим

    background_image = pygame.image.load("sprites/background_.jpg").convert()

    welcome = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 450, 150), (900, 100)),
        text="Welcome to Shreck",
        manager=manager,
        object_id="#label"
    )

    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 98, SCREEN_HEIGHT // 2), (196, 84)),
        text='Play',
        manager=manager,
        object_id="#button"
    )

    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 98, SCREEN_HEIGHT // 2 + 100), (196, 84)),
        text='Settings',
        manager=manager,
        object_id="#button"
    )

    statistic_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 98, SCREEN_HEIGHT // 2 + 200), (196, 84)),
        text='Statistic',
        manager=manager,
        object_id="#long_text"
    )

    # back_button = pygame_gui.elements.UIButton(
    #     relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 98, SCREEN_HEIGHT // 2 + 200),
    #                               (196, 84)),
    #     text='back',
    #     manager=manager,
    #     object_id="#backbutton"
    # )
    # rating_btn = pygame_gui.elements.UIButton(
    #     relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 98, 500), (196, 84)),
    #     text='Rating',
    #     manager=manager,
    #     object_id="#button"
    # )

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
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_btn:
                        menu = False
                        main()
                    elif event.ui_element == settings_btn:
                        menu = False
                        settings()
                    # elif event.ui_element == rating_btn:
                    #     menu = False
                    #     rating()
                    elif event.ui_element == statistic_btn:
                        menu = False
                        statistic(open('stat.txt', 'r').readline().split())
            manager.process_events(event)
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()


def settings():
    global manager, vol, sensitivity_multiplier
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')

    background_image = pygame.image.load("sprites/background_.jpg").convert()
    common_button_size = (100, 100)
    MIDDLE_SCREEN_w = SCREEN_WIDTH // 2

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 90), (800, 100)),
        text=f"Settings",
        manager=manager,
        object_id="#label"
    )

    sound_lbl = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, SCREEN_HEIGHT // 2 - 100), (800, 100)),
        text="Sound",
        manager=manager,
        object_id="#little_label"
    )

    sub_volume = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((MIDDLE_SCREEN_w - 1.5 * common_button_size[0], SCREEN_HEIGHT // 2),
                                  common_button_size),
        text='',
        manager=manager,
        object_id="#leftarrowbutton"
    )

    mute_volume = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((MIDDLE_SCREEN_w - common_button_size[0] // 2, SCREEN_HEIGHT // 2), (100, 100)),
        text='',
        manager=manager,
        object_id="#pausebutton"
    )

    add_volume = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((MIDDLE_SCREEN_w + common_button_size[0] // 2, SCREEN_HEIGHT // 2),
                                  common_button_size),
        text='',
        manager=manager,
        object_id="#rightarrowbutton"
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((MIDDLE_SCREEN_w - 98, SCREEN_HEIGHT // 2 + 200), (196, 84)),
        text='Back',
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
            if event.type == pygame.USEREVENT:
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
                        elif event.ui_element == back_button:
                            setting = False
                            start()
            manager.process_events(event)
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()


def end(score):
    global manager
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')
    background_image = pygame.image.load("sprites/background_.jpg").convert()

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240 - 50, 190), (900, 100)),
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
        text='Back to menu',
        manager=manager,
        object_id="#long_text"
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
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()


def statistic(*stat_data):
    global manager
    manager.clear_and_reset()
    manager.get_theme().load_theme('theme_for_button.json')
    background_image = pygame.image.load("sprites/background_.jpg").convert()

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((240, 90), (800, 100)),
        text=f"Statistic",
        manager=manager,
        object_id="#label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((440, 190), (400, 100)),
        text=f"Kills",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((400, 290), (120, 50)),
        text=f"Bow",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((750, 290), (100, 50)),
        text=f"{stat_data[0][0]}",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((405, 340), (185, 50)),
        text=f"Sword",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((750, 340), (100, 50)),
        text=f"{stat_data[0][1]}",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((405, 390), (120, 50)),
        text=f"All",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((750, 390), (100, 50)),
        text=f"{stat_data[0][2]}",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((405, 490), (185, 100)),
        text=f"Score",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((737, 490), (200, 100)),
        text=f"{stat_data[0][4]}",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((405, 540), (190, 100)),
        text=f"Deaths",
        manager=manager,
        object_id="#little_label"
    )

    info = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((750, 540), (100, 100)),
        text=f"{stat_data[0][3]}",
        manager=manager,
        object_id="#little_label"
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
        screen.blit(background_image, [0, 0])
        manager.draw_ui(screen)
        manager.update(time_delta)
        pygame.display.flip()
        pygame.display.update()


def main():
    class Enemy(Entity):
        def __init__(self, speed, hp, coords, image_shape, knight_name, group_to_collide, *group):
            super().__init__(speed, hp, (coords[0], coords[1], image_shape[0], image_shape[1]), image_shape,
                             group_to_collide, *group)
            self.surf = pygame.Surface(image_shape)
            self.surf.set_colorkey((0, 0, 0))
            self.rect = pygame.Rect((coords[0], coords[1], image_shape[0], image_shape[1]))
            self.rect.topleft = coords
            self.sprite = Sprite(8)
            self.death_flag = False
            wait_right = Animation.from_path(f'sprites/{knight_name}_wait.png', (4, 1), 4, reverse_x=False,
                                             colorkey=(0, 0, 0),
                                             scale=2.5)
            wait_left = Animation.from_path(f'sprites/{knight_name}_wait.png', (4, 1), 4, reverse_x=True,
                                            colorkey=(0, 0, 0),
                                            scale=2.5)
            run_right = Animation.from_path(f'sprites/{knight_name}_run.png', (4, 1), 4, reverse_x=False,
                                            colorkey=(0, 0, 0),
                                            scale=2.5)
            run_left = Animation.from_path(f'sprites/{knight_name}_run.png', (4, 1), 4, reverse_x=True,
                                           colorkey=(0, 0, 0),
                                           scale=2.5)
            damage_right = Animation.from_path(f'sprites/{knight_name}_damage.png', (4, 1), 3, reverse_x=False,
                                               colorkey=(0, 0, 0),
                                               scale=2.5)
            damage_left = Animation.from_path(f'sprites/{knight_name}_damage.png', (4, 1), 3, reverse_x=True,
                                              colorkey=(0, 0, 0),
                                              scale=2.5)
            death_right = Animation.from_path(f'sprites/{knight_name}_death.png', (4, 1), 4, reverse_x=False,
                                              colorkey=(0, 0, 0),
                                              scale=2.5)
            death_left = Animation.from_path(f'sprites/{knight_name}_death.png', (4, 1), 4, reverse_x=True,
                                             colorkey=(0, 0, 0),
                                             scale=2.5)
            self.sprite.add_animation({"wait_r": wait_right, "wait_l": wait_left,
                                       "run_r": run_right, "run_l": run_left}, loop=True)
            self.sprite.add_animation({"damage_r": damage_right, "damage_l": damage_left,
                                       "death_r": death_right, "death_l": death_left}, loop=False, inevitable=True)
            self.sprite.add_callback('damage_r', self.check_death_and_kill)
            self.sprite.add_callback('damage_l', self.check_death_and_kill)
            self.sprite.add_callback('death_l', self.kill)
            self.sprite.add_callback('death_r', self.kill)
            left_or_right = random.randint(0, 1)
            self.cur_state = 'wait'
            self.direction = 'l' if left_or_right else 'r'
            self.sprite.start_animation("wait_l" if left_or_right else "wait_r", restart_if_active=True)

        def update(self, dt, x_player, y_player):
            x, y = self.rect.center
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
            self.update_animation(dt, dif_x, dif_y)
            return dif_x, dif_y

        def update_animation(self, dt, dif_x, dif_y):
            self.sprite.update(dt)
            self.animation(dif_x, dif_y)

        def animation(self, dif_x, dif_y):
            if self.get_rect().centerx <= player.get_rect().centerx:
                self.direction = 'r'
            elif self.get_rect().centerx > player.get_rect().centerx:
                self.direction = 'l'
            self.sprite.start_animation(self.cur_state + '_' + self.direction, restart_if_active=False)

        def move(self, movement, objects):
            collisions = self.physic_obj.move(movement, objects)
            self.rect.x = self.physic_obj.x
            self.rect.y = self.physic_obj.y
            return collisions

        def get_hit(self, angle, damage):
            self.hp -= damage
            self.move((math.cos(angle) * 10, math.sin(angle) * 10), self.group_to_collide)
            self.sprite.start_animation("damage_" + self.direction)

        def check_death_and_kill(self):
            if self.death_flag:
                self.cur_state = 'death'

        def get_draw_rect(self):
            return pygame.Rect(self.rect.x - 20, self.rect.y - 30, self.rect.w, self.rect.h)

    class SwordEnemy(Enemy):
        def __init__(self, speed, hp, coords, image_shape, group_to_collide, *group):
            super().__init__(speed, hp, coords, image_shape, "knight", group_to_collide, *group)
            self.sword = None
            self.cooldown_sword = 300

        def update(self, dt):
            x_player, y_player = player.rect.center
            dif_x, dif_y = super().update(dt, x_player, y_player)
            if self.death_flag:
                dif_x, dif_y = -dif_x, -dif_y
            self.move((dif_x, dif_y), self.group_to_collide)

        def attack(self):
            if self.sword:
                self.sword.try_attack()

        def death(self):
            if enemy.sword:
                enemy.sword.kill()
                enemy.sword = None
            self.death_flag = True

    class ArcherEnemy(Enemy):
        def __init__(self, speed, hp, coords, image_shape, group_to_collide, *group):
            super().__init__(speed, hp, coords, image_shape, "knight", group_to_collide, *group)
            self.bow = None

        def update(self, dt):
            x, y = self.rect.center
            x_player, y_player = player.rect.center
            dif_x, dif_y = super().update(dt, x_player, y_player)
            if self.bow and abs(x_player - x) <= 200 and abs(y_player - y) <= 200 or self.death_flag:
                dif_x, dif_y = -dif_x, -dif_y
            else:
                dif_x, dif_y = 0, 0
            self.move((dif_x, dif_y), self.group_to_collide)

        def attack(self):
            if self.bow:
                self.bow.bow_tense()

        def death(self):
            if enemy.bow:
                enemy.bow.kill()
                enemy.bow = None
            self.death_flag = True

    class FastEnemy(Enemy):
        def __init__(self, speed, hp, coords, image_shape, group_to_collide, *group):
            super().__init__(speed, hp, coords, image_shape, "green_knight", group_to_collide, *group)
            self.can_attack = False
            self.reverse_for_charge = False
            self.velocity = pygame.Vector2((0, 0))
            self.cooldown_sword = 185

        def update(self, dt):
            enemy_vector = pygame.Vector2(self.rect.center)
            player_vector = pygame.Vector2(player.rect.center)
            dp = player_vector - enemy_vector
            mean_mag = 1
            if magnitude(dp) > 0:
                dp = scale_to(dp, mean_mag, magnitude(dp))
            self.velocity += dp * dt * self.cur_speed / (10 * self.cur_speed // 100 / 2)
            self.can_attack = False
            if magnitude(self.velocity) > self.cur_speed * dt:
                self.velocity = scale_to(self.velocity, self.cur_speed * dt, magnitude(self.velocity))
                self.can_attack = True
                self.reverse_for_charge = False
            self.velocity *= 0.5 ** dt
            x_vel, y_vel = self.velocity[0], self.velocity[1]
            self.update_animation(dt, x_vel, y_vel)
            if self.reverse_for_charge:
                x_vel, y_vel = -x_vel, -y_vel
            self.move((x_vel, y_vel), self.group_to_collide)

        def move(self, coords, objects):
            collisions = super().move(coords, self.group_to_collide)
            self.attack(collisions)

        def attack(self, collisions=None):
            if collisions:
                for i in collisions["data"]:
                    if i[0] == player.rect:
                        if self.can_attack:
                            player.additional_force = self.velocity * 30
                            player.get_hit(0, 50)
                            self.velocity = pygame.Vector2(0, 0)
                        else:
                            player.additional_force = self.velocity * 10
                            player.get_hit(0, 10)
                            self.reverse_for_charge = True

        def death(self):
            self.death_flag = True

    class Player(Entity):
        def __init__(self, speed, hp, rect, image_shape, group_to_collide, *group):
            super().__init__(speed, hp, rect, image_shape, group_to_collide, *group)
            self.animation_flag = True
            self.particle_flag = False
            self.last_direction = [0, 0]
            self.bow = None
            self.sword = None
            self.cooldown_sword = 0
            self.sprite = Sprite(8)
            self.particle_time_start = None
            self.movement = pygame.Vector2((0, 0))
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
            self.movement = self.direction / direction_restrict * self.cur_speed * dt
            self.move(self.movement, self.group_to_collide)
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
                create_particles(pos, camera_group.particle_player_color, ((3, 3), (4, 4)), range(200, 400),
                                 range(0, 100), x_direction, y_direction, 10, 0.1, particle_group)

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
            collisions = super().move(movement, objects)
            for i in collisions['data']:
                if i[2] in collide_objects:
                    self.hp -= 10
                    super().move(-self.direction / 100 * 50, objects)
                    break

        def get_hit(self, angle, damage):
            self.hp -= damage
            self.move((math.cos(angle) * 10, math.sin(angle) * 10), self.group_to_collide)

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
            self.sprite = None
            self.rotated_surf = self.image.copy()
            self.rect = self.rotated_surf.get_rect()
            self.rect.center = self.entity.rect.center
            self.shot_delay = shot_delay * 1000
            self.timer = pygame.time.get_ticks()
            self.angle = 0

        def get_rect(self):
            return self.rect

        def draw(self, surface, coords):
            self.sprite.draw(surface, coords)

        def get_draw_rect(self):
            return self.rect

        def get_surf(self):
            return self.rotated_surf

    class Sword(Weapon):
        def __init__(self, image, entity, target, shot_delay, damage_area, attacking_group, *group):
            super().__init__(image, entity, target, shot_delay, attacking_group, *group)
            self.damage_area = damage_area
            self.attack_flag = False
            self.attack_timer = None
            self.sprite = Sprite(4)
            self.direction = 'right'
            self.state = 'idle'
            idle_left = Animation.from_path('sprites/sword.png', reverse_x=True, scale=2)
            idle_right = Animation.from_path('sprites/sword.png', reverse_x=False, scale=2)
            attack_right = Animation.from_path('sprites/attacking_sword.png', (4, 1), 4, reverse_x=False, scale=2)
            attack_left = Animation.from_path('sprites/attacking_sword_left.png', (4, 1), 4, reverse_x=False, scale=2,
                                              reverse_animation=True)
            self.sprite.add_animation({"idle_left": idle_left, "idle_right": idle_right}, loop=True, fps_override=1)
            self.sprite.add_animation({"attack_right": attack_right, "attack_left": attack_left}, loop=False)
            self.sprite.add_callback('attack_right', self.change_to_idle)
            self.sprite.add_callback('attack_left', self.change_to_idle)
            self.sprite.start_animation('idle_right')

        def change_to_idle(self):
            self.state = 'idle'

        def try_attack(self):
            if self.target:
                dif_x = abs(self.target.rect.centerx - self.entity.rect.centerx)
                dif_y = abs(self.target.rect.centery - self.entity.rect.centery)
            if self.timer < pygame.time.get_ticks() and (
                    not self.target or dif_x <= self.damage_area[0] and dif_y <= self.damage_area[1]):
                self.attack_flag = True
                self.attack_timer = pygame.time.get_ticks() + self.entity.cooldown_sword
                self.timer = pygame.time.get_ticks() + self.shot_delay

        def attack(self):
            self.state = 'attack'
            coords = pygame.Vector2(self.entity.rect.center)
            coords[0] += math.cos(self.angle) * 60
            coords[1] += math.sin(self.angle) * 50
            Bullet(0, 100, "sword_attack", coords, self.angle, 0.02, pygame.Surface(self.damage_area),
                   self.attacking_group, self.group)
            self.attack_flag = False

        def update(self, dt):
            if self.attack_flag and self.attack_timer < pygame.time.get_ticks():
                self.attack()
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
            self.sprite.add_animation({"idle": idle}, fps_override=1)
            self.sprite.add_animation({"attack": attack})
            self.sprite.start_animation('idle')
            self.sprite.add_callback("attack", lambda: self.shoot(self.arrow_speed))
            self.sprite.add_callback("attack", lambda: self.sprite.start_animation('idle'))

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
            self.sprite.set_angle(-math.degrees(self.angle))
            self.sprite.update(dt)

        def get_draw_rect(self):
            rect = self.rect
            return rect

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
                            if (player.get_rect().bottom // size[1], player.get_rect().centerx // size[0]) == (
                                    row, col):
                                self.particle_player_color = layer[row][col].get_surf().get_at(
                                    (player.get_rect().centerx % size[0], player.get_rect().bottom % size[1]))
                            self.display_surface.blit(layer[row][col].get_surf(), dest - self.offset)
            for partickle in particle_group:
                offset_pos = partickle.get_draw_rect().topleft - self.offset
                partickle.draw(self.display_surface, offset_pos)
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.get_draw_rect().topleft - self.offset
                sprite.draw(self.display_surface, offset_pos)
                real_pos = sprite.get_rect().topleft - self.offset
                coords = (real_pos[0], real_pos[1], sprite.rect.w, sprite.rect.h)
                # pygame.draw.rect(screen, (255, 255, 255), coords, 1)

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
    bow_in_hands = False
    sword_in_hands = False
    tmx_data = load_pygame('map/map.tmx')
    map = Map(tmx_data)
    collide_objects = pygame.sprite.Group()
    for layer in map.get_collision_layers():
        for row in range(layer.height()):
            for col in range(layer.width()):
                if layer[row][col]:
                    collide_objects.add(layer[row][col])
    enemies = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()
    camera_group = CameraGroup()
    enemy_bullets = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    player = Player(200, 100, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 38, 55), (64, 64), [*collide_objects],
                    camera_group)
    clock = pygame.time.Clock()
    timer = pygame.time.get_ticks()
    game_over = None
    levels = iter([level_1(), level_2(), level_3(), level_4(), level_5(), level_6(), level_7()])
    screen_messages = []
    score = 0
    cur_level_counter = 0
    previous_time = pygame.time.get_ticks()
    player_movement_registered = False
    first_update = True

    str_with_stat = open('stat.txt', 'r').readline().split()

    bow_kills = int(str_with_stat[0])
    sword_kills = int(str_with_stat[1])
    all_kills = int(str_with_stat[2])
    all_deaths = int(str_with_stat[3])
    all_score = int(str_with_stat[4])
    while running:
        clock.tick(60)
        dt = (pygame.time.get_ticks() - previous_time) / 1000
        previous_time = pygame.time.get_ticks()
        screen.fill((75, 122, 71))
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key != 1073742085:
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
                    player.sword.try_attack()
            elif event.type == QUIT:
                running = False
        if not game_over:
            if not enemies:
                cur_level_counter += 1
                score_for_file = max(int(open('score.txt', 'r').readlines()[0]), cur_level_counter)
                open('score.txt', 'w').write(str(score_for_file - 1))
                wave = pygame.font.Font(None, 144).render(f'wave {cur_level_counter}', 1, (255, 255, 255))
                wave_2 = pygame.font.Font(None, 150).render(f'wave {cur_level_counter}', 1, (0, 0, 0))
                pos = screen.get_size()[0] // 2 - wave.get_width() // 2, screen.get_size()[
                    1] // 2 - wave.get_height() * 2.5
                pos_2 = screen.get_size()[0] // 2 - wave_2.get_width() // 2, screen.get_size()[
                    1] // 2 - wave_2.get_height() * 2.5
                screen_messages.append(
                    ((wave_2, pos_2, pygame.time.get_ticks(), 5000), (wave, pos, pygame.time.get_ticks(), 5000)))
                cur_level = next(levels, "end")
                timer = pygame.time.get_ticks()
                if cur_level == "end":
                    game_over = "victory"
                player_movement_registered = False
                first_update = True
                if not game_over:
                    player.physic_obj.x = cur_level[2][0]
                    player.physic_obj.y = cur_level[2][1]
                    player.hp = 100
                    player.update(dt)
                    timer += cur_level[1] * 1000
                    for enemy_inf in cur_level[0]:
                        if enemy_inf[0] == "swordsman":
                            enemy = SwordEnemy(enemy_inf[1], enemy_inf[2], enemy_inf[3], enemy_inf[4],
                                               [player, *enemies, *collide_objects],
                                               camera_group, enemies)
                            sword_image = pygame.Surface((16, 64))
                            enemy.sword = Sword(sword_image, enemy, player, enemy_inf[-1], (70, 70), enemy_bullets,
                                                camera_group)
                        elif enemy_inf[0] == "archer":
                            enemy = ArcherEnemy(enemy_inf[1], enemy_inf[2], enemy_inf[3], enemy_inf[4],
                                                [player, *enemies, *collide_objects],
                                                camera_group, enemies)
                            enemy.bow = Bow(pygame.Surface((40, 40)), enemy, player, enemy_inf[-1], 300, enemy_bullets,
                                            camera_group)
                        elif enemy_inf[0] == 'green_swordsman':
                            enemy = FastEnemy(enemy_inf[1], enemy_inf[2], enemy_inf[3], enemy_inf[4],
                                              [player, *enemies, *collide_objects],
                                              camera_group, enemies)
            if not game_over:
                if player_movement_registered or first_update:
                    camera_group.update(dt)
                    first_update = False
                particle_group.update(dt)
                camera_group.custom_draw(screen, map.get_layers(), player)
                for enemy in enemies:
                    enemy.attack()
                    if (collided_sprite := pygame.sprite.spritecollideany(enemy, player_bullets)):
                        enemy.get_hit(collided_sprite.angle, collided_sprite.damage)
                        collided_sprite.collide_action()
                    if enemy.hp <= 0 and not enemy.death_flag:
                        enemy.death()
                        score += 100
                        if player.bow:
                            str_with_stat = open('stat.txt', 'r').readline().split()
                            bow_kills = int(str_with_stat[0]) + 1
                            open('stat.txt', 'w').write(f"{bow_kills} {sword_kills} {all_kills} {all_deaths} {score}")
                        if player.sword:
                            str_with_stat = open('stat.txt', 'r').readline().split()
                            sword_kills = int(str_with_stat[1]) + 1
                            open('stat.txt', 'w').write(f"{bow_kills} {sword_kills} {all_kills} {all_deaths} {score}")
                        str_with_stat = open('stat.txt', 'r').readline().split()
                        all_kills = int(str_with_stat[2]) + 1
                        open('stat.txt', 'w').write(f"{bow_kills} {sword_kills} {all_kills} {all_deaths} {score}")
                if (bullet := pygame.sprite.spritecollideany(player, enemy_bullets)):
                    player.get_hit(bullet.angle, bullet.damage)
                    bullet.kill()
                for i in enemy_bullets:
                    if (bullet := pygame.sprite.spritecollideany(i, player_bullets)) and (
                            i.type == 'sword_attack' or bullet.type == 'sword_attack'):
                        i.kill()
                if player.hp <= 0:
                    player.kill()
                    game_over = "Game over"
                    str_with_stat = open('stat.txt', 'r').readline().split()
                    all_deaths = int(str_with_stat[3]) + 1
                    all_score = int(str_with_stat[4]) + score
                    open('stat.txt', 'w').write(f"{bow_kills} {sword_kills} {all_kills} {all_deaths} {score}")
                for message_box in screen_messages:
                    for message in message_box:
                        screen.blit(message[0], message[1])
                        if pygame.time.get_ticks() - message[2] >= message[3]:
                            screen_messages.remove(message_box)
                            break
        else:
            running = False
            end(score)
        pygame.display.flip()


if __name__ == "__main__":
    start()
    pygame.quit()
