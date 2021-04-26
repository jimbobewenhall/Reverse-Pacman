import pygame
from pygame.locals import *
from constants import *
from ghost import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from pacman import Ghost
from sprites import Spritesheet
from maze import Maze
from ghosts import *
from text import TextGroup
import time

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.sheet = Spritesheet()
        self.maze = Maze(self.sheet)
        self.maze.getMaze('maze1')
        self.maze.constructMaze(self.background)
        self.text = TextGroup()
        self.pelletsEaten = 0
        self.score = 0
        self.pp_time = 0
        self.time_eat = -7000
        self.gameover = False
        self.pac_pellet = 0

        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.nodes = NodeGroup("maze1.txt")
        self.pellets = PelletGroup("pellets1.txt")
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghost = Ghost(self.nodes, self.sheet)
        self.orange_ghost = Orange_Ghost(self.nodes, self.sheet)
        self.blue_ghost = Blue_Ghost(self.nodes, self.sheet)
        self.pink_ghost = Pink_Ghost(self.nodes, self.sheet)
        self.maze.getMaze('maze1')
        self.maze.constructMaze(self.background)
        self.text = TextGroup()
        self.pelletsEaten = 0
        self.score = 0
        self.pp_time = 0
        self.time_eat = -7000
        self.gameover = 3
        self.pac_pellet = 0
        self.start_time = time.time()
        
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        if self.gameover == 3:
            self.pacman.update(dt)
            self.ghost.update(dt)
            self.orange_ghost.update(dt)
            self.blue_ghost.update(dt)
            self.pink_ghost.update(dt)
            self.pellets.update(dt)

            self.checkPelletEvents()
            self.checkEvents()
            self.text.updateScore(self.score)
            if pygame.time.get_ticks() >= self.pp_time+7000:
                self.pacman.speed = 100

            pacman = self.pacman.eatGhost(self.ghost)
            if pacman:
                if int(time.time()) > int(self.start_time)+1:
                    if self.pac_pellet == 1:
                        self.text.Pac_win('PACMAN WINS')
                        self.gameover = 0
                    else:
                        self.text.Pac_win('YOU WIN')
                        self.gameover = 1

        elif self.gameover == 0 or self.gameover == 1:
            time.sleep(0.1)
            event = pygame.event.wait()
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                self.startGame()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pelletsEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.pacman.speed = 150
                self.pp_time = pygame.time.get_ticks()

        pacman_pellet = self.ghost.eatPellets(self.pellets.pelletList)
        runs = 0
        if pacman_pellet:
            if pacman_pellet.name == 'powerpellet':
                if runs == 0:
                    runs = runs+1
                    self.pellets.pelletList.remove(pacman_pellet)
                    self.pac_pellet = 1
                    self.time_eat = pygame.time.get_ticks()
            else:
                self.pellets.pelletList.remove(pacman_pellet)
            self.score += pacman_pellet.points
        if pygame.time.get_ticks() > self.time_eat+7000:
            self.pac_pellet = 0
            runs = 0

            
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)

        self.orange_ghost.render(self.screen)
        self.blue_ghost.render(self.screen)
        self.pink_ghost.render(self.screen)
        self.text.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
