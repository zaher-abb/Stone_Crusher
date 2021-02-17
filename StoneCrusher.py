import datetime
import os
import sys
import time
import random
import sqlite3

from typing import List, Tuple

import pygame

from Headset import Headset

init_start_time = time.time()

# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten.
if not pygame.font:
    print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer:
    print('Fehler pygame.mixer Modul konnte nicht geladen werden!')

pygame.init()

DEBUG_MODE = False

# RESOLUTION = (1080, 1920)
WINDOW_X = 600
WINDOW_Y = 900
RESOLUTION = (WINDOW_X, WINDOW_Y)
WINDOW = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Stone Crusher")
pygame.display.set_icon(pygame.image.load('assets/Design in Python/Spielfeld/images/icon.ico'))

EVENT_GUARD_EXPIRED = pygame.USEREVENT + 1
EVENT_BALLSPEED_EXPIRED = pygame.USEREVENT + 2
EVENT_BALLSIZE_EXPIRED = pygame.USEREVENT + 3
EVENT_RESET_BALL = pygame.USEREVENT + 4

# FLAG_IN_MAIN_MENU = 1
# FLAG_IN_SCOREBOARD = 2
# FLAG_IN_SETTINGS_MENU = 3

BLOCKS_X = 8
BLOCKS_Y = 8
BLOCKS_GAP = int(WINDOW_X / (BLOCKS_X + 1) / BLOCKS_X)  # space between neighboring blocks


def image_to_surf(dir: str, filename: str, x, y, square=False, has_alpha=False, flip_vertically=False) -> pygame.Surface:
    """
    Turns an image at the given path into a pygame.Surface that is scaled relative to the window dimensions.
    Scaling example: x=4, y=4 -> a Surface that occupies 1/16th of the window

    :param dir: Directory in which the image is located in a form os.path.join can work with
    :param filename: Name of the image to load
    :param x: Denominator to scale the horizontal dimension
    :param y: Denominator to scale the vertical dimension
    :param square: Whether the image should have a 1:1 aspect ratio
    :param has_alpha: Whether the image has transparency
    :param flip_vertically: Whether the image should be flipped vertically
    :return: A scaled pygame.Surface
    """

    if has_alpha:
        surf = pygame.image.load(os.path.join(dir, filename)).convert_alpha()
    else:
        surf = pygame.image.load(os.path.join(dir, filename)).convert()

    size_x = int(WINDOW_X / x)
    size_y = int(WINDOW_Y / y)
    if square:
        if flip_vertically:
            surf = pygame.transform.flip(surf, False, True)
        surf = pygame.transform.smoothscale(surf, (size_x, size_x))
    else:
        if flip_vertically:
            surf = pygame.transform.flip(surf, False, True)
        surf = pygame.transform.smoothscale(surf, (size_x, size_y))

    return surf


# Assets
path = 'assets/Design in Python/Hauptmenü/images'
MAIN_MENU_SURF = image_to_surf(path, 'mainMenu.png', 1, 1)
MENU_SETTINGS_SURF = image_to_surf(path, 'Setting_Page.png', 1, 1)
MENU_SCOREBOARD_SURF = image_to_surf(path, 'Scoreboard_Page 2.png', 1, 1)
BTN_SCOREBOARD_SURF = image_to_surf(path, 'Scoreboard_Button.png', 5, 20, has_alpha=True)
BTN_PLAY_SURF = image_to_surf(path, 'Play_Button.png', 5, 20, has_alpha=True)
BTN_SETTINGS_SURF = image_to_surf(path, 'Settings_Button.png', 5, 20, has_alpha=True)
BTN_UP_SURF = image_to_surf(path, 'arrow_up.png', 14, 20, has_alpha=True, square=True)
BTN_DOWN_SURF = image_to_surf(path, 'arrow_down.png', 14, 20, has_alpha=True, square=True)
BTN_MAIN_SURF = image_to_surf(path, 'main.png', 7, 26, has_alpha=True)
BTN_SAVE_SURF = image_to_surf(path, 'save_button.png', 7, 26, has_alpha=True)


path = 'assets/Design in Python/Spielfeld/images'
# PLAYFIELD = image_to_surf(path, 'playfield.png', 1, 1)  # Target, too little space
PLAYFIELD = image_to_surf(path, 'playfield_neu.png', 1, 1)  # Highscore
HEART = image_to_surf(path, 'heart.png', 1, 1, True)

