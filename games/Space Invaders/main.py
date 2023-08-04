#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import sys
from typing import Union, Dict, List
from utils import MovingCharacter
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

raw_images: Dict[str, Union[Dict[str, pygame.surface.SurfaceType], pygame.surface.SurfaceType]] = {
  'aliens': {
    'purple': pygame.image.load(pardir / 'images' / 'aliens' / 'purple.png')
  },
  'background': pygame.image.load(pardir / 'images' / 'spacebackground.jpeg'),
  'spaceship': pygame.image.load(pardir / 'images' / 'spaceship.png'),
  'bullet': pygame.image.load(pardir / 'images' / 'bullet.png')
} 
# images
images = raw_images
images['spaceship'] = pygame.transform.smoothscale_by(pygame.transform.rotate(images['spaceship'], 180), 0.17)
images['bullet'] = pygame.transform.smoothscale_by(images['bullet'], 0.17)
bullets: List[Dict[str, Union[str, pygame.rect.RectType]]]=[]
game_window.blit(images['background'], (0,0))
pygame.display.update()

def shoot():
  rect=images['bullet'].get_rect().move(SPACESHIP.x+(SPACESHIP.image.get_width()-images['bullet'].get_width())/2, SPACESHIP.y)
  bullets.append({'rect': rect, 'shooter': 'spaceship'})
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
    pygame.K_e: {
      'key_hold_allowed': False,
      'function': shoot
    }
  }
)

if __name__ == "__main__":
  try:
    # do some other pregame stuff
    run = True
    while run:
      game_window.blit(images['background'], (0,0))
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # draw the spaceship
      SPACESHIP.draw(game_window)
      bullet_index = 0
      for bullet in bullets:
        bullet_deleted=False
        if bullet['rect'].y<=0 or bullet['rect'].y>=HEIGHT:
          del bullets[bullet_index]
          bullet_deleted=True
        if bullet['shooter'] == 'spaceship' and not bullet_deleted:
          bullets[bullet_index]['rect'].y-=10
        game_window.blit(images['bullet'], bullet['rect'])
        if not bullet_deleted:
          bullet_index+=1
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