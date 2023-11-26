import pygame

class Button:
    def create_button(self, screen, color, x, y, button_size, text, width):
        self.screen = screen
        self.color = color
        self.x, self.y = x, y
        self.width = width
        self.length, self.height, self.text = button_size[0], button_size[1], text
        self.rect = pygame.Rect(x,y, button_size[0], button_size[1])
        return screen

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.length, self.height), self.width)
        self.screen.blit(self.text, (self.x + self.length // 2 - self.text.get_width() // 2,
                                     self.y + self.height // 2 - self.text.get_height() // 2))

    def pressed(self, mouse):
        if (mouse[0] > self.rect.topleft[0] and mouse[1] > self.rect.topleft[1] and mouse[0] < self.rect.bottomright[0]
                and mouse[1] < self.rect.bottomright[1]):
            return True
        else:
            return False