#import packages
# pip install pygame
import pygame as pg
import sys
#import pygame
from pygame import display
from pygame.locals import *
import time

# Initialise global variables
game_start = True
XO = 'X'
winner = None
draw = False
width = 400
height = 400
line_color = (10, 10, 10)  # Black Colour line

# TicTacToe 3x3 board
TTT = [[None]*3, [None]*3, [None]*3]

# initialise pygame window
pg.init()  # initialize all imported pygame modules
print('Path to module:', pg.__file__)
fps = 30
CLOCK = pg.time.Clock()  # create an object to help track time
# Initialize a window or screen for display set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
screen = pg.display.set_mode((width, height+100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# initialise the images
x_img = pg.image.load("images/x.png")
o_img = pg.image.load("images/O.png")
opening = pg.image.load("images/splash.jpg")

# resize the images
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height+100))

# define the functions


def game_opening():
    # blit(image, (left, top)) Draw the image to the screen at the given position.
    screen.blit(opening, (0, 0))
    display.update()  # we need to update the display everytime
    time.sleep(1)  # 1sec delay
    screen.fill('white')

    # Draw Vertical Lines
    # draw a straight line line(surface, color, start_pos, end_pos, width)
    pg.draw.line(screen, line_color, (width/3, 0), (width/3, height), 7)
    pg.draw.line(screen, line_color, (2*width/3, 0), (2*width/3, height), 7)

    # Draw Horizontal Lines
    pg.draw.line(screen, line_color, (0, height/3), (width, height/3), 7)
    pg.draw.line(screen, line_color, (0, height/3*2), (width, height/3*2), 7)
    draw_status()


def draw_status():
    global draw,winner
    if (winner == None):
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " WON!"
    if draw:
        message = "Game Draw!"

    font = pg.font.Font(None, 30)  # create a new Font object from a file
    # draw text on a new Surface render(text, antialias, color, background=None)
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message on the board
    # (0,0,0)-> Black colour and position
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    # blit(image, (left, top)) Draw the image to the screen at the given position.
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global TTT, winner, draw

    # check for winning rows
    for row in range(0, 3):
        if (((TTT[row][0]) == (TTT[row][1]) == (TTT[row][2])) and (TTT[row][0] != None)):
            # This row is the winner
            winner = TTT[row][0]
            # draw line from center of the respective row till the end of that row.
            pg.draw.line(screen, (250, 0, 0), (0, (row+1)*height / 3-height/6), (width, (row+1)*height/3-height/6), 4)
            break

    # check for winning coloumns
    for col in range(0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] != None):
            # this column is the winner
            winner = TTT[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width/3 - width/6, 0), ((col + 1) * width/3 - width/6, height), 4)
            break

    # check for diagonal winners
    if((TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] != None)):
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line(screen, (250, 0, 0), (50, 50), (350, 350), 4)

    if((TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] != None)):
        # game won diagonally right to left
        winner = TTT[2][0]
        pg.draw.line(screen, (250, 0, 0), (350, 50), (50, 350), 4)

    if(all([all(row) for row in TTT]) and winner == None):
        draw = True
    draw_status()


def drawXO(row, col):
    global TTT, XO, game_start
    if (row == 1):
        posx = 30
    if (row == 2):
        posx = width/3+30
    if (row == 3):
        posx = width/3*2+30

    if (col == 1):
        posy = 30
    if (col == 2):
        posy = height/3+30
    if (col == 3):
        posy = height/3*2+30
    
    TTT[row-1][col-1] = XO
    
    if (game_start):
        screen.blit(x_img, (posy, posx))
        XO = 'O'
        game_start=False
    else:
        if(XO == 'X'):
            screen.blit(x_img, (posy, posx))
            XO = 'O'
        else:
            screen.blit(o_img, (posy, posx))
            XO = 'X'
    pg.display.update()


def userClick():
    # get coordinates of mouse click
    # Returns the x and y position of the mouse cursor.
    x, y = pg.mouse.get_pos()
    #print(x, y)
    # get coloumn of mouse click
    if (x < width/3):
        col = 1
    elif(x < width/3*2):
        col = 2
    elif(x < width):
        col = 3
    else:
        col = None

   # get row of mouse click
    if (y < height/3):
        row = 1
    elif (y < height/3*2):
        row = 2
    elif (y < height):
        row = 3
    else:
        row = None

    if (row and col and TTT[row-1][col-1] == None):
        global XO
        drawXO(row, col)
    check_win()


def reset_game():
    global TTT, draw, winner, XO, game_start
    time.sleep(3)  # Wait for 3 seconds
    XO = 'X'
    game_start = True
    draw = False
    game_opening()
    winner = None
    TTT = [[None]*3, [None]*3, [None]*3]


game_opening()

# run the game loop forever
while(True):
    for event in pg.event.get():  # get events from the queue
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # The user clicked ; so place an X or O
            userClick()
            if (winner or draw):
                reset_game()
    display.update()
    CLOCK.tick(fps)
