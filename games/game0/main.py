#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from ..colors import colors
import pygame
from typing import Tuple, List
from pygame.locals import QUIT
from pathlib import Path

p=Path(__file__).resolve().parent

pygame.init()

width = 900
height = 500
game_window = pygame.display.set_mode((width, height))

images = (pygame.transform.scale(pygame.image.load(p/'img1.webp'), (50, 50)), pygame.image.load(p/'img2.png'))

clock = pygame.time.Clock()

class Image(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()

image1 = Image(100, 100, images[0])


def update_window():
    game_window.fill('#FFFFFF')

    game_window.blit(images[0], (100, 100))
    game_window.blit(images[1], (200, 300))

    game_window.blit(image1.image, image1.rect)
    print(image1.rect)
    pygame.display.update()


def main():
    run = True
    while run: # this while is in charge of running our game forever
        # loop through all of the events in pygame
        clock.tick(60)
        update_window()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    image1.rect.x -= 5
                if event.key == pygame.K_RIGHT:
                    image1.rect.x += 5
                if event.key == pygame.K_UP:
                    image1.rect.y -= 5
                if event.key == pygame.K_DOWN:
                    image1.rect.y += 5
                image1.rect = pygame.Rect(image1.rect.x, image1.rect.y, image1.rect.width, image1.rect.height)
            if event.type == 256:
                pygame.quit()
                exit()  

            
        







if __name__=='__main__':
    main()