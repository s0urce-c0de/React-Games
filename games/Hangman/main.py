#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import importlib
import multiprocess as multiprocessing
try:multiprocessing.set_start_method('fork')
except: pass
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
manager=multiprocessing.Manager()

pygame.init()
clock=pygame.time.Clock()
pardir=Path(__file__).resolve().parent
projdir=Path(__file__).resolve().parent.parent.parent
game_window = pygame.display.set_mode((900, 500),
                                      pygame.RESIZABLE)
pygame.display.set_caption("Hangman")
pygame.display.set_icon(pygame.image.load(projdir / 'public' / 'favicon.svg'))
game_window.fill("#FFFFFF")

words_file=open(pardir.parent / 'words.txt')
words=words_file.read().split('\n')
words_file.close()
del words_file

level=1
incorrect=0
NORMAL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 32)
MINI_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 13)
LEVEL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 25)
XL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 3487)
TITLE=NORMAL_FONT.render("Hangman", True, '#000000')
BY=MINI_FONT.render("By Kanav G.", True, '#000000')
LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')


if __name__=="__main__":
  images=manager.list([PicklableSurface(pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png').convert_alpha(), (game_window.get_width()//(900/209), game_window.get_height()/(500/216)))) for i in range(0, 7)])
  image_lock=manager.Lock()
else:
  images=[PicklableSurface(pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png').convert_alpha(), (game_window.get_width()//(900/209), game_window.get_height()/(500/216)))) for i in range(0, 7)]
  image_lock=None
def run_on_subprocess(func) -> types.FunctionType:
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        sub_p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)

        return sub_p
    return _wrapper
if __name__=="__main__":
  buttons=manager.dict()
  buttons_lock=manager.Lock()
else:
  buttons={}
  buttons_lock=None
def update_char(char: str):
  if char in ''.join(word).upper():
    for i in len(word):
      if ''.join(word).upper()[i]==char:
        guessed_word[i] = char
  print('Word:',guessed_word)
  buttons[char].should_draw=False
  return guessed_word

for char in range(65, 91):
   win_width=game_window.get_width()//15*15
   unit=win_width/15
   radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
   x=unit+win_width-(win_width-((char-65)%13)*unit)
   y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*radius*((char-65)//13) + 90
   buttons[chr(char)]=Button(x, y, radius, 3, '#000000', XL_FONT.render(chr(char), True, '#000000').convert_alpha(), update_char, chr(char))
def generate_word(printw: bool = True) -> str:
  word=random.choice(words)
  if printw:
    print(word)
  return word
def update_images(lock) -> None:
  while run.value:
    for i in range(0, 7):
      with lock:
        images[i]=PicklableSurface(pygame.transform.scale(pygame.image.load(pardir/'images'/f'Hangman{i}.png'), (game_window.get_width()//(900/209), game_window.get_height()/(500/216))))
def update_buttons(lock):
  while run.value:
      with lock:
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
    word = manager.list(generate_word())
    guessed_word=manager.list('_'*len(word))
    run = manager.Value('i', True)
    p1=multiprocessing.Process(target=update_images, args=(image_lock,))
    p1.start()
    while run.value:
      # reset level text
      LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # level
      game_window.blit(LEVEL_TEXT, (game_window.get_width()-LEVEL_TEXT.get_width(), 2))
      # hanged man
      with image_lock:
        game_window.blit(images[incorrect].surface, ((game_window.get_width()-images[incorrect].get_width())/2-game_window.get_width()/6//1, TITLE.get_height()+50))
      for key in buttons:
        if buttons[key].should_draw: buttons[key].draw(game_window)
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == 256:
          run.value=False
    pygame.quit()
    exit()
  finally:
    run.value=False
    pygame.quit
    if dev:
      raise
    exit()