path = 'assets/Stab'
PLATFORM = image_to_surf(path, 'Stab.png', 3, 30)

path = 'assets/Schutz_linie'
# GUARD_LINE = image_to_surf(path, 'Schutz_linie1.png', 1, 30, has_alpha=True)
GUARD_LINE = image_to_surf(path, 'Schutzlinie_neu44.png', 1, 40, has_alpha=True)

path = 'assets/Blöcke'
BLOCK_WHITE = image_to_surf(path, 'weiß.png',       BLOCKS_X + 1, 3 * BLOCKS_Y + 1)  # +1 so that when they are next to each other there can still be some space in between them
BLOCK_BLACK = image_to_surf(path, 'schwarz.png',    BLOCKS_X + 1, 3 * BLOCKS_Y + 1)
BLOCK_RED = image_to_surf(path, 'rot.png',          BLOCKS_X + 1, 3 * BLOCKS_Y + 1)
BLOCK_GREEN = image_to_surf(path, 'grün.png',       BLOCKS_X + 1, 3 * BLOCKS_Y + 1)
BLOCK_BLUE = image_to_surf(path, 'blau.png',        BLOCKS_X + 1, 3 * BLOCKS_Y + 1)
BLOCK_YELLOW = image_to_surf(path, 'gelb.png',      BLOCKS_X + 1, 3 * BLOCKS_Y + 1)
BLOCKS = (BLOCK_WHITE, BLOCK_BLACK, BLOCK_RED, BLOCK_GREEN, BLOCK_BLUE, BLOCK_YELLOW)
# KIND_BLOCK_MAP = {'white': BLOCK_WHITE, 'black': BLOCK_BLACK, 'red': BLOCK_RED, 'green': BLOCK_GREEN, 'blue': BLOCK_BLUE, 'yellow': BLOCK_YELLOW}

path = 'assets/Bälle/Bälle 1/groß'
BALL_BLACK = image_to_surf(path, 'Ball_schwarz_groß.png', 20, 100, True, True)
BALL_BLACK_BIGGER = image_to_surf(path, 'Ball_schwarz_groß.png', 20/2, 100/2, True, True)
BALL_BLUE = image_to_surf(path, 'Ball_blau_groß.png', 20, 100, True, True)
BALL_BLUE_BIGGER = image_to_surf(path, 'Ball_blau_groß.png', 20/2, 100/2, True, True)
BALL_GREEN = image_to_surf(path, 'Ball_grün_groß.png', 20, 100, True, True)
BALL_GREEN_BIGGER = image_to_surf(path, 'Ball_grün_groß.png', 20/2, 100/2, True, True)
ball_surf = BALL_BLACK  # just a default

# Assets - Sound
BLOCK_SOUNDS = [pygame.mixer.Sound(f'assets/Audio/laser{i + 1}.ogg') for i in range(len(BLOCKS))]
PLATFORM_SOUND = pygame.mixer.Sound('assets/Audio/tone1.ogg')
GUARD_ENGAGE_SOUND = pygame.mixer.Sound('assets/Audio/pepSound2.ogg')
GUARD_DISENGAGE_SOUND = pygame.mixer.Sound('assets/Audio/pepSound1.ogg')
LIFE_LOST_SOUND = pygame.mixer.Sound('assets/Audio/lowDown.ogg')

# Assets - Font
FONT = pygame.font.Font('assets/Schrift/zorque.ttf', 20)
FONT_BIGGER = pygame.font.Font('assets/Schrift/zorque.ttf', 30)


def change_ball_size(inflate: bool):
    if inflate:
        if ball.surf == BALL_BLACK:
            ball.surf = BALL_BLACK_BIGGER
        elif ball.surf == BALL_BLUE:
            ball.surf = BALL_BLUE_BIGGER
        elif ball.surf == BALL_GREEN:
            ball.surf = BALL_GREEN_BIGGER
    else:
        if ball.surf == BALL_BLACK_BIGGER:
            ball.surf = BALL_BLACK
        elif ball.surf == BALL_BLUE_BIGGER:
            ball.surf = BALL_BLUE
        elif ball.surf == BALL_GREEN_BIGGER:
            ball.surf = BALL_GREEN

    ball.rect = ball.surf.get_rect()


