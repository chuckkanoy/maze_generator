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
            print(cell.x, cell.y)
            if cell.x == x and cell.y == y:
                return cell
    
    # def check_adj(self):
    #     all_visited = True
    #     cell = self.current_cell
    #     if (cell.x > 0):
    #         self.find_cell(cell.x - 1, cell.y)
    #     elif (direction == 1 and cell.y < self.height - 1
    #     ):
    #         cell.bottom = False
    #         self.current_cell = self.find_cell(cell.x, cell.y + 1)
    #         self.current_cell.top = False
    #         moved = True
    #         self.dfs()
    #     # right
    #     elif (direction == 2 and cell.x < self.width - 1
    #     ):
    #         cell.right = False
    #         self.current_cell = self.find_cell(cell.x + 1, cell.y)
    #         self.current_cell.left = False
    #         moved = True
    #         self.dfs()
    #     # up
    #     elif (direction == 3 and cell.y > 0
    #     ):
    #         cell.top = False
    #         self.current_cell = self.find_cell(cell.x, cell.y - 1)
    #         self.current_cell.bottom = False
    #         moved = True
    #         self.dfs()
    
    def dfs(self):
        cell = self.current_cell
        print(cell.x, cell.y)
        if cell.visited:
            print('visited')
            return
        else:
            cell.visited = True
            moved = False
            while not moved:
                direction = randint(0, 3)
                print(direction)
                # left
                if (direction == 0 and cell.x > 0
                ):
                    cell.left = False
                    self.current_cell = self.find_cell(cell.x - 1, cell.y)
                    self.current_cell.right = False
                    moved = True
                    self.dfs()
                # down
                elif (direction == 1 and cell.y < self.height - 1
                ):
                    cell.bottom = False
                    self.current_cell = self.find_cell(cell.x, cell.y + 1)
                    self.current_cell.top = False
                    moved = True
                    self.dfs()
                # right
                elif (direction == 2 and cell.x < self.width - 1
                ):
                    cell.right = False
                    self.current_cell = self.find_cell(cell.x + 1, cell.y)
                    self.current_cell.left = False
                    moved = True
                    self.dfs()
                # up
                elif (direction == 3 and cell.y > 0
                ):
                    cell.top = False
                    self.current_cell = self.find_cell(cell.x, cell.y - 1)
                    self.current_cell.bottom = False
                    moved = True
                    self.dfs()
    
    def draw(self):
        with Image.new(mode="RGB", size=(self.width * CELL_WIDTH + LINE_WIDTH, 
                                         self.height * CELL_WIDTH + LINE_WIDTH),
                       color=(255, 255, 255)) as im:
            drawing = ImageDraw.Draw(im)
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
                
            im.show()

if __name__ == "__main__":
    maze = Maze(5, 4, 0, 0)
    maze.dfs()
    maze.draw()