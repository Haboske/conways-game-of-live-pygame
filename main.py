import pygame
import random
import time

# Config Init
WINDOW_WIDTH:int = 600 # Determine the game's window's width
WINDOW_HEIGHT:int = 600 # Determine the game's window's height
PIXELSIZE:int = 10 # Size of cells (L*W)
MAX_STARTING_CELLS:int = (((WINDOW_WIDTH+WINDOW_HEIGHT)/2)/PIXELSIZE)*(((WINDOW_WIDTH+WINDOW_HEIGHT)/2)/PIXELSIZE) # The number of maximum alived cells we could initiate the game with

#Pygame Init
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
STATE:bool=True # State used to put the game in pause or play


# I initiate de list that'll contain of my alive cells
cellsList:list[list[int,int]]=[]


def initiateCellsList():
    cellsList.clear()

    n:int = random.randrange(0,MAX_STARTING_CELLS/2,1)
    i:int = 0
    while i <= n:
        cellsList.append([random.randrange(0,WINDOW_WIDTH,PIXELSIZE),random.randrange(0,WINDOW_HEIGHT,PIXELSIZE)])
        i+=1

def update():

    # We create a toCreate and toDelete lists to not create or delete any cell during the "scan", otherwise the algo wouldn't work if we work live on the cellsList
    toDeleteList:list[list[int,int]]=[]
    toCreateList:list[list[int,int]]=[]

    if STATE: # If game in play (True)

        x:int=0
        while x <= WINDOW_WIDTH/PIXELSIZE:

            y:int=0
            while y <= WINDOW_HEIGHT/PIXELSIZE:

                elem:list[int,int]=[x*PIXELSIZE,y*PIXELSIZE]

                if elem in cellsList: # We check if actual cell is alive

                    # We count the alive cells around the actual cell to further determine if we make it die or live arounds after conway's rules
                    cellsAround:int = 0 
                    cellsAround +=1 if [(x+1)*PIXELSIZE,(y+1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x-1)*PIXELSIZE,(y-1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x+1)*PIXELSIZE,(y-1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x-1)*PIXELSIZE,(y+1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x+1)*PIXELSIZE,y*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [x*PIXELSIZE,(y+1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x-1)*PIXELSIZE,y*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [x*PIXELSIZE,(y-1)*PIXELSIZE] in cellsList else +0

                    if cellsAround > 3 : # Any live cell with more than three live neighbours dies, as if by overpopulation.
                        toDeleteList.append(elem)
                    elif cellsAround < 2 : # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                        toDeleteList.append(elem)
                
                else: # We check if actual cell is dead

                    cellsAround:int = 0
                    cellsAround +=1 if [(x+1)*PIXELSIZE,(y+1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x-1)*PIXELSIZE,(y-1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x+1)*PIXELSIZE,(y-1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x-1)*PIXELSIZE,(y+1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x+1)*PIXELSIZE,y*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [x*PIXELSIZE,(y+1)*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [(x-1)*PIXELSIZE,y*PIXELSIZE] in cellsList else +0
                    cellsAround +=1 if [x*PIXELSIZE,(y-1)*PIXELSIZE] in cellsList else +0

                    if cellsAround == 3: # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                        toCreateList.append([x*PIXELSIZE,y*PIXELSIZE])

                y+=1
            x+=1

        for i in toDeleteList:
            del cellsList[cellsList.index([i[0],i[1]])]
        
        for i in toCreateList:
            cellsList.append([i[0],i[1]])

    # Small instructions that allow us to manually create alive cells by clicking with the mouse on a cell.
    if pygame.mouse.get_pressed()[0]:
        point = pygame.mouse.get_pos()
        xPos = (point[0]//PIXELSIZE)*PIXELSIZE
        yPos = (point[1]//PIXELSIZE)*PIXELSIZE
        cellsList.append([xPos,yPos])

    
def draw():

    # Initating the grid cells
    for i in range(0,WINDOW_WIDTH,PIXELSIZE):
        pygame.draw.line(SCREEN,"black",(i,WINDOW_HEIGHT),(i,0))

    for i in range(0,WINDOW_HEIGHT,PIXELSIZE):
        pygame.draw.line(SCREEN,"black",(WINDOW_WIDTH,i),(0,i))


    for i in cellsList:
        pygame.draw.rect(SCREEN,"black",(i[0],i[1],PIXELSIZE,PIXELSIZE),0)

    # Small instructions that allow us to show the mouse cursor in game with a Blue square
    point = pygame.mouse.get_pos()
    xPos = (point[0]//PIXELSIZE)*PIXELSIZE
    yPos = (point[1]//PIXELSIZE)*PIXELSIZE
    pygame.draw.rect(SCREEN,"blue",(xPos,yPos,PIXELSIZE,PIXELSIZE),0)

GAME = True
initiateCellsList()
while GAME:

    # Event Zone
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        if event.type == pygame.KEYDOWN:
            if event.key == 32: # Game pause/play instructions
                if STATE == True:
                    STATE = False
                elif STATE == False:
                    STATE = True
                
            else: # Reinit the game by wiping out and generate new cells
                initiateCellsList()

    # Wipe SCREEN
    SCREEN.fill('grey')

    # Update Zone
    update()
    
    # Drawing Zone
    draw()

    pygame.display.flip()
    CLOCK.tick(10) # Limits FPS to 60
    
pygame.quit()

