import pygame
from setting import *
clock = pygame.time.Clock()
#button class
class Button:
    def __init__(self, x, y, colour,size_x,size_y):
        self.x, self.y = x, y
        self.colour = colour
        self.size_x, self.size_y = size_x,size_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour,(self.x, self.y, self.size_x, self.size_y))

    def clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.size_x and self.y <= mouse_y <= self.y + self.size_y
    
    def draw_rounden(self, screen):
        pygame.draw.ellipse(screen, self.colour,(self.x, self.y, self.size_x, self.size_y))


class TextOnScreen:
    def __init__(self, x, y, text,size,color):
        self.x, self.y = x, y
        self.text = text
        self.size = size
        self.color = color

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", self.size)
        text = font.render(self.text, True, self.color)
        screen.blit(text, (self.x, self.y))

class Flash:
    def __init__(self,x,y,size_x,size_y,colour,repeat,screen):
        self.x , self.y = x,y
        self.size_x, self.size_y = size_x, size_y 
        self.colour = colour 
        self.repeat = repeat
        self.screen = screen
    def animation(self):
        main_screen = self.screen.copy()
        flashing = pygame.Surface((self.size_x,self.size_y))
        flashing = flashing.convert_alpha()
        r, g, b = self.colour
        for _ in range(self.repeat):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    self.screen.blit(main_screen, (0, 0))
                    flashing.fill((r, g, b, alpha))
                    self.screen.blit(flashing, (self.x, self.y))
                    pygame.display.update()
                    clock.tick(60)
        self.screen.blit(main_screen, (0, 0))