#!/usr/bin/env python3
# -*- encoding: utf-8-*-

import pygame
import sys
from utils import CircleButton, MultiLineText_Blit
from pathlib import Path

pygame.init()
clock=pygame.time.Clock()
PyInstaller=hasattr(sys, '_MEIPASS')
pardir=Path(__file__).resolve().parent
dev=not PyInstaller
game_window = pygame.display.set_mode((853, 480),
                    ) #pygame.Resizable
WIDTH=game_window.get_width()
HEIGHT=game_window.get_height()
FPS=60
pygame.display.set_caption("Spaceship Game")
pygame.display.set_icon(pygame.image.load(pardir / 'images' / 'favicon.png'))
pygame.display.update()
level=1
NORMAL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 32)
MINI_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 13)
LEVEL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 25)
XL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 100)
BY=MINI_FONT.render("By Kanav G.", True, '#FFFFFF')
TITLE=NORMAL_FONT.render("Spaceship Game", True, '#FFFFFF')
raw_images = {
  'spaceships': {
    'red' : pygame.image.load(pardir / 'images' / 'spaceship_red.png'),
    'yellow' : pygame.image.load(pardir / 'images' / 'spaceship_yellow.png')
  },
  'background' : pygame.image.load(pardir / 'images' / 'spacebackground.jpeg')
}
images = raw_images
images['spaceships']['red'] = pygame.transform.rotate(images['spaceships']['red'], 270)
images['spaceships']['yellow']= pygame.transform.rotate(images['spaceships']['yellow'], 90)
game_window.blit(images['background'], (0, 0))
def new_level() -> None: ...

if __name__ == "__main__":
  try:
    # do some other pregame stuff
    run = True
    while run:
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # do some things
      pygame.display.update()
      # tick the clock
      clock.tick(FPS)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run=False
    pygame.quit()
    exit()
  finally:
    run=False
    pygame.quit()
    if dev:
      raise
    exit()