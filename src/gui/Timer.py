import pygame

pygame.init()
FONT = pygame.font.Font(None, 128)
PANEL_COLOR = (50, 50, 50)

class Timer:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h) # (x, y, width, height)
        self.time = 'test'
        
        self.text_surface = FONT.render(self.time, True, (0, 0, 0))

    def set_time(self, time):
        self.time = str(time)
        self.text_surface = FONT.render(self.time, True, (0, 0, 0))

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.text_surface, (self.rect.x + self.rect.width / 2 - 30, self.rect.y + self.rect.height / 2 - 30))
        # Blit the rect.
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)