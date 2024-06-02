import pygame
import sys
from objects import Block, Ball, Paddle

#Initialize the Pygame module
pygame.init()
pygame.mixer.init()

#Initial setup
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/game_music.wav")
ball_paddle_hit_sound = pygame.mixer.Sound("assets/ball_paddle_hit.wav")
ball_hit_brick_sound = pygame.mixer.Sound("assets/ball_hit_brick.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)


#Image loads
bg = pygame.image.load("assets/background.png")
ball_img = pygame.image.load("assets/ball.png")
paddle_img = pygame.image.load("assets/paddle.png")
redblock = pygame.image.load("assets/redblock.png")
orangeblock = pygame.image.load("assets/orangeblock.png")
yellowblock = pygame.image.load("assets/yellowblock.png")
greenblock = pygame.image.load("assets/greenblock.png")
blueblock = pygame.image.load("assets/blueblock.png")
purpleblock = pygame.image.load("assets/purpleblock.png")
cyanblock = pygame.image.load("assets/cyanblock.png")

#Paddle setup
paddle = Paddle(paddle_img, 600,550)
paddle_group = pygame.sprite.GroupSingle(paddle)

#Ball setup
ball = Ball(ball_img, 600, 520)
ball_group = pygame.sprite.GroupSingle(ball)

#Blocks
redlist = [Block(redblock, xpos * 60, 25) for xpos in range(0, 20, 1)]
redgroup = pygame.sprite.Group(redlist)

orangelist = [Block(orangeblock, xpos * 60, 45) for xpos in range(0, 20, 1)]
orangegroup = pygame.sprite.Group(orangelist)

yellowlist = [Block(yellowblock, xpos * 60, 65) for xpos in range(0, 20, 1)]
yellowgroup = pygame.sprite.Group(yellowlist)

greenlist = [Block(greenblock, xpos * 60, 85) for xpos in range(0, 20, 1)]
greengroup = pygame.sprite.Group(greenlist)

bluelist = [Block(blueblock, xpos * 60, 105) for xpos in range(0, 20, 1)]
bluegroup = pygame.sprite.Group(bluelist)

purplelist = [Block(purpleblock, xpos * 60, 125) for xpos in range(0, 20, 1)]
purplegroup = pygame.sprite.Group(purplelist)

cyanlist = [Block(cyanblock, xpos * 60, 145) for xpos in range(0, 20, 1)]
cyangroup = pygame.sprite.Group(cyanlist)

#Booleans
ball_moving = False
running = True


while running:
    clock.tick(60)
    screen.blit(bg, (0, 0))
    paddle_group.draw(screen)
    ball_group.draw(screen)
    redgroup.draw(screen)
    orangegroup.draw(screen)
    yellowgroup.draw(screen)
    greengroup.draw(screen)
    bluegroup.draw(screen)
    purplegroup.draw(screen)
    cyangroup.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    paddle_group.update(keys)

    if not ball_moving:
        if keys[pygame.K_SPACE]:
            ball_moving = True

    if ball_moving:
        if not ball.update():
            ball_moving = False 

        # Ball collision with paddle
        if ball.rect.colliderect(paddle.rect):
            ball.speed_y = -ball.speed_y
            pygame.mixer.Sound.play(ball_paddle_hit_sound)

        # Ball collision with blocks
        hit_block = pygame.sprite.spritecollideany(ball, redgroup) or \
                    pygame.sprite.spritecollideany(ball, orangegroup) or \
                    pygame.sprite.spritecollideany(ball, yellowgroup) or \
                    pygame.sprite.spritecollideany(ball, greengroup) or \
                    pygame.sprite.spritecollideany(ball, bluegroup) or \
                    pygame.sprite.spritecollideany(ball, purplegroup) or \
                    pygame.sprite.spritecollideany(ball, cyangroup)
        if hit_block:
            pygame.mixer.Sound.play(ball_hit_brick_sound)
            ball.speed_y = -ball.speed_y
            hit_block.kill()

    pygame.display.update()                 
