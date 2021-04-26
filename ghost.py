import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Pacman(Entity):
    def __init__(self, nodes, spritesheet):
        Entity.__init__(self, nodes, spritesheet)
        self.name = "pacman"
        self.color = YELLOW
        self.image = self.spritesheet.getImage(0, 2, 32, 32)
        self.lifeicons = self.spritesheet.getImage(0, 1, 32, 32)

    def update(self, dt):
        self.position += self.direction*self.speed*dt
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.moveBySelf()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return None

    def moveByKey(self, direction):
        if self.direction is STOP:
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction
        else:
            if direction == self.direction * -1:
                self.reverseDirection()
            if self.overshotTarget():
                self.node = self.target
                self.portal()
                if self.node.neighbors[direction] is not None:
                    self.target = self.node.neighbors[direction]
                    if self.direction != direction:
                        self.setPosition()
                        self.direction = direction
                else:
                    if self.node.neighbors[self.direction] is not None:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.setPosition()
                        self.direction = STOP

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius+self.collideRadius)**2
            if dSquared <= rSquared  and pellet.name == 'powerpellet':
                return pellet
        return None

    def eatGhost(self, ghost):
        d = self.position - ghost.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + ghost.collideRadius)**2
        if dSquared <= rSquared:
            return ghost
        return None
