#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import importlib
import random
from pathlib import Path
#from functions4pickle import update_char
#from ..utils import Button, PicklableSurface
spec = importlib.util.spec_from_file_location("utils", Path(__file__).resolve().parent.parent / 'utils.py') # type: ignore
utils = importlib.util.module_from_spec(spec) # type: ignore
spec.loader.exec_module(utils)
Button,PicklableSurface,MultiLineText_Blit=utils.CircleButton,utils.PicklableSurface,utils.MultiLineText_Blit
dev=True

pygame.init()
clock=pygame.time.Clock()
pardir=Path(__file__).resolve().parent
projdir=Path(__file__).resolve().parent.parent.parent
game_window = pygame.display.set_mode((900, 500),
                                      pygame.RESIZABLE)
pygame.display.set_caption("Hangman")
pygame.display.set_icon(pygame.image.load(pardir / 'images' / 'favicon.png'))
game_window.fill("#FFFFFF")
pygame.display.update()

words_file=open(pardir.parent / 'words.txt')
words=words_file.read().split('\n')
words_file.close()
del words_file

level=1
incorrect=0
NORMAL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 32)
MINI_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 13)
LEVEL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 25)
XL_FONT = pygame.font.Font(projdir / 'src' / 'fonts' / 'Press Start 2P' /'PS2P.ttf', 100)
BY=MINI_FONT.render("By Kanav G.", True, '#000000')
LEVEL_TEXT=LEVEL_FONT.render(f"Level: {level}", True, '#000000')
TITLE=NORMAL_FONT.render("Hangman", True, '#000000')

raw_images=[pygame.image.load(pardir/'images'/f'Hangman{i}.png') for i in range(0,7)]
images=[pygame.transform.scale(raw_images[i], (game_window.get_width()//(900/209), game_window.get_height()/(500/216))) for i in range(0, 7)]
buttons={}
def generate_word(level: int) -> str:
  generator_level=level
  if level>15:
    generator_level=15
  narrow_word_list=[]
  for word in words:
    if generator_level*2<len(word)<generator_level*2+4:
      narrow_word_list.append(word)
  return random.choice(narrow_word_list)
def new_level() -> None:
  global word, guessed_word, incorrect, level
  # update level
  level+=1
  # reset ammount of incorrect guesses
  incorrect=0
  # generate new word
  word=generate_word(level)
  print(word)
  # reset the guessed word
  guessed_word=['_']*len(word)
  # regenerate all buttons
  for button in buttons: buttons[button].should_draw=True
def update_char(char: str) -> None:
  char=char.upper()
  buttons[char].should_draw=False
  if char in ''.join(word).upper():
    for i in range(len(word)):
      if ''.join(word).upper()[i]==char:
        guessed_word[i]=char
  else:
    global incorrect
    incorrect+=1
for char in range(65, 91):
   win_width=game_window.get_width()//15*15
   unit=win_width/15
   radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
   x=unit+win_width-(win_width-((char-65)%13)*unit)
   y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*radius*((char-65)//13) + 90
   buttons[chr(char)]=Button(x, y, radius, 3, '#000000', XL_FONT.render(chr(char), True, '#000000').convert_alpha(), update_char, chr(char))
del win_width, unit, radius, x, y
def update_images() -> None:
  global images
  images=[pygame.transform.scale(raw_images[i], (game_window.get_width()//(900/209), game_window.get_height()/(500/216))) for i in range(0, 7)]
def update_buttons() -> None:
  for i in range(65, 91):
    global buttons
    button=buttons[chr(i)]
    win_width=game_window.get_width()//15*15
    unit=win_width/15
    button.radius=((game_window.get_height()-BY.get_height()-TITLE.get_height()-images[incorrect].get_height()-30))//8 - 1
    button.x=unit+win_width-(win_width-((i-65)%13)*unit)
    button.y=BY.get_height()+TITLE.get_height()+images[incorrect].get_height()+2*button.radius*((i-65)//13)+90
    button.image = pygame.transform.scale(button.image_raw, (2*button.radius, 2*button.radius))
    button.onclickargs=(button.onclickargs[0])
    buttons[chr(i)]=button
if __name__ == "__main__":
  try:
    word = generate_word(level)
    print(''.join(word))
    guessed_word=['_']*len(word)
    run = True
    while run:
      game_window.fill('#FFFFFF')
      if incorrect>=6:
        game_window.fill("#FF0000")
        MultiLineText_Blit(game_window, f"You Lose :( \nThe word was '{''.join(word)}'", ( game_window.get_width()//10*3, game_window.get_height()//7*5), NORMAL_FONT)
        for button in buttons: buttons[button].should_draw=False
      update_buttons()
      update_images()
      if '_' not in guessed_word:
        new_level()
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
      # guessed word
      game_window.blit(NORMAL_FONT.render(''.join(guessed_word), True, '#000000'), ((game_window.get_width())//2-game_window.get_width()//6+images[incorrect].get_width()//3+4, TITLE.get_height()+90))
      for key in buttons: buttons[key].draw(game_window)
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == 256:
          run=False



    pygame.quit()
    exit()
  finally:
    run=False
    pygame.quit()
    if dev:
      raise
    exit()
