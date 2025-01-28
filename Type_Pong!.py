#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11/26/2024

@author: feysy
"""

import dae_progfa_lib as pfe
from dae_progfa_lib import ShapeMode
from dae_progfa_lib import MouseButton
import random
import math
from math import sqrt
import webbrowser

# Create an instance of ProgfaEngine and set window size (width, height):
engine = pfe.ProgfaEngine(800, 600)

# Set the frame rate to x frames per second:
engine.set_fps(60)

# assign variables:

debug = False
key = None
button, button_counter = None, 0
last_game_state = 0
game_state = 0
# 0 = intro
# 1 = main menuµ
# 2 = credits
# 3 = quit
# 4 = practice
# 5 = easy
# 6 = hard
# 7 = pause
counter = 0
stars_x = []
stars_y = []
r, g, b, red, green, blue = 1, 0, 0, False, False, False

HP, word1, word2, left, right, progress, lockedword, what_word = 0, "amogus", "amogus", False, False, 0, 0, ""
ballx, bally, playerx, playery, botx, boty, xspeed, ballspeed, balldir, multiplier, points, highscore, stat1, stat2 =0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [0, 0, 0], 0, 0
pallet, table, net, menu_counter, escape_counter, alarm, size = 1, "", "", 0, 0, False, 0
word_levels = {
    "practice": ["cat", "dog", "rats", "hat", "bird", "fan", "just", "nice", "guy", "red", "bruh", "purple", "win", "real", "weird", "fake", "man", "best", "box", "blue"],
    "easy": ["welcome", "bread", "bank", "dance", "floor", "amogus", "drip", "light", "mouse", "piano", "river", "smile", "bring", "table", "train", "water", "zebra", "cloud", "plant", "stone"],
    "hard": ["abstract", "dictionary", "cabinet", "daylight", "electric", "firework", "magenta", "horizon", "jigsaw", "kingdom", "language", "insane", "quandale", "dingle", "general", "question", "treasure", "great", "volcano", "whisper"]}
list_pallets = []
menu_counter_list = [0, 3, 6, 9, 12, 13, 14, 11, 8, 5, 2, 1]


def setup():
    global pallet, list_pallets, table, net
    generate_stars()
    engine.outline_color = None
    engine.set_font('Resources/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf')

    table = engine.load_image(f"Resources/sprites/table/table.png")
    net = engine.load_image(f"Resources/sprites/table/net.png")
    for i in range(1, 16):
        pallets = engine.load_image(f"Resources/sprites/pallet/{(i - 1) // 3 + 1}{(i - 1) % 3 + 1}.png")
        list_pallets.append(pallets)


def generate_stars():
    for i in range(0, 100):
        x = random.randint(0, engine.width)
        y = random.randint(0, engine.height)
        stars_x.append(x)
        stars_y.append(y)

def draw_menu_background(speed: int | float = 3):
    global r, g, b, red, green, blue
    engine.background_color, engine.shape_mode, engine.color = ((0.2, 0.0, 0.1)), ShapeMode.CENTER, (r, g, b)

    for i in range(0, len(stars_x)):
        engine.draw_circle(stars_x[i], stars_y[i], 5)
        # engine.draw_circle(engine.width - stars_x[i], stars_y[i], 5)
    red, green, blue = True if b == 1 else False if b == 0 else red, True if r == 1 else False if r == 0 else green, True if g == 1 else False if g == 0 else blue
    r, b = round(r + 0.01, 2) if red == True else r, round(b - 0.01, 2) if red == True else b
    g, r = round(g + 0.01, 2) if green == True else g, round(r - 0.01, 2) if green == True else r
    b, g = round(b + 0.01, 2) if blue == True else b, round(g - 0.01, 2) if blue == True else g

    global counter
    counter += 0.1 if counter <= 3.9 else -4
    for i in range(0, len(stars_x)):
        if stars_y[i] > engine.height / 2 - engine.height / 10:
            stars_x[i] = stars_x[i] - speed * (1 + 2 * (stars_y[i] - (engine.height / 2 - engine.height / 10)) / (engine.height / 2 + engine.height / 10)) if stars_x[i] >= 0 and stars_x[i] <= engine.width else 0 if stars_x[i] > engine.width else engine.width
        else:
            stars_x[i] = stars_x[i] - speed * (1.3 - stars_y[i] / (2 * (engine.height * 1.5))) if stars_x[i] >= 0 and stars_x[i] <= engine.width else 0 if stars_x[i] > engine.width else engine.width


def draw_text(text, x: int | float, y: int | float, color: tuple = (1, 1, 1), size: int | float = 20, centered: bool = False):
    engine.set_font_size(size)
    hover = False
    if centered:
        x = x - (len(str(text)) * (size / 1.7)) / 2
    if x < engine.mouse_x < x + len(str(text)) * (size / 1.7) and y - size / 2 < engine.mouse_y < y + size / 1.8:
        engine.color = (color[0] / 2, color[1] / 2, color [2] / 2)
        hover = True
    else:
        engine.color = color
    engine.draw_text(str(text), x, y - size / 1.48)
    return hover

def draw_word(word, x: int | float, y: int | float, centered: bool = True, progress: int = 0, color: tuple = (1, 1, 1), size: int | float = 20):
    engine.set_font_size(size)
    xpos, ypos, engine.color = x - len(str(word)) / 2 * (size / 1.7) if centered else x, y - size / 1.48 if centered else y, color
    if progress != 0:
        engine.draw_text(str(word[progress:]), xpos + progress * (size / 1.7), ypos)
        engine.color = (color[0] / 2, color[1] / 2, color[2] / 2)
        engine.draw_text(str(word[:progress]), xpos, ypos)
    else:
        engine.draw_text(word, xpos + progress * (size / 1.7), ypos)


def draw_menu(*buttons, animation: int = 0, centered: bool = False):
    max, hover = len(buttons), False
    global button, menu_counter
    engine.shape_mode, engine.color = ShapeMode.CENTER, (0.9, 0.9, 0.5)
    engine.draw_rectangle(engine.width / 2, engine.height / 2, engine.width * 5 / 8, engine.height / 30 + engine.height / 8.57 * max)
    for i in range(0, max):
        engine.shape_mode, engine.color = ShapeMode.CENTER, (0.8, 0.8, 0.45)
        y = ((engine.height / 2 - (engine.height / 8.57) * (max - 1) / 2) if max % 2 == 1 and max != 1 else (engine.height / 2 if max == 1 else(engine.height / 2 - (engine.height / 17.14 * max - engine.height / 17.14)))) + i * engine.height / 8.57
        engine.draw_rectangle(engine.width / 2 - engine.width / 9 if not centered else engine.width / 2, y, engine.width / 3 if not centered else engine.width / 1.8, engine.height / 16)
        if draw_text(buttons[i], engine.width / 2 - engine.width / 4 if not centered else engine.width / 2, y, centered=centered, color=(1, 1, 0.9)):
            hover = i + 1

    if animation > 0:
        list_pallets[menu_counter_list[math.floor(menu_counter)]].draw_fixed_size(engine.width / 2 + engine.width * 0.184, engine.height / 2, 200, 200)
        menu_counter = menu_counter + 0.4 if animation == 1 and menu_counter < len(menu_counter_list) - 0.4 else 0 if animation == 1 else menu_counter
        menu_counter = menu_counter - 0.25 if animation == 2 and menu_counter > 0.25 else 11 if animation == 2 else menu_counter

    return hover if hover != False else if_pass()


def draw_intro():
    draw_menu_background(7)
    hover = draw_menu("main menu", "info + credits", "end game", animation = 1)
    draw_word("Type Pong!", engine.width / 2, engine.height / 7, color=(0.8, 0.8, 0.45), size=70, centered=True)

    if button == "LEFT":
        if hover == 1 or hover == 2:
            return hover
        elif hover == 3:
            print(f"{0/0} equals {1}!")
    return 0


def draw_main_menu():
    draw_menu_background()
    hover = draw_menu("intro", "practice mode", "easy mode", "hard mode", "pallet mode", animation = 2)
    draw_word("select difficulty", engine.width / 2, engine.height / 10, color=(0.8, 0.8, 0.45), size=50, centered=True)
    if button == "LEFT":
        if hover == 5:
            return -1
        return 0 if hover == 1 else hover + 2 if hover != None else 1
    return 1


def draw_credits():
    draw_menu_background(-1)
    hover = draw_menu("intro", "game rules", "made by yorifant", centered=True)
    if button == "LEFT":
        if hover == 1:
            return 0
        if hover == 2:
            return 3
        if hover == 3:
            webbrowser.open('https://www.linkedin.com/in/yoran-feys-98b6241a1/')
    return 2


def draw_rules():
    draw_menu_background(-3)
    hover = draw_menu("return", "type first letter to go left / right", "finishing last second gives x2 points", "the game constantly speeds up", "have fun!", centered=True)
    if button == "LEFT":
        if hover == 1:
            return 2
    return 3


def draw_pause(difficulty: int):
    global escape_counter, HP
    render_game(word1, word2, False)
    hover = draw_menu("resume", "restart", "end match", "main menu", animation=0, centered=True)
    if button == "LEFT":
        if hover == 1:
            return difficulty
        if hover == 2:
            HP = 0
            return difficulty
        if hover == 3:
            HP = 0
            return 8
        if hover == 4:
            return 1

    if str(engine.key).lower() == "escape" and escape_counter == 1:
        return 7
    escape_counter = 0

    if str(engine.key).lower() == "escape":
        return difficulty
    return 7


def draw_end(difficulty: int):
    draw_menu_background(2)
    difficulty_text = "practice mode" if difficulty == 4 else "easy mode" if difficulty == 5 else "hard mode"
    hover = draw_menu(f"highscore: {highscore[difficulty - 4]}", f"points: {points}", f"letters typed: {stat1}", f"words typed: {stat2}", "restart", "main menu", animation=0, centered=True)
    draw_word(f"statistics {difficulty_text}", engine.width /2, engine.height / 10 - engine.height / 15, color=(0.8, 0.8, 0.45), size=40, centered=True)
    if button == "LEFT":
        if hover == 5:
            return difficulty
        if hover == 6:
            return 1
    return 8


def render_game(word1: str, word2: str, show_words: bool = True):
    global botx
    draw_menu_background(2) if last_game_state == 4 else if_pass()
    draw_menu_background(3) if last_game_state == 5 else if_pass()
    draw_menu_background(4) if last_game_state == 6 else if_pass()

    if debug:
        list = (left, right, playerx, playery, ballx, bally, xspeed, ballspeed, balldir, lockedword, points, playerx, ballx, HP, progress, word1, word2)
        strlist = ("left", "right", "playerx", "playery", "ballx", "bally", "xspeed", "ballspeed", "balldir", "lockedword", "points", "playerx", "ballx", "HP", "progess", "word1", "word2")
        for i in range(0, len(list)):
            draw_word(f"{strlist[i]}: {list[i]}", 20, 20 + i * 20, False, 0, (0.7, 0.7, 0.7,), 10)

    engine.outline_color = None
    if debug:
        engine.outline_color = (0.9, 0.2, 0.2)
        engine.draw_line(engine.width / 2 - 100, engine.height * 4 / 5 - 360, engine.width / 2 - 250, engine.height * 4 / 5, 3)
        engine.draw_line(engine.width / 2 + 100, engine.height * 4 / 5 - 360, engine.width / 2 + 250, engine.height * 4 / 5, 3)
        engine.outline_color = None



    table.draw_fixed_size(engine.width / 2, engine.height / 2 + 100, 400 * 1.25, 530, False)

    size = 1
    botx = botx + (ballx + balldir * ((360 - bally) / ballspeed) - botx) / ((360 - bally) / ballspeed) if ballspeed > 0 and bally != 360 else botx
    pallet = 3 * min((max(-100, min(100, int(botx))) + 100) // 40, 4) + 2
    if ballspeed < 0 and bally <= 360 + 2 * ballspeed and pallet % 3 == 2:
        pallet -= 1
        size += ((360 - bally) // ballspeed) * 0.05
    if ballspeed < 0 and bally <= 360 + 4 * ballspeed and pallet % 3 == 1:
        pallet -= 1
        size += ((360 - bally) // ballspeed) * 0.05
    if ballspeed < 0 and bally <= 360 + 10 * ballspeed and pallet % 3 == 0:
        pallet += 1
        size = -1
        size -= ((360 - bally) // ballspeed) * 0.095
    if ballspeed < 0 and bally <= 360 + 20 * ballspeed and pallet % 3 == 1:
        pallet += 1
        size = 1
    list_pallets[int(pallet)].draw_fixed_size(engine.width / 2 + botx * 4/5, engine.height * 4 / 5 -390 + (15 * (1-size)), 100 + 10 * (1-size), 100 + 10 * (1-size))

    height = 0.4
    if ballspeed > 0:
        if (bally / 360) < 0.8:
            height = -4.9 * (((bally / 360)-0.35) * ((bally / 360)-0.35)) + 1
        else:
            height = -(4.9 / 1.75) * (((bally / 360) - 0.35 - 0.9) * ((bally / 360) - 0.35 - 0.9)) + 1 - 0.425
    if ballspeed < 0:
        if (bally / 360) > 0.2:
            height = -4.9 * ((((360 - bally) / 360) - 0.35) * (((360 - bally) / 360) - 0.35)) + 1
        else:
            height = -(4.9 / 1.75) * ((((360 - bally) / 360) - 0.35 - 0.9) * (((360 - bally) / 360) - 0.35 - 0.9)) + 1 - 0.425

    engine.color = (0.1, 0.1, 0.3, 0.25)
    engine.draw_ellipse(engine.width / 2 + ballx / (bally / 300 + 1) * 2.2, engine.height * 4 / 5.2 - bally / (bally / 360 + 1) * 1.75, (35 / (bally / 360 + 1)) / (1 + height / 2), (35 / (bally / 360 + 1) / 1.8) / (1 + height / 2))
    engine.draw_ellipse(engine.width / 2 + ballx / (bally / 300 + 1) * 2.2, engine.height * 4 / 5.2 - bally / (bally / 360 + 1) * 1.75, (28 / (bally / 360 + 1)) / (1 + height / 2), (28 / (bally / 360 + 1) / 1.8) / (1 + height / 2))

    net.draw_fixed_size(engine.width / 2, engine.height / 2 - 70, 330, 50, False)

    engine.color = (0.9, 0.2, 0.2)
    engine.draw_circle(engine.width / 2 + ballx / (bally / 300 + 1) * 2.2, engine.height * 4 / 5.2 - (bally + 100 * height + (7.5 / (bally / 360 + 1))) / ( bally / 360 + 1) * 1.75, 30 / (bally / 360 + 1) + 2 * height / (bally / 360 + 1))

    size = 1
    pallet = 3 * min((max(-100, min(100, playerx)) + 100) // 40, 4)
    if ballspeed > 0 and bally >= 0 and pallet % 3 == 0:
        pallet += 1
        size -= (bally // ballspeed) * 0.125
    if ballspeed > 0 and bally >= 2 * ballspeed and pallet % 3 == 1:
        pallet += 1
    if ballspeed > 0 and bally >= 8 * ballspeed and pallet % 3 == 2:
        pallet -= 1
        size = -0.7
        size += (bally // ballspeed) * 0.095
    if ballspeed > 0 and bally >= 18 * ballspeed and pallet % 3 == 1:
        pallet -= 1
        size = 1
    list_pallets[int(pallet)].draw_fixed_size(engine.width / 2 + playerx * 1.7 * 1.25, engine.height * 4/5 - 70 - (50 * (1-size)), 200 - 40 * (1-size), 200 - 40 * (1-size))

    if debug:
        engine.outline_color = (0.9, 0.2, 0.2)
        engine.draw_line(engine.width / 2 + (ballx * 0.85 - engine.width / 32) * (-1/240 * bally + 2.5), engine.height * 4 / 5 - (bally + 15) / (bally / 360 + 1) * 2, engine.width / 2 + (ballx * 0.85 - engine.width / 32) * (-1/240 * bally + 2.5), engine.height * 4 / 5 - (bally - 15) / (bally / 360 + 1) * 2, 2)
        engine.draw_line(engine.width / 2 + (ballx * 0.85 + engine.width / 32) * (-1/240 * bally + 2.5), engine.height * 4 / 5 - (bally + 15) / (bally / 360 + 1) * 2, engine.width / 2 + (ballx * 0.85 + engine.width / 32) * (-1/240 * bally + 2.5), engine.height * 4 / 5 - (bally - 15) / (bally / 360 + 1) * 2, 2)
        engine.draw_circle(engine.width / 2 + playerx * 2.5, engine.height * 4 / 5, 5)
        engine.outline_color = None

        pass

    draw_word(f"HP: {HP}", engine.width * 1/3, engine.height / 10 - engine.height / 15, color=(0.8, 0.8, 0.45), size=30, centered=True)
    draw_word(f"Points: {points}", engine.width * 2/3 + engine.width / 40, engine.height / 10 - engine.height / 15, color=(0.8, 0.8, 0.45), size=30, centered=True)
    draw_word("press esc to pause", engine.width * 1/10, engine.height / 10 - engine.height / 15, color=(0.8, 0.8, 0.45), size=10, centered=True)


    if alarm:
        engine.shape_mode = ShapeMode.CENTER
        engine.color = (0.9, 0.2, 0.2)
        engine.draw_rectangle(engine.width / 2, engine.height / 10, 35, 100)
        engine.draw_circle(engine.width / 2, engine.height /10 + 100 / 2 + 10 + 35 / 2, 35)

    if show_words:
        for i in range(1, 3):
            if lockedword == 0:
                draw_word((word1, word2)[i - 1], engine.width / 2 + (i - 1.5) * 550, engine.height / 2.4, True,
                          progress, size=35)
            if lockedword == i:
                draw_word((word1, word2)[i - 1], engine.width / 2 + (i - 1.5) * 550, engine.height / 2.4, True,
                          progress, size=35)


def pallet_test():
    global key
    draw_menu_background(0.7)
    draw_word("press esc to pause", engine.width * 1/10, engine.height / 10 - engine.height / 15, color=(0.8, 0.8, 0.45), size=10, centered=True)
    draw_word("move cursor to rotate pallet", engine.width / 2, engine.height / 10 - engine.height / 15, color=(0.8, 0.8, 0.45), size=10, centered=True)
    pallet = 12 if engine.mouse_x > 4/5 * engine.width else 9 if engine.mouse_x > 3/5 * engine.width else 6 if engine.mouse_x > 2/5 * engine.width else 3 if engine.mouse_x > 1/5 * engine.width else 0
    palletr = 0 if engine.mouse_y > 2/3 * engine.height else 1 if engine.mouse_y > 1/3 * engine.height else 2
    list_pallets[int(pallet + palletr)].draw_fixed_size(engine.width / 2, engine.height / 2, 550, 550)
    return 1 if key == "escape" else -1


def render():
    global game_state, last_game_state, key
    last_game_state = game_state if game_state in range (4, 7) else last_game_state
    engine.background_color = (0.05, 0.05, 0.05)
    if game_state == -1:
        game_state = pallet_test()
    elif game_state == 0:
        game_state = draw_intro()
    elif game_state == 1:
        key = None
        game_state = draw_main_menu()
    elif game_state == 2:
        game_state = draw_credits()
    elif game_state == 3:
        game_state = draw_rules()
    elif game_state in range (4, 7):
        render_game(word1, word2)
    elif game_state == 7:
        game_state = draw_pause(last_game_state)
    elif game_state == 8:
        game_state = draw_end(last_game_state)

def if_pass():
    pass


def choose_words(difficulty: str):
    global word1, word2, lockedword, progress
    lockedword, progress = 0, 0

    letter = word1[-1] if what_word == 1 else word2[-1]
    word1, word2 = random.choice(word_levels[difficulty]), random.choice(word_levels[difficulty])
    while word1[0] == letter:
        word1, word2 = random.choice(word_levels[difficulty]), random.choice(word_levels[difficulty])
    while word2[0] == word1[0] or word2[0] == letter:
        word2 = random.choice(word_levels[difficulty])

def ur_dead(difficulty: str):
    global HP, ballx, bally, playerx, playery, botx, boty, xspeed, ballspeed, balldir, multiplier, points
    choose_words(difficulty)
    points -= 1
    HP -= 1
    multiplier = 0
    ballspeed = ballspeed * -1
    balldir = (random.randint(-100, 100) / (360 / (ballspeed + 0.1)))
    playerx, ballx = 0, 0

def play_game(difficulty: str):
    global HP, left, right, lockedword, word1, word2, progress, ballx, bally, playerx, playery, botx, boty, xspeed, ballspeed, balldir, multiplier, points, highscore, game_state, key, escape_counter, what_word, stat1, stat2, alarm
    if HP == 0:
        ballx, bally, playerx, playery, botx, boty, xspeed, ballspeed, balldir, points, multiplier, stat1, stat2 = random.randint(-100, 100), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        choose_words(difficulty)
        if difficulty == "practice":
            HP = 10
        if difficulty == "easy":
            HP = 5
        if difficulty == "hard":
            HP = 3

    else:
        words = (word1, word2)
        alarm = False
        if progress <= 1 and ballspeed <= 0:
            left, right = True if key == word1[0] and lockedword == 1 else False, True if key == word2[0] and lockedword == 2 else False
        for i in range(1, 3):
            word = words[i - 1]
            if lockedword == 0 and key == word[0]:
                what_word = i
                lockedword = i

            if lockedword == i:
                if key == word[progress if progress < len(word) else len(word) - 1]:
                    progress += 1
                    stat1 = stat1 + 1
                    if progress == len(word):
                        progress = 0
                        lockedword = 3

        if right:
            xspeed += 0.25
        elif left:
            xspeed -= 0.25
        else:
            xspeed = xspeed * 0.85 if sqrt(xspeed * xspeed) > 1 else 0
        xspeed = 0 if playerx <= -100 or playerx >= 100 else xspeed
        playerx = -100 if playerx < -100 else 100 if playerx > 100 else playerx + xspeed

        if math.floor(bally) in range(0, 360):
            if ballspeed < 0:
                window = 0.2 if difficulty == "hard" else 0.5
                if ((360 / -ballspeed) / engine.fps) - (((360 - bally) / -ballspeed) / engine.fps) >= window:
                    if lockedword == 3:
                        multiplier = 1
                elif multiplier != 1:
                    if lockedword == 3:
                        multiplier = 2
                    else:
                        alarm = True

            if bally <= -1 * ballspeed + 1 and lockedword == 3:
                if int(playerx) in range(int(ballx * 0.85) - int(engine.width / 32), int(ballx * 0.85) + int(engine.width / 32)):
                    stat2 += 1
                    points = points + 1 * multiplier
                    ballspeed = sqrt(ballspeed * ballspeed)
                    if points <= 0:
                        if difficulty == "practice" or "easy":
                            ballspeed = 2
                        if difficulty == "hard":
                            ballspeed = 3
                    else:
                        if difficulty == "practice":
                            ballspeed += 0.1
                            highscore[0] = points if points > highscore[0] else highscore[0]
                        if difficulty == "easy":
                            ballspeed += 0.2
                            highscore[1] = points if points > highscore[1] else highscore[1]
                        if difficulty == "hard":
                            ballspeed += 0.1
                            highscore[2] = points if points > highscore[2] else highscore[2]

                    balldir = random.randint(-100, 100) / 100
                    while not balldir * (360 / math.floor(ballspeed)) + int(ballx) in range(-100, 100):
                        balldir = random.randint(-100, 100) / 100
                    choose_words(difficulty)
                else:
                    ur_dead(difficulty)
                multiplier = 0

        elif bally < 0:
            ur_dead(difficulty)

        if bally > 360:
            bally = 360
            balldir = random.randint(-100, 100) / 10
            while not balldir * (360 / ballspeed) + int(ballx) in range(-100, 100):
                balldir = random.randint(-100, 100) / 10
            ballspeed = -ballspeed
            bally += ballspeed
            ballx += balldir

        bally += ballspeed
        ballx += balldir

        if HP == 0:
            game_state = 8

        if str(engine.key).lower() == "escape" and escape_counter == 0:
            pass
        else:
            escape_counter = 1

        if str(engine.key).lower() == "escape" and escape_counter == 1:
            game_state = 7




def evaluate():
    global button, button_counter, HP
    key_down_event(engine.key)
    if button_counter == 1:
        button_counter -= 1
        button = None
    if button != None:
        button_counter += 1

    HP = 0 if game_state not in range (4, 8) else HP

    if game_state == 4:
        play_game("practice")
    elif game_state == 5:
        play_game("easy")
    elif game_state == 6:
        play_game("hard")



def key_down_event(keyboard_button: str):
    global key, game_state
    if keyboard_button != None and keyboard_button != key:
        key = engine.key.lower()
        if debug:
            print(key)
            if key == "lshift":
                game_state -= 1
            if key == "rshift":
                game_state += 1

def key_up_event(keyboard_button: str):
    global key
    if keyboard_button == key:
        key = None


def mouse_pressed_event(mouse_x: int, mouse_y: int, mouse_button: MouseButton):
    global button
    button = str(mouse_button)[12:]




# Engine stuff; best not to mess with this:
engine._setup = setup
engine._evaluate = evaluate
engine._render = render
engine._mouse_pressed_event = mouse_pressed_event
engine._key_up_event = key_up_event

# Start the game loop:
engine.play()
