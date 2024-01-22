import pygame
import random

WINDOW_WIDTH:int = 500
WINDOW_HEIGHT:int = 500
pixelSize:int = 25


def draw():

    # Initating the grid cells
    for i in range(0,WINDOW_WIDTH,pixelSize):
        pygame.draw.line(SCREEN,"black",(i,500),(i,0))

    for i in range(0,WINDOW_HEIGHT,pixelSize):
        pygame.draw.line(SCREEN,"black",(500,i),(0,i))

    # Full a grid cell
    x = random.randrange(0,500,25)
    while x%25!=0:
        x = random.randrange(0,500,25)

    y = random.randrange(0,500,25)
    while y%25!=0:
        y = random.randrange(0,500,25)

    pygame.draw.rect(SCREEN,"black",(x,y,25,25),0)





#Pygame Init
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
running = True

while running:

    # Event Zone
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wipe SCREEN
    SCREEN.fill('grey')

    # Drawing Zone
    draw()

    pygame.display.flip()

    CLOCK.tick(10) # Limits FPS to 60
    
pygame.quit()

