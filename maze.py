import sys
import os
from tokenize import PlainToken
from PIL import Image, ImageDraw
from random import randint

from consts import WIDTH, CELL_WIDTH, LINE_WIDTH, FILL_COLOR, LEFT, RIGHT, UP,\
    DOWN

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
        self.maze_drawing = None
                
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
        else:
            return False
        
        return True
    
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
    
    def draw(self, display = True):
        self.maze_drawing = Image.new(mode="RGB", 
            size=(self.width * CELL_WIDTH + LINE_WIDTH,
                  self.height * CELL_WIDTH + LINE_WIDTH),
            color=(255, 255, 255))
        drawing = ImageDraw.Draw(self.maze_drawing)
        for cell in self.cells:
            if cell.top:
                drawing.line([(cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH)], 
                                fill=FILL_COLOR, width=LINE_WIDTH)
            if cell.left:
                drawing.line([(cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH)], 
                                fill=FILL_COLOR, width=LINE_WIDTH)
            if cell.bottom:
                drawing.line([(cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH),
                                (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH)], 
                                fill=FILL_COLOR, width=LINE_WIDTH)
            if cell.right:
                drawing.line([(cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH),
                                (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH)], 
                                fill=FILL_COLOR, width=LINE_WIDTH)
        if display:  
            self.maze_drawing.show()

if __name__ == "__main__":
    maze = Maze()
    maze.dfs()
    maze.draw()