import pygame
import random
import os
import sys

# Initial Settings
pygame.init()
print('Welcome to the Classic Pong'
      '\n----------------------------'
      '\nDeveloped By Sheikh Abdullah')
clock = pygame.time.Clock()
FPS = 60
scn_width = 600
scn_height = 800
# Screen Initializer
screen = pygame.display.set_mode((scn_width, scn_height))
# Images Loading
icon = pygame.image.load('assets\\ClassicPong.png').convert_alpha()
contact = pygame.image.load('assets\\Contact.png').convert_alpha()
how_to_play_text = pygame.image.load('assets\\HowToPlay.png').convert_alpha()
downsized_icon = pygame.transform.scale(icon, (32, 32))

# Title Bar Icon And Caption Setting
pygame.display.set_icon(downsized_icon)
pygame.display.set_caption("Classic Pong By Abdullah")

# Gives the path of current folder
current_dir = os.path.relpath(".")
font_path = os.path.join(current_dir, 'assets\\blocky.ttf')

# Color Scheme
black = (20, 20, 20)
white = (255, 255, 255)

# Score Counters
player_score = 0
opp_score = 0

# Reads Highscore
highscore = 0
try:
    with open('data.txt', 'r') as f:
        data = f.read()
        highscore = int(data)
# On first-time play in a system, It'll create a new record file
except (FileNotFoundError, ValueError):
    with open('data.txt', 'w') as f:
        f.write('0')


# Score Display
def score_counter(num, y):
    if num > 9:
        screen.blit(text_surface(100, num, white), (480, y))
    else:
        screen.blit(text_surface(100, num, white), (530, y))


# Resets Both Player Score To Zero
def reset_score():
    global opp_score, player_score
    opp_score = 0
    player_score = 0


# Enables close button and saves highscore on exit
def save_and_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Saves the Highscore locally
            with open('data.txt', 'w') as f:
                f.write(str(highscore))
            pygame.quit()
            sys.exit()


# Creates text object
def text_surface(size, text, color):
    font = pygame.font.Font(font_path, round(size))
    return font.render(str(text), False, color)


# FUNCTIONAL BUTTON GENERATOR
def button(initial_size, text, sml_pos, lg_pos, color, func,  *args):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    btn_sml = text_surface(initial_size, text, color)
    btn_lg = text_surface(initial_size+initial_size*0.3, text, color)
    btn_size = btn_sml.get_size()
    # Mouse Hover Pop Out Animation Adn Function
    if sml_pos[0] < mouse_x < sml_pos[0] + btn_size[0] \
            and sml_pos[1] < mouse_y < sml_pos[1] + btn_size[1]:
        screen.blit(btn_lg, (lg_pos[0], lg_pos[1]))
        # End the menu screen if user left click on PLAY
        if pygame.mouse.get_pressed(3)[0]:
            if args:
                func(args[0])
            else:
                func()
    else:
        screen.blit(btn_sml, (sml_pos[0], sml_pos[1]))


# MENU SCREEN
def menu_loop():
    # =============== MENU LOOP ================ #
    while True:
        save_and_exit()
        screen.fill((20, 20, 20))
        screen.blit(icon, (202, 80))
        screen.blit(contact, (0, 650))
        # MENU SCREEN OPTIONS
        button(120, 'PLAY', (200, 320), (170, 310), white, game_loop, "one_player")
        button(90, '2 PLAYER', (155, 420), (125, 410), white, game_loop, "two_player")
        button(70, 'HOW TO PLAY', (155, 502), (115, 490), white, how_to_play_loop)
        button(80, 'EXIT', (230, 570), (210, 560), white, sys.exit)

        pygame.display.update()


# HOW TO PLAY SCREEN
def how_to_play_loop():
    while True:
        save_and_exit()
        screen.fill((20, 20, 20))
        screen.blit(how_to_play_text, (0, 0))
        # Back Button
        button(60, 'back', (250, scn_height-80), (240, scn_height-90), white, menu_loop)
        pygame.display.update()


