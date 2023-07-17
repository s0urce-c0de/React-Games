"""
Utilities for games
"""

import pygame
import types
import importlib
import sys
from pathlib import Path
try:
  from pygame._common import ColorValue, Coordinate
except ModuleNotFoundError:
  from typing import Union, Tuple, Sequence
  RGBOutput=Tuple[int, int, int]
  RGBAOutput=Tuple[int, int, int, int]
  Coordinate = Union[Tuple[float, float], Sequence[float], pygame.math.Vector2]
  ColorValue=Union[pygame.color.Color, int, str, RGBOutput, RGBAOutput, Sequence[int]]
pygame.init()
class CircleButton:
  """
  A PyGame Circular Button.
  Assumes that you constantly blit in 
  `while True` game loop
  """
  def __init__(self, x: int, y: int, radius: int, thickness: int =1, color: ColorValue= "#000000", \
        image: pygame.surface.SurfaceType = pygame.font.SysFont(None, 0).render('', True, "#000000"), \
        onClick: types.FunctionType = (lambda *args, **kwargs: ...), *onClickArgs, **onClickKwargs) -> None:
    """
    Initialize The Button
    """
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
  def draw(self, screen: pygame.surface.SurfaceType, force_draw=False) -> None:
    """
    Draw the button correctly
    """
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    hover = self.is_hover(mouse_pos)
    if self.should_draw and not force_draw:
      pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.thickness)
      screen.blit(self.image, (self.x-self.radius, self.y-self.radius))
      if hover and mouse_clicked and not self.clicked:
        self.onclick(*self.onclickargs, **self.onclickkwargs)
        self.clicked=True
      elif not mouse_clicked:
        self.clicked=False
  
  def is_hover(self, mouse_pos) -> bool:
    """
    Check if mouse is hover over button
    """
    distance = ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5
    return distance <= self.radius
class PicklableSurface:
  """
  Representation of pygame.surface.Surface, but it can be pickled
  """
  def __init__(self, surface: pygame.surface.SurfaceType) -> None:
    """
    Initialize class
    """
    self.surface = surface
    self.name = "PicklableSurface"

  def __getstate__(self) -> dict:
    """
    Send string object through pickle
    """
    state = self.__dict__.copy()
    surface = state.pop("surface")
    state["surface_string"] = (pygame.image.tostring(surface, "RGBA"), surface.get_size())
    return state

  def __setstate__(self, state) -> None:
    """
    Get surface object when pickle is setting item
    """
    surface_string, size = state.pop("surface_string")
    state["surface"] = pygame.image.fromstring(surface_string, size, "RGBA")
    self.__dict__.update(state)
  
  def __getattr__(self, attr) -> object:
    """
    Help compatibility by forwarding methods to the surface
    """
    return eval(f"self.surface.{attr}")
def MultiLineText_Blit(surface: pygame.surface.SurfaceType, text: str, pos: Coordinate, font: pygame.font.FontType = pygame.font.SysFont(None, 10), color=pygame.Color('black')) -> None:
  """
  Blit Muli-Line text to surface.
  Note: Text can overflow down
  """
  words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
  space = font.size(' ')[0]  # The width of a space.
  max_width, max_height = surface.get_size()
  x, y = pos
  for line in words:
    for word in line:
      word_surface = font.render(word, True, color)
      word_width, word_height = word_surface.get_size()
      if x + word_width >= max_width:
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
      surface.blit(word_surface, (x, y))
      x += word_width + space
    x = pos[0]  # Reset the x.
    y += word_height  # Start on new row.
