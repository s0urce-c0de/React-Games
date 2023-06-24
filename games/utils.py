

"""
Utilities for games
"""

import pygame
import types
import re

pygame.init()

class Image(pygame.sprite.Sprite):
  def __init__(self, x, y, image) -> None:
    super().__init__()
    self.x = x
    self.y = y
    self.image = image
    self.rect = self.image.get_rect()
class Button:
    def __init__(self, x: int, y: int, radius: int, thickness: int =1, color = "#000000", \
                 image: pygame.surface.Surface = pygame.font.SysFont(None, 0).render('', True, "#000000"), \
                 onClick: types.FunctionType = (lambda: None), *onClickArgs, **onClickKwargs) -> None:
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
    def draw(self, screen) -> None:
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
    
    def is_hover(self, mouse_pos) -> bool:
        distance = ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5
        return distance <= self.radius
class PicklableSurface:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.name = "PicklableSurface"

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        surface = state.pop("surface")
        state["surface_string"] = (pygame.image.tostring(surface, "RGB"), surface.get_size())
        return state

    def __setstate__(self, state) -> None:
        surface_string, size = state.pop("surface_string")
        state["surface"] = pygame.image.fromstring(surface_string, size, "RGB")
        self.__dict__.update(state)
    
    def __getattr__(self, attr) -> object:
      return eval(f"self.surface.{attr}")