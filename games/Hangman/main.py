#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import multiprocessing
try:multiprocessing.set_start_method('fork')
except:raise RuntimeWarning("Built for start method fork")
import functools 
import random
import os
from pathlib import Path
from ..utils import Image, Button, PickableSurface

manager=multiprocessing.Manager()

pygame.init()
clock=pygame.time.Clock()
pardir=Path(__file__).resolve().parent
game_window = pygame.display.set_mode((900, 500),
                                      pygame.RESIZABLE)



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


images=manager.list()
for i in range(0, 7):
   images.append(PicklableSurface(pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png'), (game_window.get_width()//(900/209), game_window.get_height()/(500/216)))))
def run_on_subprocess(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        sub_p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)

        return sub_p
    return _wrapper
def update_char(char: str):
  
  if char in ''.join(word).upper():
    for i in len(word):
      if ''.join(word).upper()[i]==char:
        word[i] = char
  print('Word:',guessed_word)
buttons={}
for char in range(65, 91):
   win_width=game_window.get_width()//15*15
   unit=win_width/15
   radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
   x=unit+win_width-(win_width-((char-65)%13)*unit)
   y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*radius*((char-65)//13) + 90
   buttons[chr(char)]=Button(x, y, radius, 3, '#000000', XL_FONT.render(chr(char), True, '#000000'), update_char, chr(char))
def update_images():
  while run.value:
    for i in range(0, 7):
      images[i]=pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png'), (game_window.get_width()//(900/209), game_window.get_height()/(500/216)))
del win_width, unit, radius, x, y
__name__="notmain"
try:
  if __name__ == "__main__":
    word = manager.list(random.choice(words))
    guessed_word=manager.list('_'*len(word))
    run = manager.Value('i', True)
    p1=multiprocessing.Process(target=update_images)
    print(word)
    p1.start()
    while run.value:
      # reset level text
      LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
      # set background
      game_window.fill("#FFFFFF")
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # level
      game_window.blit(LEVEL_TEXT, (game_window.get_width()-LEVEL_TEXT.get_width(), 2))
      # hanged man
      game_window.blit(images[incorrect], ((game_window.get_width()-images[incorrect].get_width())/2-game_window.get_width()/6//1, TITLE.get_height()+50))
      # for i in range(65, 91):
      #   button=buttons[chr(i)]
      #   win_width=game_window.get_width()//15*15
      #   unit=win_width/15
      #   button.radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
      #   button.x=unit+win_width-(win_width-((i-65)%13)*unit)
      #   button.y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*button.radius*((i-65)//13)+90
      #   button.image = pygame.transform.scale(button.image_raw, (2*button.radius, 2*button.radius))
      #   button.onclickargs=(button.onclickargs[0])
      #   buttons[chr(i)]=button
      for key in buttons:
        if buttons[key].should_draw: buttons[key].draw(game_window)
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == 256:
          run.value=False
    pygame.quit()
    exit()
finally:
  pygame.quit()
  exit()
