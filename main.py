from Tokens.token import Token, Player, Platform
import pygame
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
camera_active = False

tokens = [Player()]
dt = 0
camera_scroll_speed = 1
half_camera_boundry = 200

def load_jump_level(jump_size: int):
    
    width = 500
    tokens.append(Platform(0, 500, width, 500))
    tokens.append(Platform(jump_size + width, 500, width, 500))


def get_all_collisions(movable):
    
    collisions = []
    for token in tokens:
        if token != movable and movable.collides(token):
            collisions.append(token)

    return collisions

def move(token):

    if token.velocity.x != 0:
        token.moveX(dt)
        collisions = get_all_collisions(token)
        for collision in collisions:
            if token.velocity.x > 0:
                token.hitbox.x = collision.hitbox.x - token.hitbox.w
            if token.velocity.x < 0:
                token.hitbox.x = collision.hitbox.x + collision.hitbox.w
    if token.velocity.y != 0:
        token.moveY(dt)
        collisions = get_all_collisions(token)
        for collision in collisions:
            if token.velocity.y > 0:
                if isinstance(token, Player):
                    token.is_on_ground = True
                token.hitbox.y = collision.hitbox.y - token.hitbox.h
            if token.velocity.y < 0:
                token.velocity.y = 0
                token.hitbox.y = collision.hitbox.y + collision.hitbox.h

def handle_camera():

    if(isinstance(tokens[0], Player)):
        player = tokens[0]

        if player.hitbox.x > SCREEN_WIDTH/2 - half_camera_boundry:
            for token in tokens:
                token.hitbox.x -= (player.speed - camera_scroll_speed)

        if player.hitbox.x < SCREEN_WIDTH/2 + half_camera_boundry:
            for token in tokens:
                 token.hitbox.x += (player.speed - camera_scroll_speed)

    else:
        print("main.py/handle_camera !! DEBUG:  Player is not index 0")

def get_player():
    if(isinstance(tokens[0], Player)):
        return tokens[0]
    else:
        print("main.py/handle_camera !! DEBUG:  Player is not index 0")

# ---------------------------------------------------
# INTIALISE
#---------------------------------------------------

load_jump_level(200)
goal_x = 800
goal_y = 300
# --------------------------------------------------
# LOOP
# --------------------------------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("gray")

    for token in tokens:
        token.update()
    
    if camera_active:
        handle_camera()
    
    pos_x1 = get_player().hitbox.x
    pos_y1 = get_player().hitbox.y

    for token in tokens:
        move(token)

    pos_x2 = get_player().hitbox.x
    pos_y2 = get_player().hitbox.y

    dist_x = abs(pos_x2 - goal_x) - abs(pos_x1 - goal_x)
    dist_y = abs(pos_y2 - goal_y) - abs(pos_y1 - goal_y)

    for token in tokens:
        token.render(screen)

    for token in reversed(tokens):
        if token.is_dead():
            tokens.remove(token)
    
    get_player().AI.feedback(dist_x + dist_y)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

