#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
import sys
from utils import CircleButton as Button, MultiLineText_Blit
from pathlib import Path

pygame.init()
clock = pygame.time.Clock()
PyInstaller=hasattr(sys, '_MEIPASS')
pardir=Path(__file__).resolve().parent
dev=not PyInstaller
game_window = pygame.display.set_mode((900, 500),
                                      pygame.RESIZABLE)
WIDTH=game_window.get_width()
HEIGHT=game_window.get_height()
FPS=60
pygame.display.set_caption("My Game")
pygame.display.set_icon(pygame.image.load(pardir / 'images' / 'favicon.png'))
game_window.fill("#FFFFFF")
pygame.display.update()

level=1
NORMAL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 32)
MINI_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 13)
LEVEL_FONT = pygame.font.Font(pardir / 'fonts' / 'PS2P.ttf', 25)
BY=MINI_FONT.render("By Kanav G.", True, '#000000')
TITLE=NORMAL_FONT.render("My Game", True, '#000000')

raw_images = {} # images
images = raw_images

def new_level() -> None: ...

if __name__ == "__main__":
  try:
    # do some other pregame stuff
    run = True
    while run:
      # refill screen
      game_window.fill('#FFFFFF')
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      # do some things
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