class Entity:
    def __init__(self, surf: pygame.Surface, pos: List[float] = None):
        self.surf = surf
        if pos:
            self.pos = pos
            self.rect = surf.get_rect().move(pos)
        else:
            self.pos = [float(surf.get_rect().x), float(surf.get_rect().y)]
            self.rect = surf.get_rect()

    def move(self, pos: List[float]):
        self.pos[0] += pos[0]
        self.pos[1] += pos[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        # if DEBUG_MODE and type(self) is Ball:
        #     print('Moved ball by ' + str(pos) + ' to ' + str(self.pos) + ', now the rect is here: ' + str(self.rect))


class Brick(Entity):
    def __init__(self, surf: pygame.Surface, index: List[int] = None, pos: List[float] = None):
        super().__init__(surf, pos)
        self.index = index

    def on_hit(self):
        if DEBUG_MODE:
            print('Brick ' + str(self.index) + ' got hit')

        # print(str(type(self.index[0])) + ' ' + str(self.index[0]) + '\n' + str(type(self.index[1])) + ' ' + str(self.index[1]))
        # Remove this block from the wall
        wall[self.index[0]][self.index[1]] = None
        global blocks_left, score, last_sound
        blocks_left -= 1
        score += 1

        if self.surf == BLOCK_WHITE:
            pass
        elif self.surf == BLOCK_BLACK:
            global ball_speed
            ball_speed *= 0.5
            pygame.time.set_timer(EVENT_BALLSPEED_EXPIRED, 10000, True)
        elif self.surf == BLOCK_RED:
            def call_on_hit_if_exists(i, j):
                if i >= 0 and j >= 0 and i < BLOCKS_X and j < BLOCKS_Y:
                    if wall[i][j]:
                        wall[i][j].on_hit()

            i, j = self.index[0], self.index[1]
            call_on_hit_if_exists(i-1, j-1)
            call_on_hit_if_exists(i-1, j)
            call_on_hit_if_exists(i-1, j+1)
            call_on_hit_if_exists(i,   j-1)
            call_on_hit_if_exists(i,   j+1)
            call_on_hit_if_exists(i+1, j-1)
            call_on_hit_if_exists(i+1, j)
            call_on_hit_if_exists(i+1, j-1)
        elif self.surf == BLOCK_GREEN:
            change_ball_size(True)
            global ball_bigger
            ball_bigger = True
            pygame.time.set_timer(EVENT_BALLSIZE_EXPIRED, 10000, True)
        elif self.surf == BLOCK_BLUE:
            global health
            health += 1
        elif self.surf == BLOCK_YELLOW:
            # Sounds should not overlap each other too bad
            if time.time() - last_sound > 0.1:
                GUARD_ENGAGE_SOUND.play()
                last_sound = time.time()
            global guard_active
            guard_active = True
            pygame.time.set_timer(EVENT_GUARD_EXPIRED, 10000, True)

        # Sounds should not overlap each other too bad
        if time.time() - last_sound > 0.1:
            BLOCK_SOUNDS[BLOCKS.index(self.surf)].play()
            last_sound = time.time()


class Ball(Entity):
    def __init__(self, surf: pygame.Surface, pos: List[float]):
        super().__init__(surf, pos)
        self.direction: pygame.Vector2
        self.set_direction(pygame.Vector2((-1.0, 1.0)[random.randint(0, 1)] * random.random(), -random.random()))

    def set_direction(self, v: pygame.Vector2):
        self.direction = v.normalize()
        if DEBUG_MODE:
            print("Ball's direction changed to: " + str(self.direction))
            print('Horizontality: ' + str(self.direction.x / self.direction.y))


def render_gamescreen():
    start_time = time.time()
    WINDOW.blit(PLAYFIELD, (0, 0))
    WINDOW.blit(ball.surf, ball.rect)
    WINDOW.blit(platform.surf, platform.rect)
    if guard_active:
        WINDOW.blit(GUARD.surf, GUARD.rect)

    if DEBUG_MODE:
        pygame.draw.rect(WINDOW, (255, 255, 255), ball.rect, 2)
        pygame.draw.rect(WINDOW, (255, 255, 255), platform.rect, 2)
        if guard_active:
            pygame.draw.rect(WINDOW, (255, 255, 255), GUARD.rect, 2)
    for i in range(len(wall)):
        for j in range(len(wall[i])):
            block = wall[i][j]
            if block:
                WINDOW.blit(block.surf, block.rect)
                if DEBUG_MODE:
                    pygame.draw.rect(WINDOW, (255, 255, 255), block.rect, 2)

    health_text = FONT_BIGGER.render(str(health), True, (255, 255, 255))
    WINDOW.blit(health_text, (WINDOW_X / 2 + 10, 15))
    score_text = FONT_BIGGER.render(str(score), True, (255, 255, 255))
    WINDOW.blit(score_text, (WINDOW_X * 0.185, 14))
    highscore_text = FONT_BIGGER.render(str(highscore), True, (255, 255, 255))
    WINDOW.blit(highscore_text, (WINDOW_X / 2 * 1.79, 14))

    pygame.display.flip()
    if DEBUG_MODE:
        print('Took ' + str(int((time.time() - start_time) * 1000000)).rjust(7) + ' μs to render')


def generate_wall() -> List[List[Brick]]:
    """
    Generates a new wall with the given width and height.

    :return: A new more or less randomly generated wall
    """

    wall = [[Brick(BLOCKS[random.randint(0, len(BLOCKS) - 1)]) for x in range(BLOCKS_Y)] for y in range(BLOCKS_X)]

    for i in range(len(wall)):
        for j in range(len(wall[i])):
            # The narrower the range, the less likely the Block type is.
            # Mind that likelyhoods of being chosen get smaller the the closer you get to whites naturally.
            if random.randint(0, 6) == 0:
                brick = Brick(BLOCK_YELLOW)
            elif random.randint(0, 5) == 0:
                brick = Brick(BLOCK_RED)
            elif random.randint(0, 7) == 0:
                brick = Brick(BLOCK_BLUE)
            elif random.randint(0, 4) == 0:
                brick = Brick(BLOCK_BLACK)
            elif random.randint(0, 3) == 0:
                brick = Brick(BLOCK_GREEN)
            else:
                brick = Brick(BLOCK_WHITE)

            brick.index = [i, j]
            # Each block is one block's width and height further from (0, 0) than it's predecessor ...
            pos = [i * brick.surf.get_width(), j * brick.surf.get_height()]
            # ... plus a gap in between them and from walls.
            pos[0] += (i + 1) * BLOCKS_GAP
            pos[1] += (j + 1) * BLOCKS_GAP
            # Lastly, shift block down to not interfere with the top UI
            pos[1] += 80
            brick.move(pos)

            wall[i][j] = brick

    return wall


def save_score():
    c = DB.cursor()
    # c.execute('CREATE TABLE scores (date text, score integer)')
    now = str(datetime.datetime.now().strftime("%Y-%m-%d  %H:%M"))
    c.execute("INSERT INTO scores VALUES (?,?)", (now, score))
    DB.commit()
    c.close()


def get_scores() -> List[Tuple[str, int]]:
    c = DB.cursor()
    c.execute('SELECT * FROM scores ORDER BY score desc')
    scores = c.fetchmany(5)
    c.close()
    return scores


# Buttons - Main Menu
BTN_SCOREBOARD = Entity(BTN_SCOREBOARD_SURF,    [WINDOW_X * 0.18, WINDOW_Y * 0.35])
BTN_PLAY = Entity(BTN_PLAY_SURF,                [WINDOW_X * 0.5 - BTN_PLAY_SURF.get_width() / 2, WINDOW_Y * 0.35])
BTN_SETTINGS = Entity(BTN_SETTINGS_SURF,        [WINDOW_X * 0.62, WINDOW_Y * 0.35])
selected_button_main_menu = BTN_PLAY
# Buttons - Score Board
BTN_SCOREBOARD_MAIN = Entity(BTN_MAIN_SURF, [WINDOW_X * 0.5 - BTN_MAIN_SURF.get_width() / 2, WINDOW_Y * 0.4])
# Buttons - Settings
BTN_BALL_GREEN = Entity(BALL_GREEN,     [WINDOW_X * 0.45, WINDOW_Y * 0.345])
BTN_BALL_BLUE = Entity(BALL_BLUE,       [WINDOW_X * 0.60, WINDOW_Y * 0.345])
BTN_BALL_BLACK = Entity(BALL_BLACK,     [WINDOW_X * 0.75, WINDOW_Y * 0.345])
BTN_BALL_UP = Entity(BTN_UP_SURF,       [WINDOW_X * 0.44, WINDOW_Y * 0.274])
BTN_BALL_DOWN = Entity(BTN_DOWN_SURF,   [WINDOW_X * 0.59, WINDOW_Y * 0.274])
BTN_BALL_SAVE = Entity(BTN_SAVE_SURF,   [WINDOW_X * 0.5 - BTN_SAVE_SURF.get_width() / 2, WINDOW_Y * 0.394])
selected_button_settings_menu = BTN_BALL_SAVE

wall = generate_wall()
platform = Entity(PLATFORM, [WINDOW_X / 2 - PLATFORM.get_width() / 2, WINDOW_Y - 100])
ball = Ball(ball_surf,      [WINDOW_X / 2 - BALL_BLACK.get_width() / 2, WINDOW_Y - 200])
GUARD = Entity(GUARD_LINE, [0, WINDOW_Y - 50])
PLATFORM_SPEED_MAX = WINDOW_X / 80  # Speed of the platform when controlled via keyboard
ball_speed_default = WINDOW_X / 250  # Normal speed of the ball, may be changed via settings
BALL_SPEED_SLOWER = ball_speed_default / 2  # Slower speed of the ball
BALL_SPEED_FASTER = ball_speed_default * 2  # Faster speed of the ball
ball_speed = ball_speed_default
ball_speed_multi = 1.0
guard_active = False
ball_bigger = False
blocks_left = BLOCKS_X * BLOCKS_Y
last_sound = time.time()

running = True
in_menu = MAIN_MENU_SURF
DB = sqlite3.connect('scores.db')
clock = pygame.time.Clock()
health = 1
score = 0
highscore = int(get_scores()[0][1])
command_left_power, command_right_power = 0, 0
last_command_fetch = time.time()
t = time.time()
last_push, last_shift_left, last_shift_right = t, t, t
del t
pushing, shifting_left, shifting_right = False, False, False

headset = Headset()

print('Initialisation took ' + str(int((time.time() - init_start_time) * 1000)) + ' ms')


def simulate_game(events: List[pygame.event.Event]) -> bool:
    global running, guard_active, ball_bigger, ball, ball_speed, ball_speed_multi, wall, health, score, blocks_left

    for e in events:
        if e.type == EVENT_GUARD_EXPIRED:
            GUARD_DISENGAGE_SOUND.play()
            guard_active = False
        elif e.type == EVENT_BALLSPEED_EXPIRED:
            ball_speed = ball_speed_default
            if DEBUG_MODE:
                print('New ball speed: ' + str(ball_speed), ' multi: ' + str(ball_speed_multi))
        elif e.type == EVENT_BALLSIZE_EXPIRED:
            ball_bigger = False
            change_ball_size(False)
        elif e.type == EVENT_RESET_BALL:
            ball = Ball(ball_surf, [WINDOW_X / 2 - BALL_BLACK.get_width() / 2, WINDOW_Y - 200])

    keys = pygame.key.get_pressed()
    # Movement requests are only accepted when the platform still can move in that direction
    if keys[pygame.K_LEFT] and platform.pos[0] >= 0:
        platform.move([-PLATFORM_SPEED_MAX, 0])
    if keys[pygame.K_RIGHT] and platform.pos[0] <= WINDOW_X - PLATFORM.get_width():
        platform.move([PLATFORM_SPEED_MAX, 0])

    if platform.pos[0] >= 0:
        platform.move([-PLATFORM_SPEED_MAX * command_left_power, 0])
    if platform.pos[0] < WINDOW_X - PLATFORM.get_width():
        platform.move([PLATFORM_SPEED_MAX * command_right_power, 0])

    ball.move([ball.direction.x * ball_speed * ball_speed_multi, ball.direction.y * ball_speed * ball_speed_multi])

    ball_topline = (ball.rect.topleft, ball.rect.topright)
    ball_bottomline = (ball.rect.bottomleft, ball.rect.bottomright)
    ball_left = ball.rect.midleft
    ball_right = ball.rect.midright

    # Handle collisions with blocks
    for i in range(len(wall)):
        for j in range(len(wall[i])):
            block = wall[i][j]
            if not block:
                continue
            # Let the ball move to the right,
            if block.rect.collidepoint(ball_left):
                if ball.direction.x < 0:
                    ball.direction.x *= -1
                block.on_hit()
            # Let the ball move to the left,
            elif block.rect.collidepoint(ball_right):
                if ball.direction.x > 0:
                    ball.direction.x *= -1
                block.on_hit()
            # Let the ball move down,
            elif block.rect.clipline(ball_topline):
                if ball.direction.y < 0:
                    ball.direction.y *= -1
                block.on_hit()
            # Let the ball move up,
            elif block.rect.clipline(ball_bottomline):
                if ball.direction.y > 0:
                    ball.direction.y *= -1
                block.on_hit()

    # Handle collisions with walls and guard
    # Let the ball move to the right,
    if ball_left[0] <= 0:
        if ball.direction.x < 0:
            ball.direction.x *= -1
    # Let the ball move to the left,
    elif ball_right[0] >= WINDOW_X:
        if ball.direction.x > 0:
            ball.direction.x *= -1
    # Let the ball move down,
    elif ball.rect.top <= 80:
        if ball.direction.y < 0:
            ball.direction.y *= -1
    # Let the ball move up,
    elif guard_active and GUARD.rect.clipline(ball_bottomline):
        if ball.direction.y > 0:
            ball.direction.y *= -1
        PLATFORM_SOUND.play()

    # Handle collisions with the platform
    # Let the ball move to the right,
    if platform.rect.collidepoint(ball_left):
        if ball.direction.x < 0:
            ball.direction.x *= -1
        PLATFORM_SOUND.play()
    # Let the ball move to the left,
    elif platform.rect.collidepoint(ball_right):
        if ball.direction.x > 0:
            ball.direction.x *= -1
        PLATFORM_SOUND.play()
    # Let the ball move down,
    elif platform.rect.clipline(ball_topline):
        if ball.direction.y < 0:
            ball.direction.y *= -1
        PLATFORM_SOUND.play()
    # Let the ball move up,
    elif platform.rect.clipline(ball_bottomline):
        if ball.direction.y > 0:
            ball.direction.y *= -1
        PLATFORM_SOUND.play()
        ball_speed_multi += 0.03
        if DEBUG_MODE:
            print('New ball speed: ' + str(ball_speed), ' multi: ' + str(ball_speed_multi))
        ball.move([0, (platform.rect.top - ball.rect.bottom) - 1])
        # Calculate how far away the ball is from the platform's middle
        deflection_strength = (ball.rect.centerx - platform.rect.centerx) / 80
        # When the exit angle is too small, the ball bounces between the walls for a long time, which is boring
        v = pygame.Vector2(ball.direction.x + deflection_strength, ball.direction.y).normalize()
        if v.y > -0.3:
            v.y = -0.3
            v.normalize()
        ball.set_direction(v)

    # If ball fell out of window
    if ball.pos[1] > WINDOW_Y:
        if not pygame.mixer.get_busy():
            LIFE_LOST_SOUND.play()
        health -= 1
        pygame.time.set_timer(EVENT_RESET_BALL, 2000, True)
        ball = Ball(ball_surf, [WINDOW_X / 2 - BALL_BLACK.get_width() / 2, WINDOW_Y - 200])
        ball.direction = pygame.Vector2(0, 0)

    if blocks_left == 0:
        score += 10
        ball = Ball(ball.surf, [WINDOW_X / 2 - BALL_BLACK.get_width() / 2, WINDOW_Y - 200])
        wall = generate_wall()
        blocks_left = BLOCKS_X * BLOCKS_Y

    render_gamescreen()

    if health < 1:
        return True
    return False


def on_button_press_in_main_menu():
    global in_menu
    if selected_button_main_menu == BTN_PLAY:
        in_menu = None
    elif selected_button_main_menu == BTN_SCOREBOARD:
        in_menu = MENU_SCOREBOARD_SURF
    elif selected_button_main_menu == BTN_SETTINGS:
        in_menu = MENU_SETTINGS_SURF


def on_button_press_in_settings():
    global ball_speed_default, ball_speed, in_menu
    if selected_button_settings_menu == BTN_BALL_UP:
        ball_speed_default += 0.5
        ball_speed = ball_speed_default
    elif selected_button_settings_menu == BTN_BALL_DOWN:
        ball_speed_default -= 0.5
        ball_speed = ball_speed_default
    elif selected_button_settings_menu == BTN_BALL_BLACK:
        ball.surf = BALL_BLACK
    elif selected_button_settings_menu == BTN_BALL_BLUE:
        ball.surf = BALL_BLUE
    elif selected_button_settings_menu == BTN_BALL_GREEN:
        ball.surf = BALL_GREEN
    elif selected_button_settings_menu == BTN_BALL_SAVE:
        in_menu = MAIN_MENU_SURF


def on_shift_in_main_menu(direction: str):
    global selected_button_main_menu
    if direction == 'right':
        if selected_button_main_menu == BTN_SCOREBOARD:
            selected_button_main_menu = BTN_PLAY
        elif selected_button_main_menu == BTN_PLAY:
            selected_button_main_menu = BTN_SETTINGS
    elif direction == 'left':
        if selected_button_main_menu == BTN_SETTINGS:
            selected_button_main_menu = BTN_PLAY
        elif selected_button_main_menu == BTN_PLAY:
            selected_button_main_menu = BTN_SCOREBOARD


def on_shift_in_settings_menu(direction: str):
    global selected_button_settings_menu
    if direction == 'right':
        if selected_button_settings_menu == BTN_BALL_UP:
            selected_button_settings_menu = BTN_BALL_DOWN
        elif selected_button_settings_menu == BTN_BALL_DOWN:
            selected_button_settings_menu = BTN_BALL_GREEN
        elif selected_button_settings_menu == BTN_BALL_GREEN:
            selected_button_settings_menu = BTN_BALL_BLUE
        elif selected_button_settings_menu == BTN_BALL_BLUE:
            selected_button_settings_menu = BTN_BALL_BLACK
        elif selected_button_settings_menu == BTN_BALL_BLACK:
            selected_button_settings_menu = BTN_BALL_SAVE
    elif direction == 'left':
        if selected_button_settings_menu == BTN_BALL_GREEN:
            selected_button_settings_menu = BTN_BALL_DOWN
        elif selected_button_settings_menu == BTN_BALL_DOWN:
            selected_button_settings_menu = BTN_BALL_UP
        elif selected_button_settings_menu == BTN_BALL_BLACK:
            selected_button_settings_menu = BTN_BALL_BLUE
        elif selected_button_settings_menu == BTN_BALL_BLUE:
            selected_button_settings_menu = BTN_BALL_GREEN
        elif selected_button_settings_menu == BTN_BALL_SAVE:
            selected_button_settings_menu = BTN_BALL_BLACK


if __name__ == '__main__':
    while running:
        clock.tick(60)
        logic_start_time = time.time()
        pushing, shifting_left, shifting_right = False, False, False

        # Get new command data from headset, if present
        # Due to the 8 Hz polling rate of the headset, processing time of get_data in Cortex client spikes to 120ms when spammed
        # For some reason, commands fetched via receive_data() are queued. So you have to fetch them at least 8 times a
        # second or they will pile up resulting in out of date commands
        if headset.is_present and time.time() - last_command_fetch > 1/9:
            # left, right, push = headset.get_commands("stream")
            left, right, push = headset.get_commands("receive")
            command_left_power  = left
            command_right_power = right
            if time.time() - last_shift_left  > 1 and left > 0.6:   # TODO: tweak sensitivity
                shifting_left = True
                last_shift_left = time.time()
                print('left shift registered at ' + time.strftime("%H:%M:%S"))
            if time.time() - last_shift_right > 1 and right > 0.6:  # TODO: tweak sensitivity
                shifting_right = True
                last_shift_right = time.time()
                print('right shift registered at ' + time.strftime("%H:%M:%S"))
            if time.time() - last_push        > 1 and push > 0.6:   # TODO: tweak sensitivity
                pushing = True
                last_push = time.time()
                print('push registered at ' + time.strftime("%H:%M:%S"))
            last_command_fetch = time.time()
            # print('Command fetched at ' + str(last_command_fetch))

        # Handle ESC inputs
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                if in_menu == MAIN_MENU_SURF:
                    running = False
                else:
                    in_menu = MAIN_MENU_SURF
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Menues part of loop
        if in_menu:
            WINDOW.blit(in_menu, (0, 0))
            if in_menu == MAIN_MENU_SURF:
                WINDOW.blit(BTN_SCOREBOARD.surf, BTN_SCOREBOARD.pos)
                WINDOW.blit(BTN_PLAY.surf, BTN_PLAY.pos)
                WINDOW.blit(BTN_SETTINGS.surf, BTN_SETTINGS.pos)
                if DEBUG_MODE:
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_SCOREBOARD.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_PLAY.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_SETTINGS.rect, 3)
                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RIGHT:
                            on_shift_in_main_menu('right')
                        elif e.key == pygame.K_LEFT:
                            on_shift_in_main_menu('left')
                        elif e.key == pygame.K_RETURN:
                            on_button_press_in_main_menu()
                if shifting_left:
                    on_shift_in_main_menu('left')
                if shifting_right:
                    on_shift_in_main_menu('right')
                if pushing:
                    on_button_press_in_main_menu()

                pygame.draw.rect(WINDOW, (255, 0, 0), selected_button_main_menu.rect, 3)

            elif in_menu == MENU_SCOREBOARD_SURF:
                scores = get_scores()
                i = 0
                for s in scores:
                    date_text = FONT.render(str(s[0]), True, (0, 0, 0))
                    score_text = FONT.render(str(s[1]), True, (0, 0, 0))
                    WINDOW.blit(date_text, (WINDOW_X * 0.29, WINDOW_Y * 0.264 + i * date_text.get_height()))
                    WINDOW.blit(score_text, (WINDOW_X * 0.67, WINDOW_Y * 0.264 + i * date_text.get_height()))
                    i += 1
                WINDOW.blit(BTN_SCOREBOARD_MAIN.surf, BTN_SCOREBOARD_MAIN.pos)
                pygame.draw.rect(WINDOW, (255, 0, 0), BTN_SCOREBOARD_MAIN.rect, 3)
                for e in events:
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                        in_menu = MAIN_MENU_SURF
                if pushing:
                    in_menu = MAIN_MENU_SURF

            elif in_menu == MENU_SETTINGS_SURF:
                WINDOW.blit(BTN_BALL_BLACK.surf, BTN_BALL_BLACK.rect)
                WINDOW.blit(BTN_BALL_BLUE.surf, BTN_BALL_BLUE.rect)
                WINDOW.blit(BTN_BALL_GREEN.surf, BTN_BALL_GREEN.rect)
                WINDOW.blit(BTN_BALL_UP.surf, BTN_BALL_UP.rect)
                WINDOW.blit(BTN_BALL_DOWN.surf, BTN_BALL_DOWN.rect)
                WINDOW.blit(BTN_BALL_SAVE.surf, BTN_BALL_SAVE.rect)

                # Highlight ball that is currently selected
                if ball.surf == BALL_GREEN or ball.surf == BALL_GREEN_BIGGER:
                    pygame.draw.rect(WINDOW, (0, 255, 0), BTN_BALL_GREEN.rect.inflate(6, 6), 4)
                elif ball.surf == BALL_BLUE or ball.surf == BALL_BLUE_BIGGER:
                    pygame.draw.rect(WINDOW, (0, 255, 0), BTN_BALL_BLUE.rect.inflate(6, 6), 4)
                elif ball.surf == BALL_BLACK or ball.surf == BALL_BLACK_BIGGER:
                    pygame.draw.rect(WINDOW, (0, 255, 0), BTN_BALL_BLACK.rect.inflate(6, 6), 4)

                for e in events:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RIGHT:
                            on_shift_in_settings_menu('right')
                        elif e.key == pygame.K_LEFT:
                            on_shift_in_settings_menu('left')
                        elif e.key == pygame.K_RETURN:
                            on_button_press_in_settings()
                if shifting_right:
                    on_shift_in_settings_menu('right')
                if shifting_left:
                    on_shift_in_settings_menu('left')
                if pushing:
                    on_button_press_in_settings()

                speed_text = FONT.render(str(ball_speed_default)[0:3], True, (0, 0, 0))
                WINDOW.blit(speed_text, (WINDOW_X * 0.522, WINDOW_Y * 0.282))

                pygame.draw.rect(WINDOW, (255, 0, 0), selected_button_settings_menu.rect, 3)

                if DEBUG_MODE:
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_BALL_BLACK.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_BALL_GREEN.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_BALL_BLUE.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_BALL_SAVE.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_BALL_UP.rect, 3)
                    pygame.draw.rect(WINDOW, (255, 255, 255), BTN_BALL_DOWN.rect, 3)

            pygame.display.flip()

        # Gameplay part of loop
        if not in_menu:
            game_over = simulate_game(events)
            if game_over:
                in_menu = MENU_SCOREBOARD_SURF

                save_score()
                highscore = int(get_scores()[0][1])

                # Reset game session
                wall = generate_wall()
                platform = Entity(PLATFORM, [WINDOW_X / 2 - PLATFORM.get_width() / 2, WINDOW_Y - 100])
                ball = Ball(ball_surf, [WINDOW_X / 2 - BALL_BLACK.get_width() / 2, WINDOW_Y - 200])
                ball_speed = ball_speed_default
                ball_speed_multi = 1.0
                guard_active = False
                health = 1
                score = 0
                blocks_left = BLOCKS_X * BLOCKS_Y

        if DEBUG_MODE:
            print('Took ' + str(int((time.time() - logic_start_time) * 1000000)).rjust(7) + ' μs for logic')

    pygame.quit()
    sys.exit()
