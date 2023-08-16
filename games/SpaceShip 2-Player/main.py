#!/usr/bin/env python3
# -*- encoding: utf-8-*-

"""
A spaceship game made with PyGame.

Controls:
  Red Spaceship: 
    Movement: Arrow Keys
    Shoot: E
  Yellow Spaceship: 
    Movemet: WASD
    Shoot: Forward Slash
"""

import pygame
import sys
from utils import MovingCharacter, RectangularButton
from pathlib import Path
import asyncio

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
BY=MINI_FONT.render("By Kanav G.", True, '#FFFFFF')
TITLE=NORMAL_FONT.render("Spaceship Game", True, '#FFFFFF')
print("Controls:\n\tRed Spaceship:\n\t\tMovement: Arrow Keys\n\t\tShoot: E\n\tYellow Spaceship:\n\t\tMovemet: WASD\n\t\tShoot: Forward Slash")
raw_images = {
  'spaceships': {
    'red': pygame.image.load(pardir / 'images' / 'spaceship_red.png'),
    'yellow': pygame.image.load(pardir / 'images' / 'spaceship_yellow.png')
  },
  'background': pygame.image.load(pardir / 'images' / 'spacebackground.jpeg'),
  'bullet': pygame.image.load(pardir / 'images' / 'bullet.png')
}
DEFAULT_HEALTH=50
images = raw_images
disable_red=False
disable_yellow=False
bullets=[]
def red_shoot():
  if not disable_red:
    rect=images['bullet'].get_rect()
    rect.x=RED_SPACESHIP.x+20
    rect.y=RED_SPACESHIP.y+(RED_SPACESHIP.image.get_height()-images['bullet'].get_height())//2
    bullets.append({'rect': rect, 'shooter': 'red'})
def yellow_shoot():
  if not disable_yellow:
    rect=images['bullet'].get_rect()
    rect.x=YELLOW_SPACESHIP.x+YELLOW_SPACESHIP.image.get_width()-images['bullet'].get_width()+20
    rect.y=YELLOW_SPACESHIP.y+(YELLOW_SPACESHIP.image.get_height()-images['bullet'].get_height())//2
    bullets.append({'rect': rect, 'shooter': 'yellow'})
def restart():
  global bullets, RED_SPACESHIP, YELLOW_SPACESHIP, RED_SPACESHIP_HEALTH, RED_SPACESHIP_HEALTH_TEXT, YELLOW_SPACESHIP_HEALTH, YELLOW_SPACESHIP_HEALTH_TEXT, WINNER_TEXT, disable_red, disable_yellow
  bullets=[]
  RED_SPACESHIP = MovingCharacter(
                    images['spaceships']['red'],
                    WIDTH/10*7,
                    (HEIGHT-images['spaceships']['red'].get_height())//2,
                    'arrow_keys',
                    None,
                    WIDTH//2,
                    None,
                    None,
                    False,
                    False,
                    False,
                    False,
                    {
                      pygame.K_SLASH:
                        {
                          'function': red_shoot,
                          'key_hold_allowed': False
                        }
                    }
                  )
  YELLOW_SPACESHIP = MovingCharacter(
                      images['spaceships']['yellow'],
                      WIDTH/10*3-images['spaceships']['yellow'].get_width(),
                      (HEIGHT-images['spaceships']['yellow'].get_height())//2,
                      'WASD',
                      None,
                      None,
                      None,
                      WIDTH//2,
                      False,
                      False,
                      False,
                      False,
                      {
                        pygame.K_e: {
                          'function': yellow_shoot,
                          'key_hold_allowed': False
                          }
                      }
                    )
  RED_SPACESHIP_HEALTH = DEFAULT_HEALTH
  YELLOW_SPACESHIP_HEALTH = DEFAULT_HEALTH
  RED_SPACESHIP_HEALTH_TEXT=MINI_FONT.render(f'HEALTH: {RED_SPACESHIP_HEALTH}', True, '#FFFFFF')
  YELLOW_SPACESHIP_HEALTH_TEXT=MINI_FONT.render(f'HEALTH: {YELLOW_SPACESHIP_HEALTH}', True, '#FFFFFF')
  disable_red=False
  disable_yellow=False
  WINNER_TEXT=pygame.sysfont.SysFont(None,0).render('',False,(0,0,0,0))
  RESTART.hide()
