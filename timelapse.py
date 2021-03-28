import sys
import pygame
import pygame_gui
import pygame.camera
from time import sleep
from pygame.locals import *

dimensions = (800, 600)
pygame.init()
pygame.camera.init()
pygame.init()
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((dimensions))
background = pygame.Surface((dimensions))
background.fill(pygame.Color('#000000'))
manager = pygame_gui.UIManager((dimensions))

cam = pygame.camera.Camera('/dev/video0', (800, 600))
cam.start()
image = cam.get_image()
pygame_image = pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect((0, 0), dimensions), image_surface=image, manager=manager)
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           is_running = False
    manager.process_events(event)
    manager.update(time_delta)
    image = cam.get_image()
    pygame_image.set_image(image)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

    """
    wait = int(sys.argv[1])

    camlist = pygame.camera.list_cameras()
    for dev in camlist:
        cam = pygame.camera.Camera(dev, (1024, 768))
        try:
            cam.start()
            image = cam.get_image()
            parts = dev.split("/")
            print('initialized', dev)
            seq = 0
            while True:
                pygame.image.save(image,"%s-filename.jpg" % seq)
                seq += 1
                sleep(wait)
        except Exception as e:
            print('could not initialize', dev, e)
    """