# GAME SCREEN
def game_loop(mode):
    global highscore, opp_score, player_score

    # Ball Speed And Starting Direction
    ball_speed = 5.5 if mode == "one_player" else 8
    random_direction_h = random.choice([1, -1])
    random_direction_v = random.choice([1, -1])
    ball_speed_vector = {'horizontal': ball_speed * random_direction_h,
                         'vertical': ball_speed * random_direction_v}

    # Player And Opponent Movement Speed
    player_speed = 10
    opp_speed = 4
    # Ball And Pads Position At Start
    x, y = 295, 420
    player_pos = scn_width / 2 - 50
    opp_pos = scn_width / 2 - 50

    # Position of interactive objects at the end of each loop
    player = pygame.draw.rect(screen, "green", pygame.Rect(player_pos, 740, 100, 15))
    opponent = pygame.draw.rect(screen, "red", pygame.Rect(opp_pos, 85, 100, 15))
    ball = pygame.draw.circle(screen, "white", (x, y), 10)

    # Reset scores at start
    opp_score = 0
    player_score = 0

    # Some variables to keep track of ball behaviour after collision
    wall_collide = False
    player_collide = True
    counter_for_ball_pause = -FPS * 2

    # =============== GAME LOOP ================ #
    while True:
        # Close Button Enabler
        save_and_exit()
        # Key Press Register
        keys = pygame.key.get_pressed()
        # Player Pad Movement Direction From Corresponding Key Pressed
        if keys[pygame.K_RIGHT] and player_pos < scn_width-100:
            player_pos += player_speed
        elif keys[pygame.K_LEFT] and player_pos > 0:
            player_pos -= player_speed

        # Background Color
        screen.fill(black)

        # Top Panel
        pygame.draw.rect(screen, 'white', pygame.Rect(0, 0, scn_width, 62))
        button(50, 'back', (20, 15), (10, 10), black, menu_loop)
        button(45, 'reset', (480, 15), (460, 13), black, reset_score)

        # Score Panel
        score_counter(player_score, 435)
        pygame.draw.rect(screen, white, pygame.Rect(523, 416, 50, 3))
        score_counter(opp_score, 335)

        # Ball Movement Logic
        if counter_for_ball_pause > FPS:
            x += ball_speed_vector['horizontal']
            y += ball_speed_vector['vertical']

        # Scoring Logic And Display Counter
        if y < 0:
            player_score += 1
            if mode == "one_player":
                ball_speed_vector['horizontal'] = ball_speed_vector['horizontal'] * 1.02
                ball_speed_vector['vertical'] = ball_speed_vector['vertical'] * 1.02
                opp_speed += opp_speed * 0.03
        elif y > 800:
            opp_score += 1

        # Winner Decider
        if opp_score > 9 and mode == "two_player":
            win_loop("red")
        elif player_score > 9 and mode == "two_player":
            win_loop("green")

        # Mode
        pygame.draw.rect(screen, white, pygame.Rect(0, scn_height - 20, 180, 20))
        if mode == "two_player":
            screen.blit(text_surface(30, "MODE: 2 PLAYER", black), (10, scn_height-20))
        elif mode == "one_player":
            screen.blit(text_surface(30, "MODE: 1 PLAYER", black), (10, scn_height-20))

        # Highscore Recorder
        if mode == "one_player":
            if player_score > highscore:
                highscore = player_score
            screen.blit(text_surface(60, 'highscore: '+str(highscore), black), (scn_width/2-140, 8))
        elif mode == "two_player":
            screen.blit(text_surface(45, "RED", "red"), (190, 17))
            screen.blit(text_surface(40, "vs", black), (260, 17))
            screen.blit(text_surface(45, "GREEN", "green"), (310, 17))
        # Reset Ball Position
        if y < 0 or y > scn_height:
            counter_for_ball_pause = 0
            x, y = 295, 395
            ball_speed_vector['horizontal'] *= random.randrange(-1, 2, 2)
            ball_speed_vector['vertical'] *= random.randrange(-1, 2, 2)
            player_collide = True

        # Ball Collision Detection With Walls
        if x > 600 or x < 0:
            ball_speed_vector['horizontal'] = -ball_speed_vector['horizontal']
            wall_collide = True

        # Position of interactive objects at the end of each loop
        player = pygame.draw.rect(screen, "green", pygame.Rect(player_pos, 740, 100, 15))
        opponent = pygame.draw.rect(screen, "red", pygame.Rect(opp_pos, 85, 100, 15))
        ball = pygame.draw.circle(screen, "white", (x, y), 10)

        # BALL COLLISION DETECTION
        # With Player's Pad
        if pygame.Rect.colliderect(ball, player) and wall_collide:
            ball_speed_vector['vertical'] = -ball_speed_vector['vertical']
            wall_collide = False
            player_collide = True
        # With Opponent's Pad
        elif pygame.Rect.colliderect(ball, opponent) and wall_collide:
            ball_speed_vector['vertical'] = -ball_speed_vector['vertical']
            wall_collide = False
            player_collide = False

        # Opponent Pad Movement Logic
        if mode == "one_player":
            if player_collide:
                if opp_pos < scn_width-100 and opp_pos+50 < x:
                    opp_pos += opp_speed
                elif opp_pos > 0:
                    opp_pos -= opp_speed
        elif mode == "two_player":
            if keys[pygame.K_d] and opp_pos < scn_width - 100:
                opp_pos += player_speed
            elif keys[pygame.K_a] and opp_pos > 0:
                opp_pos -= player_speed

        pygame.display.update()
        counter_for_ball_pause += 1
        clock.tick(FPS)


# Winner Screen
def win_loop(winner):
    while True:
        save_and_exit()
        screen.fill(black)
        # Message
        if winner == "red":
            screen.blit(text_surface(100, "RED WINS", white), (140, 300))
        elif winner == "green":
            screen.blit(text_surface(100, "GREEN WINS", white), (100, 300))

        # Buttons
        button(40, "Go to menu", (40, 500), (30, 495), white, menu_loop)
        button(40, "Play again", (400, 510), (380, 505), white, game_loop, "two_player")

        pygame.display.update()


menu_loop()


