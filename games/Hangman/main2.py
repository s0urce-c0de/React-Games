import dill
import pygame
import io

def pickleable(obj):
    # Serialize the object using dill
    pickled_obj = dill.dumps(obj)
    
    # Deserialize the object using dill
    unpickled_obj = dill.loads(pickled_obj)
    
    return unpickled_obj

# Pygame example
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Pickleable Surface Example')
    
    # Create a surface and fill it with a color
    other_surface = pygame.Surface((100, 100))
    other_surface.fill((255, 0, 0))  # Red color
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Fill the screen with a white background
        
        # Use the pickleable function in the context of surface.blit()
        screen.blit(pickleable(other_surface), (320, 240))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()