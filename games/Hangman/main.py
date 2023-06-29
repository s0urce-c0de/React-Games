#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import importlib
import functools
import random
import types
import sys
import os
from pathlib import Path
#from functions4pickle import update_char
#from ..utils import Button, PicklableSurface
spec = importlib.util.spec_from_file_location("utils", Path(__file__).resolve().parent.parent / 'utils.py')
utils = importlib.util.module_from_spec(spec)
sys.modules["utils"] = utils
spec.loader.exec_module(utils)
Button,PicklableSurface=utils.Button,utils.PicklableSurface
dev=True

pygame.init()
clock=pygame.time.Clock()
pardir=Path(__file__).resolve().parent
projdir=Path(__file__).resolve().parent.parent.parent
game_window = pygame.display.set_mode((900, 500),
                                      pygame.RESIZABLE)
# pygame.display.set_caption("Hangman")
# pygame.display.set_icon(pygame.image.load(projdir / 'public' / 'favicon.svg'))
game_window.fill("#FFFFFF")
pygame.display.update()

# words_file=open(pardir.parent / 'words.txt')
# words=words_file.read().split('\n')
# words_file.close()
# del words_file

words=['FOO', 'BAR']

level=1
incorrect=0
NORMAL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 32)
MINI_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 13)
LEVEL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 25)
XL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 100)
BY=MINI_FONT.render("By Kanav G.", True, '#000000')
LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
TITLE=NORMAL_FONT.render("Hangman", True, '#000000')


images=[pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png').convert_alpha(), (game_window.get_width()//(900/209), game_window.get_height()/(500/216))) for i in range(0, 7)]
buttons={}
def update_char(char: str):
  char=char.upper()
  buttons[char].should_draw=False
  print(buttons)
  print(buttons[char])
  print(char)
  if char in ''.join(word).upper():
    for i in range(len(word)):
      if word[i]==char:
        guessed_word[i]=char
for char in range(65, 91):
   win_width=game_window.get_width()//15*15
   unit=win_width/15
   radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
   x=unit+win_width-(win_width-((char-65)%13)*unit)
   y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*radius*((char-65)//13) + 90
   buttons[chr(char)]=Button(x, y, radius, 3, '#000000', XL_FONT.render(chr(char), True, '#000000').convert_alpha(), update_char, chr(char))
def update_images() -> None:
  images=[pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png'), (game_window.get_width()//(900/209), game_window.get_height()/(500/216))) for i in range(0,7)]
def update_buttons() -> None:
  for i in range(65, 91):
    button=buttons[chr(i)]
    win_width=game_window.get_width()//15*15
    unit=win_width/15
    button.radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
    button.x=unit+win_width-(win_width-((i-65)%13)*unit)
    button.y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*button.radius*((i-65)//13)+90
    button.image = pygame.transform.scale(button.image_raw, (2*button.radius, 2*button.radius))
    button.onclickargs=(button.onclickargs[0])
    buttons[chr(i)]=button
del win_width, unit, radius, x, y
if __name__ == "__main__":
  try:
    word = list(random.choice(words))
    print(word)
    guessed_word=['_']*len(word)
    run = True
    while run:
      # reset level text
      LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # level
      game_window.blit(LEVEL_TEXT, (game_window.get_width()-LEVEL_TEXT.get_width(), 2))
      # hanged man
      game_window.blit(images[incorrect], ((game_window.get_width()-images[incorrect].get_width())/2-game_window.get_width()/6//1, TITLE.get_height()+50))
      for key in buttons: buttons[key].draw(game_window)
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == 256:
          run=False



    pygame.quit()
    exit()
  finally:
    run=False
    pygame.quit
    if dev:
      raise
    exit()