images['spaceships']['red'] = pygame.transform.smoothscale_by(pygame.transform.rotate(images['spaceships']['red'], 270), 0.17)
images['spaceships']['yellow'] = pygame.transform.smoothscale_by(pygame.transform.rotate(images['spaceships']['yellow'], 90), 0.17)
images['bullet'] = pygame.transform.smoothscale_by(pygame.transform.rotate(images['bullet'], 90), 0.17)
RED_SPACESHIP = MovingCharacter(
                  images['spaceships']['red'],
                  WIDTH/10*7,
                  (HEIGHT-images['spaceships']['red'].get_height())//2,
                  'arrow_keys',
                  None,
                  WIDTH//2,
                  None,
                  None,
                  False,
                  False,
                  False,
                  False,
                  {
                    pygame.K_SLASH:
                      {
                        'function': red_shoot,
                        'key_hold_allowed': False
                      }
                  }
                )
RED_SPACESHIP_HEALTH=DEFAULT_HEALTH
RED_SPACESHIP_HEALTH_TEXT=MINI_FONT.render(f'HEALTH: {RED_SPACESHIP_HEALTH}', True, '#FFFFFF')
YELLOW_SPACESHIP = MovingCharacter(
                    images['spaceships']['yellow'],
                    WIDTH/10*3-images['spaceships']['yellow'].get_width(),
                    (HEIGHT-images['spaceships']['yellow'].get_height())//2,
                    'WASD',
                    None,
                    None,
                    None,
                    WIDTH//2,
                    False,
                    False,
                    False,
                    False,
                    {
                      pygame.K_e: {
                        'function': yellow_shoot,
                        'key_hold_allowed': False
                        }
                    }
                  )
YELLOW_SPACESHIP_HEALTH=DEFAULT_HEALTH
YELLOW_SPACESHIP_HEALTH_TEXT=MINI_FONT.render(f'HEALTH: {YELLOW_SPACESHIP_HEALTH}', True, '#FFFFFF')
WINNER_TEXT=pygame.sysfont.SysFont(None,0).render('',False,(0,0,0,0))
RESTART_TEXT=NORMAL_FONT.render('Restart', True, '#FFFFFF')
RESTART=RectangularButton(
  (WIDTH-RESTART_TEXT.get_width())/2,
  HEIGHT/2+RESTART_TEXT.get_height()*2.6,
  RESTART_TEXT.get_height()+34,
  RESTART_TEXT.get_width()+50,
  3,
  "#000000",
  (10, 10, 10, 10),
  RESTART_TEXT,
  restart
)
RESTART.hide()
game_window.blit(images['background'], (0, 0))

