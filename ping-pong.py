from pygame import *
import os

clock = time.Clock()

x = 200
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# Window
global_height = 700
global_width = 700
window = display.set_mode((global_width,global_height))

display.set_caption("Shooter")
display.set_icon(image.load("background.jpg"))
background = transform.scale(image.load("background.jpg"), (global_height, global_width))

# Variables
game_Play = True

while game_Play:

    window.blit(background, (0,0))

    for event_get in event.get():
        if event_get.type == QUIT:
            game_Play = False

    display.update()

    clock.tick(60)