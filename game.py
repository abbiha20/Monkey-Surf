import pygame
import random
import cv2
from PIL import Image
import numpy as np
import train


class Game:
    pygame.init()
    clock = pygame.time.Clock()
    width = 1024
    height = 500
    black = (0, 0, 0)
    white = (255, 255, 255)
    display = pygame.display.set_mode((width, height))
    gameExit = False
    tree = pygame.image.load('img/tree.png').convert_alpha()
    pygame.display.set_caption("Monkey Surf")
    tree_rect = tree.get_rect()
    trees = []
    counter = 0
    camera = cv2.VideoCapture(0)
    exit = False
    score = 0
    cac = False

    def __init__(self):
        from monkey import Monkey
        self.aab = Monkey()
        self.model = train.load_model()
        self.model.load_weights('weights.h5')
        self.create_and_resize_window()
        self.intro()

    def create_and_resize_window(self):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 300, 350)

    def intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.gameloop()
            self.display.fill(self.white)
            largeText = pygame.font.Font('freesansbold.ttf', 100)
            textSurf = largeText.render("Press SPACE to play", True, self.black)
            textRect = textSurf.get_rect()
            textRect.center = ((self.width / 2), (self.height / 2))
            self.display.blit(textSurf, textRect)
            pygame.display.update()
            self.clock.tick(30)

    def gameloop(self):

        while not self.gameExit:
            self.display.fill(self.white)
            pygame.draw.line(self.display, self.black, (0, self.height - 50), (self.width, self.height - 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
            if self.counter % (random.randrange(100, 110)) == 0:
                self.cac = True
                from tree import Tree
                self.trees.append(Tree())
            for c in self.trees:
                c.showTree()
                c.hitbox = [c.rect.x, c.rect.y + 5, 41, 45]
                c.rect.x -= 13
                if c.rect.x <= -c.rect.width:
                    self.trees = self.trees[1:]
            pic = self.take_photo()
            result = self.predict(pic)
            if result == 0:
                pass
            else:
                self.aab.jump()
            self.aab.updateVariables()
            self.score += 1
            text = pygame.font.Font('freesansbold.ttf', 20)
            textSurf = text.render("Score: " + str(self.score), True, self.black)
            self.display.blit(textSurf, [10, 10])
            self.aab.show()
            self.aabHitbox = pygame.Rect(self.aab.hitbox)
            pygame.display.update()
            if self.aab.var > 50:
                self.aab.var -= 10
            if self.collision() and self.cac:
                self.gameExit = True
            self.clock.tick(30)
            self.counter += 1
        pygame.quit()
        self.camera.release()
        cv2.destroyAllWindows()
        quit()

    def take_photo(self):
        return_value, image = self.camera.read()
        cv2.imshow('image', image)
        cv2.resizeWindow('image', 300, 350)  # Move this line here
        im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = im.resize((100, 100))
        im = np.array(im)
        im = np.resize(im, (1, 100, 100, 3))
        im = (im.astype(float) - 128) / 128
        return im

    def predict(self, pic):
        prob = self.model.predict(pic)
        result = np.argmax(prob)
        return result

    def collision(self):
        for tree in self.trees:
            if self.aabHitbox.colliderect(pygame.Rect(tree.hitbox)):
                return True
        return False


if __name__ == '__main__':
    g = Game()
