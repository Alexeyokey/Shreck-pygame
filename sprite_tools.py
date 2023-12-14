import pygame
class Animation(object):
    def __init__(self, surface, sheet_size=(1, 1), frame_count=1, rect=None,
                 reverse_x=False, reverse_y=False, reverse_animation=False, colorkey=None, scale=1.0, start_frame=0):
        self.surface = surface
        self.reverse_x = reverse_x
        self.reverse_y = reverse_y
        self.reverse_animation = reverse_animation
        self.frame_count = frame_count
        self.colorkey = colorkey
        self.scale = scale
        self.frames = self.split(surface, sheet_size, frame_count, rect, scale)[start_frame:]
        self.frame_count -= start_frame

    @staticmethod
    def from_path(path, *args, **kwargs):
        return Animation(pygame.image.load(path), *args, **kwargs)

    def split(self, surface, sheet_size, frame_count, rect=None, scale=1.0):
        rect = (0, 0, surface.get_width(), surface.get_height()) if rect is None else rect
        rect = pygame.Rect(*rect)
        pixel_width, pixel_height = rect.width, rect.height
        frame_width = pixel_width // sheet_size[0]
        frame_height = pixel_height // sheet_size[1]
        frames = []
        frame_x = 0
        frame_y = 0
        for idx in range(frame_count):
            x_origin = frame_x * frame_width + rect[0]
            y_origin = frame_y * frame_height + rect[1]
            frame_rect = x_origin, y_origin, frame_width, frame_height
            new_frame = surface.subsurface(frame_rect)
            if self.reverse_x or self.reverse_y:
                new_frame = pygame.transform.flip(new_frame, self.reverse_x, self.reverse_y)
            else:
                new_frame = new_frame.copy()
            if self.colorkey:
                new_frame.set_colorkey(self.colorkey)
            if scale != 1.0:
                width = int(new_frame.get_width() * scale)
                height = int(new_frame.get_height() * scale)
                new_frame = pygame.transform.scale(new_frame, (width, height))
            frames.append(new_frame)
            frame_x += 1
            if frame_x > sheet_size[0]:
                frame_x = 0
                frame_y += 1
        if self.reverse_animation:
            frames = frames[::-1]

        return frames

    def reverse(self, x_bool, y_bool):
        for idx, frame in enumerate(self.frames):
            self.frames[idx] = pygame.transform.flip(frame, x_bool, y_bool)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, fps=12, position=(0, 0)):
        super().__init__()
        self.animations = {}
        self.animation_fps_overrides = {}
        self.animation_chain_mapping = {}
        self.animation_callbacks = {}
        self.animation_temporary_callbacks = {}

        self.image = None
        self.rect = None
        self.x, self.y = position

        self.angle = 0

        #   Set initial flags and values
        self.paused = False
        self.paused_at = 0
        self.active_animation_key = None

        #   Set frames per second
        self.fps = fps
        self.now = 0

    def add_animation(self, anim_dict, fps_override=None, loop=False):
        for name in anim_dict:
            self.animations[name] = anim_dict[name]
            if fps_override:
                self.animation_fps_overrides[name] = fps_override
            if loop:
                self.chain_animation(name, name)

    def start_animation(self, name, restart_if_active=True, clear_time=True):
        self.resume()
        if not restart_if_active and name == self.active_animation_key:
            return
        if clear_time:
            self.now = 0
        self.active_animation_key = name

    def get_frame_num(self):
        fps = self.fps
        if self.active_animation_key in self.animation_fps_overrides:
            fps = self.animation_fps_overrides[self.active_animation_key]
        frame_time = 1.0 / fps
        frame_number = int(self.now / frame_time)
        return frame_number

    def get_image(self):
        active_animation = self.animations[self.active_animation_key]
        frame_time = 1 / self.fps
        frame_number = self.get_frame_num()
        if frame_number >= active_animation.frame_count:
            new_animation_exists = self.on_animation_finished(self.active_animation_key)
            if not new_animation_exists:
                self.pause()
                self.now = frame_time * (len(active_animation.frames) - 0.5)
                return active_animation.frames[-1]
            self.now -= frame_time * active_animation.frame_count
            return self.get_image()

        image = active_animation.frames[frame_number]
        if self.angle != 0:
            image = pygame.transform.rotate(image, self.angle)
        return image

    def update_image(self):
        self.image = self.get_image()

    def set_angle(self, angle):
        self.angle = angle

    def draw(self, surface, coords):
        if self.active_animation_key not in self.animations:
            raise Sprite.InvalidAnimationKeyException(f"Animation key {self.active_animation_key} has not been added.")
        if not self.image:
            self.image = self.get_image()
        surface.blit(self.image, coords)

    def pause(self):
        """ Pause the active animation. """
        self.paused = True

    def resume(self):
        """ Resume the active animation. """
        self.paused = False

    def update(self, dt):
        """ Updates the animation with a time step of dt. """
        if not self.paused:
            self.now += dt

        self.image = self.get_image()
        w = self.image.get_width()
        h = self.image.get_height()
        x = int(self.x - w / 2)
        y = int(self.y - h / 2)
        self.rect = pygame.Rect(x, y, w, h)

    def set_position(self, pos):
        """ Sets the position of the sprite on the screen. """
        self.x, self.y = pos

    def add_callback(self, animation_key, callback, args=None, kwargs=None, temporary=False):
        args = args if args else ()
        kwargs = kwargs if kwargs else {}
        if temporary:
            callback_dict = self.animation_temporary_callbacks
        else:
            callback_dict = self.animation_callbacks
        if animation_key not in callback_dict:
            callback_dict[animation_key] = []
        callback_dict[animation_key].append((callback, args, kwargs))

    def chain_animation(self, previous_animation, next_animation):
        self.animation_chain_mapping[previous_animation] = next_animation

    def on_animation_finished(self, animation_key):
        self.run_callbacks(animation_key)
        next_animation = self.get_next_animation(animation_key)
        if next_animation:
            self.start_animation(next_animation, restart_if_active=True, clear_time=False)
            return True
        return False

    def run_callbacks(self, animation_key):
        if animation_key in self.animation_temporary_callbacks:
            for callback, args, kwargs in self.animation_temporary_callbacks[animation_key]:
                callback(*args, **kwargs)
            del self.animation_temporary_callbacks[animation_key]  # Temporary callbacks should only be run once
        if animation_key in self.animation_callbacks:
            for callback, args, kwargs in self.animation_callbacks[animation_key]:
                callback(*args, **kwargs)

    def get_next_animation(self, animation_key):
        if animation_key in self.animation_chain_mapping:
            return self.animation_chain_mapping[animation_key]
        return None

    class InvalidAnimationKeyException(IndexError):
        pass

