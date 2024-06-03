import pygame
import sys
from objects import Block, Ball, Paddle, Button

#Initialize the Pygame module
pygame.init()
pygame.mixer.init()


#Initial setup
screen = pygame.display.set_mode((1200, 600))
text_font = pygame.font.SysFont("Courier", 50)
controls_font = pygame.font.SysFont("Courier", 25)
text_color = (255, 255, 255)
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/game_music.wav")
ball_paddle_hit_sound = pygame.mixer.Sound("assets/ball_paddle_hit.wav")
ball_hit_brick_sound = pygame.mixer.Sound("assets/ball_hit_brick.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)


#Globals
BALL_MOVING = False
SCORE = 0
LIVES = 3
MAIN_MENU = True


#Image loads
bg = pygame.image.load("assets/background.png")
ball_img = pygame.image.load("assets/ball.png")
paddle_img = pygame.image.load("assets/paddle.png")
start_img = pygame.image.load("assets/start.png")
quit_img = pygame.image.load("assets/quit.png")
block_images = [
    pygame.image.load("assets/redblock.png"),
    pygame.image.load("assets/orangeblock.png"),
    pygame.image.load("assets/yellowblock.png"),
    pygame.image.load("assets/greenblock.png"),
    pygame.image.load("assets/blueblock.png"),
    pygame.image.load("assets/purpleblock.png"),
    pygame.image.load("assets/cyanblock.png"),
]



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


def draw_main_menu():
    screen.blit(bg, (0,0))
    draw_text("Main Menu", text_font, text_color, 465, 100)
    draw_text("Controls:", controls_font, text_color, 10, 120)
    draw_text("Space = Shoot", controls_font, text_color, 10, 150)
    draw_text("Left arrow = Move left", controls_font, text_color, 10, 180)
    draw_text("Right arrow = Move right", controls_font, text_color, 10, 210)
    draw_text("Escape = Return to main menu", controls_font, text_color, 10, 240)
    start_group.draw(screen)
    quit_group.draw(screen)


def draw_game():
    screen.blit(bg, (0,0))
    paddle_group.draw(screen)
    ball_group.draw(screen)
    draw_text(f"SCORE:{SCORE}", text_font, text_color, 0, 0)
    draw_text(f"LIVES:{LIVES}", text_font, text_color, 990, 0)   
    for block_group in block_groups:
        block_group.draw(screen)

def handle_collisions():
    global BALL_MOVING, SCORE
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y = -ball.speed_y
        pygame.mixer.Sound.play(ball_paddle_hit_sound)

    for block_group in block_groups:
        hit_block = pygame.sprite.spritecollideany(ball, block_group)
        if hit_block:
            pygame.mixer.Sound.play(ball_hit_brick_sound)
            ball.speed_y = -ball.speed_y
            hit_block.kill()
            SCORE += 10 

def update_game_state(keys):
    global BALL_MOVING, LIVES
    paddle_group.update(keys)

    if not BALL_MOVING:
        if keys[pygame.K_SPACE]:
            BALL_MOVING = True

    if BALL_MOVING:
        if not ball.update():
            BALL_MOVING = False
            LIVES -= 1

                                        
#Paddle setup
paddle = Paddle(paddle_img, 600,550)
paddle_group = pygame.sprite.GroupSingle(paddle)

#Ball setup
ball = Ball(ball_img, 600, 520)
ball_group = pygame.sprite.GroupSingle(ball)

#Button setup
start = Button(start_img, 600, 300)
start_group = pygame.sprite.GroupSingle(start)
_quit = Button(quit_img, 600, 400)
quit_group = pygame.sprite.GroupSingle(_quit)

#Blocks
block_groups = []
def generate_level():
    global block_groups
    block_groups = []
    for i, block_image in enumerate(block_images):
        block_list = [Block(block_image, xpos * 60, 60 + i * 20) for xpos in range(20)]
        block_group = pygame.sprite.Group(block_list)
        block_groups.append(block_group)

#Game loop
running = True
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    if MAIN_MENU:
        draw_main_menu()   
    else:    
        draw_game()
        update_game_state(keys)
        handle_collisions()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if start.is_click():
        generate_level()
        MAIN_MENU = False
        BALL_MOVING = False
        SCORE = 0
        LIVES = 3
        paddle.rect.midbottom = (600, 550)
        ball.rect.midbottom = (600, 520)
    if _quit.is_click():
        pygame.quit()
        sys.exit()
    if keys[pygame.K_ESCAPE] == True:
        MAIN_MENU = True        

    pygame.display.update()                 
