#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import types
import multiprocessing
from pathlib import Path

pygame.init()
clock=pygame.time.Clock()
pardir=Path(__file__).resolve().parent
manager = multiprocessing.Manager()
shared_dict = manager.dict()
shared_dict["game_window"] = pygame.display.set_mode((900, 500),
                                      pygame.RESIZABLE)
shared_dict["WINDOW_WIDTH"]=shared_dict["game_window"].get_width()
shared_dict["WINDOW_HEIGHT"]=shared_dict["game_window"].get_height()

images=[]
for i in range(0, 7):
   images.append(pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png'), (shared_dict["WINDOW_WIDTH"]//(900/209), shared_dict["WINDOW_HEIGHT"]/(500/216))))
shared_dict["images"] = images

words_file=open(pardir.parent / 'words.txt')
words=words_file.read().split('\n')
words_file.close()
del words_file

level=1
incorrect=0
NORMAL_FONT = pygame.font.SysFont('comicsans', 32)
MINI_FONT = pygame.font.SysFont('comicsans', 13)
LEVEL_FONT = pygame.font.SysFont('comicsans', 25)
XL_FONT = pygame.font.SysFont('comicsans', 3487)
TITLE=NORMAL_FONT.render("Hangman", True, '#000000')
BY=MINI_FONT.render("By Kanav G.", True, '#000000')
LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
shared_dict["level"] = level
shared_dict["incorrect"] = incorrect
shared_dict["NORMAL_FONT"] = NORMAL_FONT
shared_dict["MINI_FONT"] = MINI_FONT
shared_dict["LEVEL_FONT"] = LEVEL_FONT
shared_dict["XL_FONT"] = XL_FONT
shared_dict["TITLE"] = TITLE
shared_dict["BY"] = BY
shared_dict["LEVEL_TEXT"] = LEVEL_TEXT

class Image(pygame.sprite.Sprite):
  def __init__(self, x, y, image):
    super().__init__()
    self.x = x
    self.y = y
    self.image = image
    self.rect = self.image.get_rect()

class Button:
    def __init__(self, x: int, y: int, radius: int, thickness: int =1, color = "#000000", \
                 image: pygame.surface.Surface = pygame.font.SysFont(None, 0).render('', True, "#000000"), \
                 onClick: types.FunctionType = (lambda: 1), *onClickArgs, **onClickKwargs):
        self.x = x
        self.y = y
        self.radius = radius
        self.thickness = thickness
        self.color = color
        self.image_raw = image
        self.onclick=onClick
        self.onclickargs=onClickArgs
        self.onclickkwargs=onClickKwargs
        self.image_rect = self.image_raw.get_rect()
        self.image_rect.center = (self.x, self.y)
        self.image = pygame.transform.scale(self.image_raw, (2*self.radius, 2*self.radius))
        self.clicked=False
        self.image.blit(self.image, (0,0), (0,0,self.radius*2,self.radius*2))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        hover = self.is_hover(mouse_pos)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.thickness)
        screen.blit(self.image, (self.x-self.radius, self.y-self.radius))
        
        if hover and mouse_clicked and not self.clicked:
            self.onclick(*self.onclickargs, **self.onclickkwargs)
            self.clicked=True
        elif not mouse_clicked:
           self.clicked=False
    
    def is_hover(self, mouse_pos):
        distance = ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5
        return distance <= self.radius

button_count=0
buttons=[]
for char in range(ord('A'), ord('Z')+1):
   button_count+=1
   win_width=shared_dict["WINDOW_WIDTH"]//15*15
   unit=win_width/15
   radius=((shared_dict["WINDOW_HEIGHT"]-BY.get_height()-TITLE.get_height()-shared_dict["images"][incorrect].get_height()-30))//8 - 1
   y_buffer = radius*((button_count-1)//13)+60
   x=unit+win_width-(win_width-((button_count-1)%13)*unit)
   y=BY.get_height()+TITLE.get_height()+shared_dict["images"][incorrect].get_height()+30*((button_count-1)//13)+y_buffer
   buttons.append(Button(x, y, radius, 3, '#000000', XL_FONT.render(chr(char), True, '#000000')))
del button_count, win_width, unit, radius, y_buffer, x, y

if __name__ == "__main__":
  run = True
  while run:

    shared_dict["images"]=[]
    for i in range(0, 7):
      shared_dict["images"].append(pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png'), (shared_dict["WINDOW_WIDTH"]//(900/209), shared_dict["WINDOW_HEIGHT"]/(500/216))))
    # reset size 4 resizable  window
    shared_dict["WINDOW_WIDTH"]=shared_dict["game_window"].get_width()
    shared_dict["WINDOW_HEIGHT"]=shared_dict["game_window"].get_height()
    # reset level text
    shared_dict["LEVEL_TEXT"]=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
    # set background
    shared_dict["game_window"].fill("#FFFFFF")
    # title
    shared_dict["game_window"].blit(TITLE, ((shared_dict["WINDOW_WIDTH"]-TITLE.get_width())/2, 3))
    # by
    shared_dict["game_window"].blit(BY, ((shared_dict["WINDOW_WIDTH"]-TITLE.get_width())/2+5, 7+TITLE.get_height()))
    # level
    shared_dict["game_window"].blit(shared_dict["LEVEL_TEXT"], (shared_dict["WINDOW_WIDTH"]-shared_dict["LEVEL_TEXT"].get_width(), 2))
    # hanged man
    shared_dict["game_window"].blit(shared_dict["images"][incorrect], ((shared_dict["WINDOW_WIDTH"]-shared_dict["images"][incorrect].get_width())/2-shared_dict["WINDOW_WIDTH"]/6//1, TITLE.get_height()+50))
    for i in range(0, 26):
      button=buttons[i]
      win_width=shared_dict["WINDOW_WIDTH"]//15*15
      unit=win_width/15
      button.radius=((shared_dict["WINDOW_HEIGHT"]-BY.get_height()-TITLE.get_height()-shared_dict["images"][incorrect].get_height()-30))//8 - 1
      y_buffer = button.radius*(i//13)+60
      button.x=unit+win_width-(win_width-(i%13)*unit)
      button.y=BY.get