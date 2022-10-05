import sys
import os
from tokenize import PlainToken
from PIL import Image, ImageDraw
from random import randint
import pygame
from time import sleep

LINE_WIDTH = 2
PIXEL_WIDTH = 500
WIDTH = 5
CELL_WIDTH = (int) (PIXEL_WIDTH / WIDTH) # must be greater than LINE_WIDTH
FILL_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

BEGIN = 0
PLAYING = 1
END = 2


class Cell():
    def __init__(self, x, y):
        self.visited = False
        self.x = x
        self.y = y
        self.top = True
        self.left = True
        self.right = True
        self.bottom = True

class Maze():
    def __init__(self, width = WIDTH, height = WIDTH, x_start = 0, y_start = 0, x_end = WIDTH - 1, y_end = WIDTH - 1):
        self.width = width
        self.height = height
        self.cells = []
        for x in range(width):
            for y in range(height):
                self.cells.append(Cell(x, y))
        self.current_cell = self.find_cell(x_start, y_start)
        self.start_cell = self.find_cell(x_start, y_start)
        self.end_cell = self.find_cell(x_end, y_end)
                
    def find_cell(self, x, y):
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
            
    def move(self, direction):
        cell = self.current_cell
        if direction == UP and cell.y != 0 and not cell.top:
            self.current_cell = self.find_cell(cell.x, cell.y - 1)
        elif direction == DOWN and cell.y < self.height - 1 and not cell.bottom:
            self.current_cell = self.find_cell(cell.x, cell.y + 1)
        elif direction == LEFT and cell.x != 0 and not cell.left:
            self.current_cell = self.find_cell(cell.x - 1, cell.y)
        elif direction == RIGHT and cell.x < self.width - 1 and not cell.right:
            self.current_cell = self.find_cell(cell.x + 1, cell.y)
    
    def check_adj(self):
        all_visited = []
        cell = self.current_cell
        
        if (cell.x > 0):
            all_visited.append(self.find_cell(cell.x - 1, cell.y).visited)
        if (cell.y < self.height - 1):
            all_visited.append(self.find_cell(cell.x, cell.y + 1).visited)
        if (cell.x < self.width - 1):
            all_visited.append(self.find_cell(cell.x + 1, cell.y).visited)
        if (cell.y > 0):
            all_visited.append(self.find_cell(cell.x, cell.y - 1).visited)
        
        return False in all_visited
    
    def dfs(self):
        cell = self.current_cell
        if cell.visited:
            return
        else:
            cell.visited = True
            while self.check_adj():
                direction = randint(0, 3)
                # left
                if (direction == 0 and cell.x > 0 and
                    not self.find_cell(cell.x - 1, cell.y).visited):
                    cell.left = False
                    self.current_cell = self.find_cell(cell.x - 1, cell.y)
                    self.current_cell.right = False
                # down
                elif (direction == 1 and cell.y < self.height - 1 and
                    not self.find_cell(cell.x, cell.y + 1).visited):
                    cell.bottom = False
                    self.current_cell = self.find_cell(cell.x, cell.y + 1)
                    self.current_cell.top = False
                # right
                elif (direction == 2 and cell.x < self.width - 1 and
                    not self.find_cell(cell.x + 1, cell.y).visited):
                    cell.right = False
                    self.current_cell = self.find_cell(cell.x + 1, cell.y)
                    self.current_cell.left = False
                # up
                elif (direction == 3 and cell.y > 0 and
                    not self.find_cell(cell.x, cell.y - 1).visited):
                    cell.top = False
                    self.current_cell = self.find_cell(cell.x, cell.y - 1)
                    self.current_cell.bottom = False
                x = cell.x
                y = cell.y
                self.dfs()
                self.current_cell = self.find_cell(x, y)
    
    def draw(self):
        with Image.new(mode="RGB", size=(self.width * CELL_WIDTH + LINE_WIDTH, 
                                         self.height * CELL_WIDTH + LINE_WIDTH),
                       color=(255, 255, 255)) as im:
            drawing = ImageDraw.Draw(im)
            for cell in self.cells:
                if cell.top and cell.x != 0:
                    drawing.line([(cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                  (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH)], 
                                 fill=FILL_COLOR, width=LINE_WIDTH)
                if cell.left:
                    drawing.line([(cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                  (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH)], 
                                 fill=FILL_COLOR, width=LINE_WIDTH)
                if cell.bottom and cell.x != self.width - 1:
                    drawing.line([(cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH),
                                  (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH)], 
                                 fill=FILL_COLOR, width=LINE_WIDTH)
                if cell.right:
                    drawing.line([(cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH),
                                  (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH)], 
                                 fill=FILL_COLOR, width=LINE_WIDTH)
                
            im.show()
            
class Netrunner():
    def __init__(self, maze: Maze, width = WIDTH * CELL_WIDTH + LINE_WIDTH, height = WIDTH * CELL_WIDTH + LINE_WIDTH):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Netrunner')
        self.display.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        self.maze = maze
        self.state = BEGIN
        
    def draw_cell(self, cell, color):
        rectangle = pygame.Rect(cell.x * CELL_WIDTH,
                                cell.y * CELL_WIDTH,
                                CELL_WIDTH,
                                CELL_WIDTH)
        pygame.draw.rect(surface = self.display,
                         color = color, rect = rectangle)
    
    def move(self, direction):
        self.maze.move(direction)
        
        current = self.maze.current_cell
        end = self.maze.end_cell
        if current.x == end.x and current.y == end.y:
            self.state = END
            return
        
        self.draw_maze()
        
    def draw_maze(self):
        self.display.fill(BACKGROUND_COLOR)
        self.draw_cell(self.maze.current_cell, FILL_COLOR)
        for cell in self.maze.cells:
            if cell.top and cell.x != 0:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
            if cell.left:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
            if cell.bottom and cell.x != self.maze.width - 1:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
            if cell.right:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
        pygame.display.flip()
    
    def draw_begin(self):
        font = pygame.font.Font('punk.ttf', 32)
        text = font.render('NETRUNNING', True, BACKGROUND_COLOR, FILL_COLOR)
        textRect = text.get_rect()
        textRect.center = (PIXEL_WIDTH // 2, PIXEL_WIDTH // 2)
        self.display.fill(FILL_COLOR)
        self.display.blit(text, textRect)
        pygame.display.flip()
    
    def draw_victory(self):
        font = pygame.font.Font('punk.ttf', 32)
        text = font.render('DATA ACQUIRED', True, BACKGROUND_COLOR, FILL_COLOR)
        textRect = text.get_rect()
        textRect.center = (PIXEL_WIDTH // 2, PIXEL_WIDTH // 2)
        self.display.fill(FILL_COLOR)
        self.display.blit(text, textRect)
        pygame.display.flip()

if __name__ == "__main__":
    maze = Maze()
    maze.dfs()
    
    net = Netrunner(maze)
    net.draw_maze()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif net.state == BEGIN:
                net.draw_begin()
                if event.type == pygame.KEYDOWN:
                    net.maze = Maze()
                    net.maze.dfs()
                    net.draw_maze()
                    net.state = PLAYING
            elif net.state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        net.move(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        net.move(RIGHT)
                    elif event.key == pygame.K_UP:
                        net.move(UP)
                    elif event.key == pygame.K_DOWN:
                        net.move(DOWN)
            elif net.state == END:
                net.draw_victory()
                if event.type == pygame.KEYDOWN:
                    net.state = BEGIN