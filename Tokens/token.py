import pygame
from Tokens.mistake_learning import Model

class Token:

    def __init__(self, x, y, w, h):
        self.dead = False
        self.hitbox = pygame.Rect(x, y, w, h)
        self.velocity = pygame.Vector2(0, 0)
        self.is_on_ground = False

    def is_dead(self):
        return self.dead

    def update(self):
        pass

    def render(self, g):
        pass

    def collides(self, token):
        return self.hitbox.colliderect(token.hitbox)

    def moveX(self, dt):
        self.hitbox.x += self.velocity.x #* dt

    def moveY(self, dt):
        self.hitbox.y += self.velocity.y #* dt

class Player(Token):

    def __init__(self):
        super().__init__(100, 100, 40, 100)
        self.speed = 10
        self.AI = Model()

    def update(self):

        self.velocity.x = 0
        keys = pygame.key.get_pressed()
        
        move = self.AI.get_move()

        if move == 'A':
            self.velocity.x = -self.speed 
        if move == 'D':
            self.velocity.x = self.speed
        if move == 'W' and self.is_on_ground:
            self.velocity.y = -25

        if self.is_on_ground and self.velocity.y >= 1:
            self.velocity.y = 0
        else:
            self.velocity.y += 1
            if self.velocity.y > 3:
                self.velocity.y += 0.5

            if self.velocity.y > 7:
                self.velocity.y = 7

        self.is_on_ground = False

        if self.hitbox.y > 1200:
            self.respawn()

    def respawn(self):
        self.hitbox.y = 100
        self.hitbox.x = 100 

    def render(self, g):
        pygame.draw.rect(g, (255, 0, 0), self.hitbox)

class Platform(Token):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        

    def render(self, g):
        pygame.draw.rect(g, (255, 255, 0), self.hitbox)
