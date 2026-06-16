import pygame

pygame.init()
FONT = pygame.font.Font(None, 32)
PANEL_COLOR = (50, 50, 50)

class Chat:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h) # (x, y, width, height)
        self.lines = [f"This is log message number {i}" for i in range(1, 5)]
        self.line_height = FONT.get_linesize()
        self.text_surface = pygame.Surface((self.rect.width, len(self.lines) * self.line_height), pygame.SRCALPHA)
        
        
        self.scroll_y = 0
        self.max_scroll = max(0, self.text_surface.get_height() - self.rect.height)

        for index, line in enumerate(self.lines):
            text_obj = FONT.render(line, True, (255,255,255))
            self.text_surface.blit(text_obj, (10, index * self.line_height))


    def Add(self, line, color):
        print(line)
        self.lines.append(line)
        text_obj = FONT.render(line, True, (255, 255, 255))
        
        temp = pygame.Surface((self.rect.width, len(self.lines) * self.line_height), pygame.SRCALPHA)
        temp.blit(self.text_surface, (0,0))
        temp.blit(text_obj, (10, (len(self.lines) - 1) * self.line_height))
        
        self.text_surface = temp
        
        self.max_scroll = max(0, self.text_surface.get_height() - self.rect.height)


    def Draw(self, screen):
        pygame.draw.rect(screen, PANEL_COLOR, self.rect)
        viewport = pygame.Rect(0, self.scroll_y, self.rect.width, self.rect.height)
        screen.blit(self.text_surface, (self.rect.x, self.rect.y), viewport)

    def Event_Handle(self, event):
        if event.type == pygame.MOUSEWHEEL:
            # Scroll up or down (y value is 1 for up, -1 for down)
            self.scroll_y -= event.y * 30 
            
            # 4. Constrain scrolling between 0 and max_scroll
            self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))