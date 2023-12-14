import pygame
import random


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, scales, dx, dy, duration, *groups):
        super().__init__(*groups)
        surf = pygame.Surface((5, 5))
        surf.fill(color)
        part = [surf]
        for scale in scales:
            part.append(pygame.transform.scale(part[0], (scale[0], scale[1])))
        self.image = random.choice(part)
        self.rect = self.image.get_rect()
        self.v = [dx, dy]
        self.rect.centerx, self.rect.centery = pos
        self.x, self.y = self.rect.topleft
        self.start_time = pygame.time.get_ticks()
        self.duration = duration * 1000

    def update(self, dt) -> None:
        self.x += self.v[0] * dt
        self.y -= self.v[1] * dt
        self.rect.topleft = (self.x, self.y)
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.kill()

    def get_rect(self):
        return self.rect

    def get_draw_rect(self):
        return self.rect

    def draw(self, screen, pos):
        screen.blit(self.image, pos)


def create_particles(position, color,  scales, vel_range_x, vel_range_y, x_direction, y_direction, count, duration, *groups):
    particle_color = [0, 0, 0, 255]
    for i in range(3):
        if color[i] - 20 >= 0:
            particle_color[i] = color[i] - 20
        else:
            particle_color[i] = color[i]
    for _ in range(count):
        Particle(position, particle_color, scales, random.choice(vel_range_x) * x_direction, random.choice(vel_range_y) * y_direction, duration, *groups)