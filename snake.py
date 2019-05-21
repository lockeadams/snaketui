#!/usr/bin/python3

""" CURSES INTERFACE FOR PLAYING SNAKE """

import curses
import time
import random

def main(stdscr):

    # Curses initialization
    stdscr.nodelay(True)
    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
    lines, cols = stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1]

    # Game initialization
    head_line = round(lines / 2)
    head_col = round(cols / 2)
    direction = 'up'
    loop_time = 0.14
    apple_spawned = False
    apple_line, apple_col = 0, 0
    snake = [[head_line, head_col]]
    for i in range(1, 5):
        snake.append([head_line + i, head_col])
    snake_length = len(snake)

    # Game loop
    while True:

        # Update dimensions
        lines, cols = stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1]
        head_line = snake[0][0]
        head_col = snake[0][1]

        # Paint background
        for i in range(lines):
            for j in range(cols):
                stdscr.addstr(i, j, ' ', curses.color_pair(3))

        # Get keypresses
        try:
            key = stdscr.getkey()
            if key == 'h':
                direction = 'left'
            elif key == 'j':
                direction = 'down'
            elif key == 'k':
                direction = 'up'
            elif key == 'l':
                direction = 'right'
            continue
        except:
            pass

        # Check for game over
        line_edge = head_line == 0 or head_line == lines - 1
        col_edge = head_col == 0 or head_col == cols - 1
        snake_hit = False
        for i in range(len(snake)):
            for j in range(i + 1, len(snake)):
                if snake[i][0] == snake[j][0] and snake[i][1] == snake[j][1]:
                    snake_hit = True
        if line_edge or col_edge or snake_hit:
            stdscr.addstr(round(lines / 2), round(cols / 2) - 4, 'Game over', curses.A_BOLD)
            stdscr.refresh()

        # Move snake
        else:
            if snake_length == len(snake):
                snake.pop()
            if direction == 'left':
                loop_time = 0.07
                snake.insert(0, [head_line, head_col - 1])
            elif direction == 'down':
                loop_time = 0.14
                snake.insert(0, [head_line + 1, head_col])
            elif direction == 'up':
                loop_time = 0.14
                snake.insert(0, [head_line - 1, head_col])
            elif direction == 'right':
                loop_time = 0.07
                snake.insert(0, [head_line, head_col + 1])
            for i in snake:
                stdscr.addstr(i[0], i[1], '#', curses.A_BOLD | curses.color_pair(3))

            # Handle apples
            if head_line == apple_line and head_col == apple_col:
                apple_spawned = False
                snake_length += 1
            if not apple_spawned:
                apple_line = random.randrange(1, lines - 1)
                apple_col = random.randrange(1, cols - 1)
                apple_spawned = True
            stdscr.addstr(apple_line, apple_col, 'a', curses.color_pair(1) | curses.A_BOLD)

            # Display score
            stdscr.addstr(lines, 0, 'Score: ' + str(snake_length), curses.A_BOLD)
            stdscr.refresh()

            # Wait
            time.sleep(loop_time)

if __name__ == '__main__':
    curses.wrapper(main)
