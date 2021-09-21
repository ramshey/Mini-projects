import pygame
from pygame.locals import *
import sys
import time
import random

class Game:
    def __init__(self):
        self.w=1000
        self.h=667
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Your type time is 0 with Accuracy of 0% at 0 Words per minute.'
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 255, 255)
        self.TEXT_C = (219,219,219)
        self.RESULT_C = (255,255,146)


        pygame.init()
        self.open_img = pygame.image.load('open_page.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))


        self.bg = pygame.image.load('mybackground.jpg')
        self.bg = pygame.transform.scale(self.bg, (1000,667))

        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Speed test')

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w / 2,y+115))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence
# Accuracy is (no of correct characters)x100/ (total characters in the sentence)

    def show_results(self, screen):
        if(not self.end):
            #Time
            self.total_time = time.time() - self.time_start

            #Accuracy
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                 pass
            self.accuracy = count/len(self.word)*100

            #Words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = ('Your time is '+str(round(self.total_time)) +" s with an Accuracy of "+ str(round(self.accuracy)) + "%" + ' at ' + str(round(self.wpm)) + ' words per minute.')

            # draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150,150))
            #screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w/2-75,self.h-140))
            self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))

            print(self.results)
            pygame.display.update()
    def run(self):
        self.reset_game()


        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (170,360,650,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (170,360,650,50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 265, 40,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=5 and x<=1000 and y>=0 and y<=667):
                        self.active = True

                        self.input_text = ''
                        self.time_start = time.time()
                    # position of reset box
                    if(x>=310 and x<=510 and y>=390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()


                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()


        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(1)

        self.reset=False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg,80, 80,self.HEAD_C)
        # input box
        pygame.draw.rect(self.screen,(255,192,25), (170,360,600,50), 2)

        # draw the sentence
        self.draw_text(self.screen, self.word,200, 30,self.TEXT_C)

        pygame.display.update()
Game().run()
