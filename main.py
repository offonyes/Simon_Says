import pygame, random
from sprites import *
from setting import *

class Game:
    def __init__(self): #DONE
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.colours = [GREEN,RED, YELLOW, BLUE]
        self.dark_colours = [DARKGREEN,DARKRED, DARKYELLOW, DARKBLUE]
        self.flash = [Flash(0,0,WIDTH,HEIGHT,WHITE,3,self.screen)]
        self.buttons = [Button(110,30,DARKGREEN),Button(330,30,DARKRED),Button(110,250,DARKYELLOW),Button(330,250,DARKBLUE)]

    def get_max_score(self): #DONE
        with open("max_score.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self): #DONE
        with open("max_score.txt", "w") as file:
            if self.score > self.max_score:
                self.max_score = self.score
            file.write(str(self.max_score))
    def new(self):
        self.waiting_player = False
        self.order = []
        self.current_step = 0
        self.score = 0
        self.max_score = self.get_max_score()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()

    def update(self): #HALFDONE
        if not self.waiting_player:
            pygame.time.wait(1000) #time between stages
            self.order.append(random.choice(self.dark_colours))
            for button in self.order:
                self.button_animation(button)
                pygame.time.wait(250) # Time between animation button
            self.waiting_player = True
        
        else:
            # pushed the correct button
            if self.clicked_button and self.clicked_button == self.order[self.current_step]:
                self.button_animation(self.clicked_button)
                self.current_step += 1

                # pushed the last button
                if self.current_step == len(self.order):
                    self.score += 1
                    self.waiting_player = False
                    self.current_step = 0

            # pushed the wrong button
            elif self.clicked_button and self.clicked_button != self.order[self.current_step]:
                self.flash[0].animation()
                self.save_score()
                self.playing = False

    def draw(self):
        self.screen.fill((40, 40, 40))
        TextOnScreen(170, 480, f"Score: {str(self.score)}").draw(self.screen)
        TextOnScreen(370, 480, f"High score: {str(self.max_score)}").draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()
    
    def button_animation(self, colour): #DONE
        for i in range(len(self.colours)):
                if self.dark_colours[i] == colour:
                    colour = self.colours[i]
                    button = self.buttons[i]
        button_flash = Flash(button.x,button.y,SIZE_OF_BUTTON,SIZE_OF_BUTTON,colour,1,self.screen)
        button_flash.animation()

    def events(self): #DONE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button.colour
        

game = Game()

while True:
    game.new()
    game.run()