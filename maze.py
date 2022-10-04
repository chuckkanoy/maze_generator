import sys
import os
from PIL import Image, ImageDraw
from random import randint

LINE_WIDTH = 2
CELL_WIDTH = 25 # must be greater than LINE_WIDTH
FILL_COLOR = 0

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
    def __init__(self, width, height, x_start = 0, y_start = 0):
        self.width = width
        self.height = height
        self.cells = []
        for x in range(width):
            for y in range(height):
                self.cells.append(Cell(x, y))
        self.current_cell = self.find_cell(x_start, y_start)
                
    def find_cell(self, x, y):
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
    
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
        
        print(all_visited)
        
        return False in all_visited
    
    def dfs(self):
        cell = self.current_cell
        if cell.visited:
            print(cell.x, cell.y)
            return
        else:
            cell.visited = True
            while self.check_adj():
                print(cell.x, cell.y)
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

if __name__ == "__main__":
    maze = Maze(20, 20, 0, 0)
    maze.dfs()
    maze.draw()