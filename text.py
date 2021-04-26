import pygame
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, color, x, y, size, show=True):
        self.text = text
        self.color = color
        self.size = size
        self.position = Vector2(x, y)
        self.show = show
        self.label = None
        self.font = None
        self.setupFont("PressStart2P-vaV7.ttf")
        self.createLabel()

    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newtext):
        self.text = newtext
        self.createLabel()

    def render(self, screen):
        if self.show:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))
    



class TextGroup(object):
    def __init__(self):
        self.textlist = {}
        self.setupText()
        self.tempText = []
        
    def setupText(self):
        self.textlist["score_label"] = Text("SCORE", WHITE, 0, 0, TILEHEIGHT)
        self.textlist["score"] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, TILEHEIGHT)

    def Pac_win(self, winner):
        self.textlist["score_label"] = Text(winner, WHITE, 160, 270, TILEHEIGHT)

    def update(self, dt):
        if len(self.tempText) > 0:
            tempText = []
            for text in self.tempText:
                text.update(dt)
                if text.show:
                    tempText.append(text)
            self.tempText = tempText
            
    def updateScore(self, score):
        self.textlist["score"].setText(str(score).zfill(8))

    def createTemp(self, value, position):
        x, y = position.asTuple()
        text = Text(str(value), WHITE, x, y, 8)
        text.lifespan = 1
        self.tempText.append(text)

    def render(self, screen):
        for key in self.textlist.keys():
            self.textlist[key].render(screen)

        for item in self.tempText:
            item.render(screen)
