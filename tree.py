import pygame
from game import Game


class Tree:
    def __init__(self):
        self.x = Game.width
        self.Tree = pygame.image.load('img/tree.png').convert_alpha()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.Tree
        self.rect = self.Tree.get_rect()
        self.rect.x = self.x
        self.rect.y = Game.height - 50 - self.rect.height
        self.hitbox = [self.rect.x,self.rect.y+5,41,45]

    def showTree(self):
        Game.display.blit(self.Tree, self.rect)

