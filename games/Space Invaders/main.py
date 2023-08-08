#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import sys
import threading
import time
import random
from typing import Union, Dict, List
from utils import MovingCharacter, center_screen
from pathlib import Path

pygame.init()
clock = pygame.time.Clock()
PyInstaller=hasattr(sys, '_MEIPASS')
pardir=Path(__file__).resolve().parent
dev=not PyInstaller
game_window = pygame.display.set_mode((853, 480),
                                      )# pygame.RESIZABLE)
WIDTH=game_window.get_width()
HEIGHT=game_window.get_height()
FPS=60
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load(pardir / 'images' / 'favicon.png'))

NORMAL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 32)
MINI_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 13)
LEVEL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 25)
BY=MINI_FONT.render("By Kanav G.", True, '#FFFFFF')
TITLE=NORMAL_FONT.render("Space Invaders", True, '#FFFFFF')
SCORE=MINI_FONT.render(f"Score: {(score := 0)}", True, '#FFFFFF')

raw_images: Dict[str, Union[Dict[str, pygame.surface.SurfaceType], pygame.surface.SurfaceType]] = {
  'aliens': {
    'purple': pygame.image.load(pardir / 'images' / 'aliens' / 'purple.png')
  },
  'background': pygame.image.load(pardir / 'images' / 'spacebackground.jpeg'),
  'spaceship': pygame.image.load(pardir / 'images' / 'spaceship.png'),
  'bullet': pygame.image.load(pardir / 'images' / 'bullet.png'),
  'empty': pygame.sysfont.SysFont(None,0).render('',False,(0,0,0,0)),
  'GAME_OVER': pygame.sysfont.SysFont(None,0).render('',False,(0,0,0,0))
} 
# images
images = raw_images
images['spaceship'] = pygame.transform.smoothscale_by(pygame.transform.rotate(images['spaceship'], 180), 0.17)
images['bullet'] = pygame.transform.smoothscale_by(images['bullet'], 0.17)
images['aliens']['purple']=pygame.transform.smoothscale_by(images['aliens']['purple'], 0.13)
bullets: List[Dict[str, Union[str, pygame.rect.RectType]]]=[]
aliens: List[List[List[Union[pygame.rect.RectType, pygame.surface.SurfaceType]]]] = []
game_window.blit(images['background'], (0,0))
pygame.display.update()

def shoot():
  rect=images['bullet'].get_rect().move(SPACESHIP.x+(SPACESHIP.image.get_width()-images['bullet'].get_width())/2, SPACESHIP.y)
  bullets.append({'rect': rect, 'shooter': 'spaceship'})
def shoot_thread_function():
  wait=5
  while run and not game_over_status:
    new_row()
    for i in range(0, 1000*wait):
      if run and not game_over_status:
        time.sleep(1/1000)
      else:
        exit()
def new_row(alien: pygame.surface.Surface = random.choice(list(images['aliens'].keys()))):
  a2l=[]
  for i in range(0, 8):
    a2l.append([images['aliens'][alien], images['aliens'][alien].get_rect().move((WIDTH*(1/10*(2+i)))-images['aliens'][alien].get_width()/2, 100)])
  row=0
  for alien_row in aliens:
    num=0
    for alien in alien_row:
      aliens[row][num][1].y+=aliens[row][num][0].get_height() - 2
      num+=1
    row+=1
  aliens.append(a2l)
def game_over():
  global game_over_status
  game_over_status=True
  SPACESHIP.extra_controls={}
  SPACESHIP.disable_down=True
  SPACESHIP.disable_left=True
  SPACESHIP.disable_right=True
  SPACESHIP.disable_up=True
  images['GAME_OVER']=NORMAL_FONT.render('GAME OVER!', True, '#FFFFFF')
SPACESHIP=MovingCharacter(
  images['spaceship'],
  (WIDTH-images['spaceship'].get_height())/2,
  HEIGHT/10*7,
  'WASD',
  None,
  None,
  None,
  None,
  False,
  False,
  False,
  False,
  {
    pygame.K_SPACE: {
      'key_hold_allowed': False,
      'function': shoot
    }
  }
)
  
if __name__ == "__main__":
  try:
    # do some other pregame stuff
    game_over_status=False
    run = True
    shoot_thread=threading.Thread(target=shoot_thread_function, daemon=False)
    shoot_thread.start()
    while run:
      game_window.blit(images['background'], (0,0))
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # score
      game_window.blit(SCORE, (5,5))
      # draw the spaceship
      SPACESHIP.draw(game_window)
      bullet_index = 0
      for bullet in bullets:
        bullet_deleted=False
        if bullet['shooter']=='spaceship':
          row=0
          for alien_row in aliens:
            num=0
            for alien in alien_row:
              alien_deleted=False
              if bullet['rect'].colliderect(alien[1]):
                alien_deleted=True
                del alien_row[num]
                bullet_deleted=True
                del bullets[bullet_index]
                score += 1
                SCORE = MINI_FONT.render(f"Score: {score}", True, '#FFFFFF')
              num+=1 if not alien_deleted else 0
            row+=1
        if bullet['rect'].y<=0 or bullet['rect'].y>=HEIGHT:
          del bullets[bullet_index]
          bullet_deleted=True
        if bullet['shooter'] == 'spaceship' and not bullet_deleted:
          bullets[bullet_index]['rect'].y-=10
        elif bullet['shooter'] == 'alien' and not bullet_deleted:
          bullets[bullet_index]['rect'].y=10
        game_window.blit(images['bullet'], bullet['rect'])
        if not bullet_deleted:
          bullet_index+=1
      for alien_row in aliens:
        for alien in alien_row:
          game_window.blit(alien[0], alien[1])
          if alien[1].colliderect(SPACESHIP.image.get_rect().move(SPACESHIP.x, SPACESHIP.y)): 
            game_over()
      game_window.blit(images['GAME_OVER'], center_screen(game_window, images['GAME_OVER']))
      pygame.display.update()
      # tick the clock
      clock.tick(FPS)
      for event in pygame.event.get(pygame.QUIT): run=False
    pygame.quit()
    exit()
  finally:
    run=False
    pygame.quit()
    if dev:
      raise
    exit()