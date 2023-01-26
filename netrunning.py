import pygame
from maze import Maze
from consts import WIDTH, CELL_WIDTH, LINE_WIDTH, BACKGROUND_COLOR, \
    FILL_COLOR, RED, GREEN, LEFT, RIGHT, UP, DOWN, PIXEL_WIDTH
from time import sleep
    

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

VELOCITY = .1
MOVE_WAIT = .01

class Netrunning():
    def __init__(self, maze: Maze, width = WIDTH * CELL_WIDTH + LINE_WIDTH, height = WIDTH * CELL_WIDTH + LINE_WIDTH):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Netrunner')
        self.display.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        self.maze = maze
        # maze.dfs()
        maze.draw(display=False)
        self.state = BEGIN
        self.player_icon = pygame.image.load(BASE_PATH + CYBERPUNK_PATH)
        self.convert_PIL_to_surface()
        pygame.display.set_icon(self.player_icon)
        self.player_icon = pygame.transform.scale(self.player_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.dest_icon = pygame.image.load(BASE_PATH + DEST_PATH)
        self.dest_icon = pygame.transform.scale(self.dest_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.acquired_icon = pygame.image.load(BASE_PATH + ENERGY_PATH)
        self.acquired_icon = pygame.transform.scale(self.acquired_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.gameover_icon = pygame.image.load(BASE_PATH + GAME_OVER_PATH)
        self.gameover_icon = pygame.transform.scale(self.gameover_icon, ((int)(CELL_WIDTH * 1 / 2), (int)(CELL_WIDTH * 1 / 2)))
        self.x = 0
        self.y = 0
        self.score = 0
    
    def convert_PIL_to_surface(self):
        self.data = self.maze.maze_drawing.tobytes()
        self.size = self.maze.maze_drawing.size
        self.mode = self.maze.maze_drawing.mode
        self.maze_asset = pygame.image.fromstring(self.data, self.size, self.mode)
        self.rect = self.maze_asset.get_rect()
        
    def draw_cell(self, icon, x, y):
        self.display.blit(icon, (x * CELL_WIDTH + CELL_WIDTH * 1 / 4, y * CELL_WIDTH + CELL_WIDTH * 1 / 4))
        
        end_cell = self.maze.end_cell
        curr_cell = self.maze.current_cell
        
        rectangle = pygame.Rect(curr_cell.x * CELL_WIDTH + LINE_WIDTH,
                                curr_cell.y * CELL_WIDTH + LINE_WIDTH,
                                CELL_WIDTH - LINE_WIDTH,
                                CELL_WIDTH - LINE_WIDTH)
        
        if self.x == end_cell.x and self.y == end_cell.y:
            pygame.draw.rect(surface = self.display,
                             color = GREEN, rect = rectangle)
            self.display.blit(self.acquired_icon, (self.x * CELL_WIDTH + CELL_WIDTH * 1 / 4, self.y * CELL_WIDTH + CELL_WIDTH * 1 / 4))
        elif self.state == LOSS:
            pygame.draw.rect(surface = self.display,
                             color = RED, rect = rectangle)
            self.display.blit(self.gameover_icon, (curr_cell.x * CELL_WIDTH + CELL_WIDTH * 1 / 4, curr_cell.y * CELL_WIDTH + CELL_WIDTH * 1 / 4))
        
        pygame.display.flip()
    
    def move(self, direction):
        if not self.maze.move(direction):
            self.state = LOSS
            self.draw_maze()
            return
        self.draw_move(direction)
        self.x = self.maze.current_cell.x
        self.y = self.maze.current_cell.y
        self.draw_maze()
        current = self.maze.current_cell
        end = self.maze.end_cell
        if current.x == end.x and current.y == end.y:
            self.state = VICTORY
            return
        
    def draw_maze(self):
        self.display.fill(BACKGROUND_COLOR)
        self.display.blit(self.maze_asset, self.rect)
        self.draw_cell(self.player_icon, self.x, self.y)
        self.draw_cell(self.dest_icon, self.maze.end_cell.x, 
                        self.maze.end_cell.y)
        pygame.display.flip()
    
    def draw_move(self, direction):
        dest_x_pix = self.x
        dest_y_pix = self.y
        self.draw_cell(self.player_icon, self.x, self.y)
        
        if direction == LEFT:
            dest_x_pix -= 1
            while self.x > dest_x_pix:
                self.draw_maze()
                self.x -= VELOCITY
                sleep(MOVE_WAIT)
        elif direction == RIGHT:
            dest_x_pix += 1
            while self.x < dest_x_pix:
                self.draw_maze()
                self.x += VELOCITY
                sleep(MOVE_WAIT)
        elif direction == UP:
            dest_y_pix -= 1
            while self.y > dest_y_pix:
                self.draw_maze()
                self.y -= VELOCITY
                sleep(MOVE_WAIT)
        elif direction == DOWN:
            dest_y_pix += 1
            while self.y < dest_y_pix:
                self.draw_maze()
                self.y += VELOCITY
                sleep(MOVE_WAIT)
    
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
        self.draw_menu('DATA ACQUIRED: {}'.format(self.score))
        
    def draw_loss(self):
        self.draw_menu('CONNECTION LOST: {}'.format(self.score))
        
if __name__ == "__main__":
    maze = Maze()
    action_exec = False
    
    net = Netrunning(maze)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif net.state == BEGIN:
                net.draw_begin()
                if event.type == pygame.KEYDOWN:
                    net.x = 0
                    net.y = 0
                    net.maze = Maze(WIDTH, WIDTH)
                    net.maze.dfs()
                    net.maze.draw(display=False)
                    net.convert_PIL_to_surface()
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
                    net.score += 1
                    net.draw_victory()
                    action_exec = True
            elif net.state == LOSS:
                if event.type == pygame.KEYDOWN and action_exec:
                    net.state = BEGIN
                    action_exec = False
                elif event.type == pygame.KEYDOWN:
                    net.draw_loss()
                    action_exec = True
                    net.score = 0