async def main():
  global YELLOW_SPACESHIP_HEALTH, RED_SPACESHIP_HEALTH, YELLOW_SPACESHIP_HEALTH_TEXT, RED_SPACESHIP_HEALTH_TEXT, WINNER_TEXT
  try:
    # do some other pregame stuff
    run = True
    while run:
      # background
      game_window.blit(images['background'], (0, 0))
      # title
      game_window.blit(TITLE, ((game_window.get_width()-TITLE.get_width())/2, 3))
      # by
      game_window.blit(BY, ((game_window.get_width()-TITLE.get_width())/2+5, 7+TITLE.get_height()))
      #Health texts
      game_window.blit(RED_SPACESHIP_HEALTH_TEXT, (WIDTH-5-RED_SPACESHIP_HEALTH_TEXT.get_width(), 5))
      game_window.blit(YELLOW_SPACESHIP_HEALTH_TEXT, (5, 5))
      # spaceships
      RED_SPACESHIP.draw(game_window)
      YELLOW_SPACESHIP.draw(game_window)
      bullet_index=0
      for bullet in bullets:
        bullet_deleted=False
        if RED_SPACESHIP.image.get_rect().move(RED_SPACESHIP.x, RED_SPACESHIP.y).colliderect(bullet['rect']) and bullet['shooter'].lower() != 'red':
          del bullets[bullet_index]
          bullet_deleted=True
          RED_SPACESHIP_HEALTH-=1
          RED_SPACESHIP_HEALTH_TEXT=MINI_FONT.render(f'HEALTH: {RED_SPACESHIP_HEALTH}', True, '#FFFFFF')
        elif YELLOW_SPACESHIP.image.get_rect().move(YELLOW_SPACESHIP.x, YELLOW_SPACESHIP.y).colliderect(bullet['rect']) and bullet['shooter'].lower() != 'yellow':
          del bullets[bullet_index]
          bullet_deleted=True
          YELLOW_SPACESHIP_HEALTH-=1
          YELLOW_SPACESHIP_HEALTH_TEXT=MINI_FONT.render(f'HEALTH: {YELLOW_SPACESHIP_HEALTH}', True, '#FFFFFF')
        if bullet['rect'].x<0 or bullet['rect'].x>WIDTH and not bullet_deleted:
          del bullets[bullet_index]

        if bullet['shooter']=='red':
          bullet['rect'].x-=10
        elif bullet['shooter']=='yellow':
          bullet['rect'].x+=10
        game_window.blit(images['bullet'], bullet['rect'])
        bullet_index+=1
      if RED_SPACESHIP_HEALTH<=0:
        disable_red=True
        RED_SPACESHIP.disable_down=True
        RED_SPACESHIP.disable_left=True
        RED_SPACESHIP.disable_right=True
        RED_SPACESHIP.disable_up=True
        if not(RED_SPACESHIP.image.get_height()<=0):
          RED_SPACESHIP.image=pygame.transform.scale_by(pygame.transform.smoothscale(pygame.transform.rotate(RED_SPACESHIP.image, 14),\
                                                       (RED_SPACESHIP.image.get_width(), RED_SPACESHIP.image.get_height())), 0.99)
        WINNER_TEXT=NORMAL_FONT.render('YELLOW WINS!!!', True, '#FFFF00')
        RESTART.show()
        
      if YELLOW_SPACESHIP_HEALTH<=0:
        disable_yellow=True
        YELLOW_SPACESHIP.disable_down=True
        YELLOW_SPACESHIP.disable_left=True
        YELLOW_SPACESHIP.disable_right=True
        YELLOW_SPACESHIP.disable_up=True
        if not(YELLOW_SPACESHIP.image.get_height()<=0):
          YELLOW_SPACESHIP.image=pygame.transform.scale_by(pygame.transform.smoothscale(pygame.transform.rotate(YELLOW_SPACESHIP.image, -14),\
                                                          (YELLOW_SPACESHIP.image.get_width(), YELLOW_SPACESHIP.image.get_height())), 0.99)
        WINNER_TEXT=NORMAL_FONT.render('RED WINS!!!', True, '#FF0000')
        RESTART.show()
      if YELLOW_SPACESHIP_HEALTH<=0 and RED_SPACESHIP_HEALTH<=0:
        WINNER_TEXT=NORMAL_FONT.render('TIE!', True, '#FFFFFF')
        RESTART.show()
      game_window.blit(WINNER_TEXT, ((WIDTH-WINNER_TEXT.get_width())/2, (HEIGHT-WINNER_TEXT.get_height())/2))
      RESTART.draw(game_window)
      pygame.display.update()
      # tick the clock
      clock.tick(FPS)
      await asyncio.sleep(0)
      for event in pygame.event.get(pygame.QUIT): run=False
    pygame.quit()
    exit()
  finally:
    run=False
    pygame.quit()
    if dev:
      raise
    exit()
if __name__=="__main__": asyncio.run(main())