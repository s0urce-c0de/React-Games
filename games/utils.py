"""
Utilities for games
"""

import pygame
import types
from typing import Union, Tuple, Sequence, Optional
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

class MovingCharacter:
  def __init__(self, image: pygame.surface.SurfaceType, x, y, controls='WASD', max_top: Optional[int] = None, max_left: Optional[int] = None, max_bottom: Optional[int] = None, max_right: Optional[int] = None, disable_left: bool = False, disable_right: bool = False, disable_up: bool = False, disable_down: bool = False, extra_controls=()):
    self.image = image
    self.controls = controls
    self.max_top = max_top
    self.max_left = max_left
    self.max_bottom = max_bottom
    self.max_right = max_right
    self.x = x
    self.y = y
    self.disable_left = disable_left
    self.disable_right = disable_right
    self.disable_up = disable_up
    self.disable_down = disable_down
    self.extra_controls = extra_controls

  def draw(self, target_surf: pygame.surface.SurfaceType, speed: int = 5):
    # Set default values for max_*
    if self.max_bottom is None:
      self.max_bottom = target_surf.get_height()
    if self.max_left is None:
      self.max_left = 0
    if self.max_right is None:
      self.max_right = target_surf.get_width()
    if self.max_top is None:
      self.max_top = 0
      
    # Move the character based on the controls
    keys = pygame.key.get_pressed()

    if self.controls == 'WASD':
      if not self.disable_left and keys[pygame.K_a]:
        self.x -= speed
      if not self.disable_right and keys[pygame.K_d]:
        self.x += speed
      if not self.disable_up and keys[pygame.K_w]:
        self.y -= speed
      if not self.disable_down and keys[pygame.K_s]:
        self.y += speed
    elif self.controls == 'arrow_keys':
      if not self.disable_left and keys[pygame.K_LEFT]:
        self.x -= speed
      if not self.disable_right and keys[pygame.K_RIGHT]:
        self.x += speed
      if not self.disable_up and keys[pygame.K_UP]:
        self.y -= speed
      if not self.disable_down and keys[pygame.K_DOWN]:
        self.y += speed
    else:
      for control in self.controls:
        if not self.disable_left and keys[pygame.key.key_code(control[0])]:
          self.x -= speed
        if not self.disable_right and keys[pygame.key.key_code(control[0])]:
          self.x += speed
        if not self.disable_up and keys[pygame.key.key_code(control[0])]:
          self.y -= speed
        if not self.disable_down and keys[pygame.key.key_code(control[0])]:
          self.y += speed

    # Keep the character within the screen bounds
    self.x = max(self.x, self.max_left)
    self.x = min(self.x, self.max_right - self.image.get_width())
    self.y = max(self.y, self.max_top)
    self.y = min(self.y, self.max_bottom - self.image.get_height())

    # Draw the character on the target surface
    target_surf.blit(self.image, (self.x, self.y))