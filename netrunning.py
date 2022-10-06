import pygame
from maze import Maze
from consts import WIDTH, CELL_WIDTH, LINE_WIDTH, BACKGROUND_COLOR, \
    FILL_COLOR, RED, GREEN, LEFT, RIGHT, UP, DOWN, PIXEL_WIDTH
    

BASE_PATH = 'assets\\'
PUNK_FONT_PATH = 'punk.ttf'
CYBERPUNK_PATH = 'cyberpunk.png'
DEST_PATH = 'dest.png'
ENERGY_PATH = 'energy-drink.png'
GAME_OVER_PATH = 'game-over.png'

BEGIN = 0
PLAYING = 1
VICTORY = 2
LOSS = 3

class Netrunning():
    def __init__(self, maze: Maze, width = WIDTH * CELL_WIDTH + LINE_WIDTH, height = WIDTH * CELL_WIDTH + LINE_WIDTH):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Netrunner')
        self.display.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        self.maze = maze
        self.state = BEGIN
        self.player_icon = pygame.image.load(BASE_PATH + CYBERPUNK_PATH)
        pygame.display.set_icon(self.player_icon)
        self.player_icon = pygame.transform.scale(self.player_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.dest_icon = pygame.image.load(BASE_PATH + DEST_PATH)
        self.dest_icon = pygame.transform.scale(self.dest_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.acquired_icon = pygame.image.load(BASE_PATH + ENERGY_PATH)
        self.acquired_icon = pygame.transform.scale(self.acquired_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.gameover_icon = pygame.image.load(BASE_PATH + GAME_OVER_PATH)
        self.gameover_icon = pygame.transform.scale(self.gameover_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        
    def draw_cell(self, cell, icon):
        self.display.blit(icon, (cell.x * CELL_WIDTH + CELL_WIDTH * 1 / 4, cell.y * CELL_WIDTH + CELL_WIDTH * 1 / 4))
        
        end_cell = self.maze.end_cell
        curr_cell = self.maze.current_cell
        
        rectangle = pygame.Rect(curr_cell.x * CELL_WIDTH + LINE_WIDTH,
                                curr_cell.y * CELL_WIDTH + LINE_WIDTH,
                                CELL_WIDTH - LINE_WIDTH,
                                CELL_WIDTH - LINE_WIDTH)
        
        if curr_cell.x == end_cell.x and curr_cell.y == end_cell.y:
            pygame.draw.rect(surface = self.display,
                             color = GREEN, rect = rectangle)
            self.display.blit(self.acquired_icon, (cell.x * CELL_WIDTH + CELL_WIDTH * 1 / 4, cell.y * CELL_WIDTH + CELL_WIDTH * 1 / 4))
        elif self.state == LOSS:
            pygame.draw.rect(surface = self.display,
                             color = RED, rect = rectangle)
            self.display.blit(self.gameover_icon, (curr_cell.x * CELL_WIDTH + CELL_WIDTH * 1 / 4, curr_cell.y * CELL_WIDTH + CELL_WIDTH * 1 / 4))
    
    def move(self, direction):
        if not self.maze.move(direction):
            self.state = LOSS
            self.draw_maze()
            return
        self.draw_maze()
        current = self.maze.current_cell
        end = self.maze.end_cell
        if current.x == end.x and current.y == end.y:
            self.state = VICTORY
            return
        
    def draw_maze(self):
        self.display.fill(BACKGROUND_COLOR)
        self.draw_cell(self.maze.current_cell, self.player_icon)
        for cell in self.maze.cells:
            if cell.top:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
            if cell.left:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
            if cell.bottom:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH), 
                                color=FILL_COLOR, width=LINE_WIDTH)
            if cell.right:
                pygame.draw.line(surface = self.display,
                                 start_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH),
                                end_pos = (cell.x * CELL_WIDTH + CELL_WIDTH, cell.y * CELL_WIDTH + CELL_WIDTH + LINE_WIDTH / 2), 
                                color=FILL_COLOR, width=LINE_WIDTH)
        self.draw_cell(self.maze.end_cell, self.dest_icon)
        pygame.display.flip()
    
    def draw_menu(self, text):
        font = pygame.font.Font(BASE_PATH + PUNK_FONT_PATH, 32)
        text = font.render(text, True, BACKGROUND_COLOR, FILL_COLOR)
        textRect = text.get_rect()
        textRect.center = (PIXEL_WIDTH // 2, PIXEL_WIDTH // 2)
        self.display.fill(FILL_COLOR)
        self.display.blit(text, textRect)
        pygame.display.flip()
        
    def draw_begin(self):
        self.draw_menu('NETRUNNING')
    
    def draw_victory(self):
        self.draw_menu('DATA ACQUIRED')
        
    def draw_loss(self):
        self.draw_menu('CONNECTION LOST')
        
if __name__ == "__main__":
    maze = Maze()
    maze.dfs()
    action_exec = False
    
    net = Netrunning(maze)
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
            elif net.state == VICTORY:
                if event.type == pygame.KEYDOWN and action_exec:
                    net.state = BEGIN
                    action_exec = False
                elif event.type == pygame.KEYDOWN:
                    net.draw_victory()
                    action_exec = True
            elif net.state == LOSS:
                if event.type == pygame.KEYDOWN and action_exec:
                    net.state = BEGIN
                    action_exec = False
                elif event.type == pygame.KEYDOWN:
                    net.draw_loss()
                    action_exec = True