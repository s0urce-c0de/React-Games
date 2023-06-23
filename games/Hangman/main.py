#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import types
import multiprocessing
multiprocessing.set_start_method('fork')
import functools 
import random
from pathlib import Path

if __name__=="__main__":
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
                 onClick: types.FunctionType = (lambda: None), *onClickArgs, **onClickKwargs):
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
        self.should_draw=True
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
class PicklableSurface:
    def __init__(self, surface):
        self.surface = surface
        self.name = "PicklableSurface"

    def __getstate__(self):
        state = self.__dict__.copy()
        surface = state.pop("surface")
        state["surface_string"] = (pygame.image.tostring(surface, "RGB"), surface.get_size())
        return state

    def __setstate__(self, state):
        surface_string, size = state.pop("surface_string")
        state["surface"] = pygame.image.fromstring(surface_string, size, "RGB")
        self.__dict__.update(state)
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
  raise
  exit()
