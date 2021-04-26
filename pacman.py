import pygame
from entity import Entity
from constants import *
from vector import Vector2
from random import randint

class Ghost(Entity):
    def __init__(self, nodes, spritesheet):
        Entity.__init__(self, nodes, spritesheet)
        self.name = "ghost"
        self.image = self.spritesheet.getImage(0, 1, 32, 32)
        self.points = 200

    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.forceBacktrack())
        return validDirections
    
    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]

    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            self.portal()
            validDirections = self.getValidDirections()
            self.direction = self.randomDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()
            
    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT
        
    def portalSlowdown(self):
        self.speed = 100
        if self.node.portalNode or self.target.portalNode:
            self.speed = 50

    def eatPellets(self, pelletList):
        for pacman_pellet in pelletList:
            d = self.position - pacman_pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pacman_pellet.radius+self.collideRadius)**2
            if dSquared <= rSquared:
                return pacman_pellet
        return None

    def eatPacman(self, pacman):
        d = self.position - pacman.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + pacman.collideRadius)**2
        if dSquared <= rSquared:
            return pacman
        return None

