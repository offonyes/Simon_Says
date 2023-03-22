import pygame, random
from sprites import *
from setting import *
status = "New_open"
logo = pygame.image.load("download-removebg-preview.png")
logo = pygame.transform.scale(logo,(600,90))
class Game:
    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.colours = [GREEN,RED, YELLOW, BLUE]
        self.dark_colours = [DARKGREEN,DARKRED, DARKYELLOW, DARKBLUE]
        self.flash = [Flash(0,0,WIDTH,HEIGHT,WHITE,3,self.screen)]
        self.buttons = [Button(110,30,DARKGREEN,SIZE_OF_BUTTON,SIZE_OF_BUTTON),Button(330,30,DARKRED,SIZE_OF_BUTTON,SIZE_OF_BUTTON),Button(110,250,DARKYELLOW,SIZE_OF_BUTTON,SIZE_OF_BUTTON),Button(330,250,DARKBLUE,SIZE_OF_BUTTON,SIZE_OF_BUTTON)]
        self.sound = [pygame.mixer.Sound(i) for i in audio_files]
        [self.sound[i].set_volume(0.015) for i in range(4)]
        self.loss_sound = pygame.mixer.Sound("Sound\Loss_sound.wav")
        self.loss_sound.set_volume(0.015)
        self.start_button = Button(100,250,DARKGREEN,440,100)

    def get_max_score(self): 
        with open("max_score.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self): 
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

    def start(self):
        self.max_score = self.get_max_score()
        self.screen.fill((40, 40, 40))
        self.screen.blit(logo,(20,50))
        self.start_button.draw(self.screen)
        TextOnScreen(230, 270, "START",70,RED).draw(self.screen)
        TextOnScreen(440, 480, f"High score: {str(self.max_score)}",24,WHITE).draw(self.screen)
        pygame.display.update()
        self.events()
        
    def update(self):
        if not self.waiting_player:
            pygame.time.wait(1000) #time between stages
            self.order.append(random.choice(self.dark_colours))
            for button in self.order:
                self.button_animation(button)
                pygame.time.wait(250) # Time between animation button
            self.waiting_player = True
        
        else:
            if self.clicked_button and self.clicked_button == self.order[self.current_step]:
                self.button_animation(self.clicked_button)
                self.current_step += 1

                if self.current_step == len(self.order):
                    self.score += 1
                    self.waiting_player = False
                    self.current_step = 0

            elif self.clicked_button and self.clicked_button != self.order[self.current_step]:
                self.loss_sound.play()
                pygame.time.wait(200)
                self.flash[0].animation()
                self.save_score()
                self.playing = False

    def draw(self):
        self.screen.fill((40, 40, 40))
        TextOnScreen(170, 480, f"Score: {str(self.score)}",16,WHITE).draw(self.screen)
        TextOnScreen(370, 480, f"High score: {str(self.max_score)}",16,WHITE).draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()
    
    def button_animation(self, colour): 
        for i in range(len(self.colours)):
                if self.dark_colours[i] == colour:
                    colour = self.colours[i]
                    button = self.buttons[i]
                    self.sound[i].play()
        button_flash = Flash(button.x,button.y,SIZE_OF_BUTTON,SIZE_OF_BUTTON,colour,1,self.screen)
        button_flash.animation()

    def events(self): 
        global status
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button.colour
                if self.start_button.clicked(mouse_x, mouse_y):
                    self.new()
                    self.run()
                    status = "Play"
        

game = Game()

while True:
    if status == "New_open":
        game.start()
    if status == "Play":
        game.new()
        game.run()