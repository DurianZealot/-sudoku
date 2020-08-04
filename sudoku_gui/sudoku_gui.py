# -*- coding: utf-8 -*-
# @Time    : 2020-07-18 1:10 AM
# @Author  : Yolanda (Yiqi) Zhi
# @FileName: sudoku_gui.py
# @Description:
# @Github:
import sys
from math import sqrt
import time
import pygame
from typing import List, Tuple, Optional


from sudoku_text import *




# initialize the font module
pygame.font.init()
# initialize a pygame window
pygame.init()


class Button:

    def __init__(self, font, font_size, text, text_col, inactive_col, active_col):
        self.text = text
        self.inactive_col = inactive_col
        self.active_col = active_col
        self.font_size = font_size
        self.font = font
        self.text_col = text_col
        self.cur_col = inactive_col
        self.x = None
        self.y = None

    def __generate_font(self):
        return pygame.font.SysFont(self.font, self.font_size)

    def get_button_size(self):
        w, h = self.__generate_font().size(self.text)
        return (w, h)

    def create_button(self, surface, x, y):
        # set up the button coordinate
        self.x = x
        self.y = y


        # draw the button
        pygame.draw.rect(surface, self.inactive_col, pygame.Rect((x, y), self.get_button_size()), 0)

        # render the text
        button_text = self.__generate_font().render(self.text, True, self.text_col, None)
        surface.blit(button_text, (x, y))

        # blit the rect of the button
        button_rect = pygame.Rect((x, y), self.get_button_size())

        pygame.display.update()
        return button_rect

    def press_the_button(self, surface):
        if self.cur_col == self.inactive_col:
            self.cur_col = self.active_col
        else:
            self.cur_col = self.inactive_col
        pygame.draw.rect(surface, self.cur_col, pygame.Rect((self.x, self.y), self.get_button_size()), 0)
        button_text = self.__generate_font().render(self.text, True, self.text_col, None)
        surface.blit(button_text, (self.x, self.y))
        pygame.display.update()



    def get_color(self):
        return self.cur_col



class Cube:
    """
    A cube that is used to represent a cell in the sudoku board
    """

    def __init__(self, value: int, row: int, col: int, width: float, height: float):
        """
        value: the value of a slot
        row: the row number
        col: the column number
        width: the width of the cube
        height: the height of the cube
        selected: True if the solt is selected
        temp: temporary value
        """
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.fixed = False

    def fix_value(self) -> None:
        self.fixed = True

    def draw(self, window: pygame.Surface) -> None:
        """
        Render a cell with number
        """

        font = pygame.font.SysFont("Marker Felt", 40)

        gap = self.width

        col_des = self.col * gap
        row_des = self.row * gap

        # if the slot is to be filled and the user is trying to fill it. Display the number in grey
        if self.value == 0 and self.temp != 0:
            # generate a Surface num_text to display
            num_text = font.render(str(self.temp), True, (128, 128, 128), None)
            # blit the number on the grid surface
            window.blit(num_text, (
                row_des + (gap / 2 - num_text.get_width() / 2), col_des + (gap / 2 - num_text.get_height() / 2)))

        # if the slot is filled, display the number in black
        elif self.value != 0:
            num_text = font.render(str(self.value), True, (0, 0, 0), None)
            window.blit(num_text, (
                row_des + (gap / 2 - num_text.get_width() / 2), col_des + (gap / 2 - num_text.get_height() / 2)))

        # if the slot is empty and not selected, do nothing

        # if the slot is select by the user, draw a red square
        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), pygame.Rect(row_des, col_des, gap, gap), 5)




    def set(self, value: int) -> None:
        """
        Set the cell value
        """

        self.value = value

    def set_temp(self, temp: int) -> None:
        """
         Set the temp value
        """

        self.temp = temp

    def select(self) -> None:
        self.selected = True

    def unselect(self) -> None:
        self.selected = False

    def get_temp(self) -> int:
        return self.temp

    def get_value(self) -> int:
        return self.value


class Grid:
    """
    A Sudoku Grid, consists of Cubes
    """

    def __init__(self, rows: int, cols: int, board: List[List[int]], width: int, height: int, square_dim: int):
        """

        @model : List[List[int]] to store the current data on the board
        """
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(board[row][col], row, col, width / cols, height / rows) for col in range(cols)] for row in
                      range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.square_dim = square_dim
        self.set = False
        self.selected = None
        self.answer = None

    def set_up_cell(self, row: int, col: int, value: int) -> None:
        """
        Set up a cell
        """
        self.cubes[row][col].set(value)

    def update_model(self) -> None:
        """
        Update model
        """
        self.model = [[self.cubes[row][col].get_value() for col in range(self.cols)] for row in range(self.rows)]

    def place(self, value: int) -> bool:
        """
        ONLY triggered by the user pressed ENTER
        Place a value at the selected cell and check if valid.
        If valid, return True.Otherwise, return False and reset the cell.
        """
        row, col = self.selected
        # only allow the user to click on cubes that is not filled
        if self.cubes[row][col].get_value() == 0:
            self.cubes[row][col].set(value)
            self.update_model()

            # if the value that user enter is correccted, return true
            if board_valid(self.model, value, (row, col)) and is_correst(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, value: int) -> None:
        row, col = self.selected
        self.cubes[row][col].set_temp(value)

    def draw_grid(self, window: pygame.Surface) -> None:
        # draw grid lines
        cube_width = self.width / self.cols
        for row in range(self.rows + 1):
            if row % self.square_dim == 0:
                thick = 4
            else:
                thick = 1

            pygame.draw.line(window, (0, 0, 0), (0, row * cube_width), (self.width, row * cube_width), thick)
            pygame.draw.line(window, (0, 0, 0), (row * cube_width, 0), (row * cube_width, self.height), thick)

    def draw_cubes(self, window: pygame.Surface) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].draw(window)

    def select(self, row, col):
        # Reset all other selected cubes
        for r in range(self.rows):
            for c in range(self.cols):
                self.cubes[r][c].unselect()

        self.cubes[row][col].select()
        self.selected = (row, col)

    def click(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Get the click from the user and transcribe it as information based on the grid. If out of range of the board, return None. Otherwise, return (row, col) of the cube being clicked.
        """
        x, y = pos
        if 0<= x <= self.width and 0<= y <= self.height:
            cube_width = self.width / (self.square_dim**2)
            x = x // cube_width
            y = y // cube_width
            return (int(x), int(y))
        else:
            return None

    def is_finished(self) -> bool:
        for row in range(len(self.cubes)):
            for col in range(len(self.cubes[0])):
                if self.cubes[row][col].get_value() == 0:
                    return False
        return True

    def sketch_init_board(self, value):
        print("set " + "( " + str(self.selected[0]) + ", " + str(self.selected[1]) + ")")
        self.cubes[self.selected[0]][self.selected[1]].set_temp(value)


    def solvable(self) -> bool:
        temp = []
        for i in range(len(self.cubes)):
            row = []
            for j in range(len(self.cubes[0])):
                row.append(self.cubes[j][i].get_temp())
            temp.append(row)

        if solve_board(int(sqrt(len(self.cubes))), temp):
            self.answer = temp

            print_board(int(sqrt(len(self.cubes))), int(sqrt(len(self.cubes))), self.answer)

            return True
        else:
            return False

    def set_up(self) -> None:
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                self.cubes[i][j].set(self.cubes[i][j].get_temp())
                self.cubes[i][j].set_temp(0)

    def reset(self) -> None:
        for i in range(len(self.cubes)):
            for j in range(len(self.cubes[0])):
                self.cubes[i][j].set_temp(0)
        self.answer = None


    def attempt_validate(self) -> bool:
        col, row = self.selected
        if self.answer[row][col] == self.cubes[col][row].get_temp():
            # the user enter a right value
            self.cubes[col][row].set(self.cubes[col][row].get_temp())
            self.cubes[col][row].set_temp(0)
            return True
        else:
            return False



def make_display(width: int, height: int, background=None) -> pygame.Surface:
    window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    if background is not None:
        background_image = pygame.image.load(background).convert()
        background_image_rect = background_image.get_rect(center=window.get_rect().center)
        window.blit(background_image, background_image_rect)
    pygame.display.update()
    return window


def render_text(window: pygame.Surface,
                text: str,
                horizontal: int,
                vertical: int,
                color: Tuple[int, int, int],
                font: str,
                font_size: int) -> List:

    # initialize font
    font_init = pygame.font.SysFont(font, font_size)

    # render text
    text_box = font_init.render(text, True, color)
    text_width = text_box.get_width()

    if horizontal == 1:
        hori_pos = (window.get_width() / 2) - (text_width / 2)
    else:
        hori_pos = 0

    # blit text into the window
    window.blit(text_box, (hori_pos, vertical))

    top_right = (hori_pos + text_width, vertical)
    bottom_right = (hori_pos + text_width, vertical + text_box.get_height())

    # return this text box in order to arrange other text box
    # also return top right and bottom right position of the box
    return [text_box, top_right, bottom_right]

def redraw_grid(window: pygame.Surface, board: Grid, time: float):
    # Draw the background
    make_display(window.get_width(), window.get_height(), "sudoku_background.jpeg")

    # Draw the Grid
    board.draw_grid(window)

    # Draw cubes
    board.draw_cubes(window)

    pygame.display.update()

def update_time(time_diff: int, window: pygame.Surface) -> None:
    minute = time_diff // 60
    sec = time_diff % 60

    font = pygame.font.SysFont("Marker Felt", 30)
    print(f'the size of the window is {window.get_width()} and {window.get_height()}')
    width = window.get_width()
    height = window.get_height() - 100

    time_surface = font.render(f'TIME : {minute}:{sec}', True, pygame.Color("Black"))
    window.blit(time_surface, (width - time_surface.get_width(), height + time_surface.get_height() // 2))

    pygame.display.update()


def game_finish(window: pygame.Surface) -> None:
    pygame.init()
    font = pygame.font.Font("/Library/Fonts/Herculanum.ttf", 20)
    game_finish_page = make_display(window.get_width(), window.get_height(), "game_over.jpg")
    congrats = font.render("Congrulations!", True, pygame.Color("white"))
    window.blit(congrats,
                ((window.get_width() - congrats.get_width()) // 2,  (window.get_height() - congrats.get_height()) // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

def main():
    # initialize the setting on the sudoku board
    font = pygame.font.Font("/Library/Fonts/Herculanum.ttf", 50)
    pygame.display.set_caption("Sudoku")
    sudoku_img = pygame.image.load("icon.png")
    pygame.display.set_icon(sudoku_img)

    # get the user-defined size of the board
    # number of cubes : (sqr_dim ** 2) ** 2
    sqr_dim = intro_window(font)

    # shift to the sudoku board
    sudoku_window = make_display(sqr_dim**2*50, sqr_dim**2*50+100, "sudoku_background.jpeg")

    init_board = [[0 for i in range(sqr_dim ** 2)] for i in range(sqr_dim ** 2)]
    init_grid = Grid(sqr_dim ** 2, sqr_dim ** 2, init_board, sqr_dim ** 2*50, sqr_dim ** 2*50, sqr_dim)


    set_button = Button("MarkerFelt", 30, "SET", pygame.Color("white"),  pygame.Color("grey"), pygame.Color("green"))
    start_button = Button("MarkerFelt", 30, "START", pygame.Color("white"), pygame.Color("grey"), pygame.Color("green"))
    pause_button = Button("MarkerFelt", 30, "PAUSE", pygame.Color("white"), pygame.Color("grey"), pygame.Color("red"))

    board_is_set = False
    key = number = None
    start = False
    pause = False

    while True:
        redraw_grid(sudoku_window, init_grid, 10.0)

        if init_grid.is_finished():
            break
        if start and not pause:
            # update the running time
            play_time = round(time.time() - start_time)
            update_time(play_time, sudoku_window)

        if not board_is_set:
            set_button_rect = set_button.create_button(sudoku_window, 0, sqr_dim ** 2 * 50 + 30)
        if board_is_set and not start:
            start_button_rect = start_button.create_button(sudoku_window, 0, sqr_dim ** 2 * 50 + 30)
        if start:
            pause_button_rect = pause_button.create_button(sudoku_window, 0, sqr_dim ** 2 * 50 + 30)


        for event in pygame.event.get():
            # if the user close the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            # if the user set the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                if set_button_rect.collidepoint(event.pos) and not board_is_set:
                    set_button.press_the_button(sudoku_window)
                    if init_grid.solvable():
                        # if the user enter a board that is solvable
                        board_is_set = True
                        # set all all cubes' value
                        init_grid.set_up()
                        break
                    else:
                        # if the user enter a board that is not solvable
                        # reset all input in the board
                        init_grid.reset()

                        key = number = None
                        continue
                if not start and board_is_set and start_button_rect.collidepoint(event.pos):
                    # the user click the start button and the clock count down should start
                    start_button.press_the_button(sudoku_window)
                    start_time = time.time()
                    start = True
                    break

                if start and pause_button_rect.collidepoint(event.pos):
                    pause = not pause
                    start_time = round(time.time() - start_time)
                    pause_button.press_the_button(sudoku_window)

                # if the user try to enter a value on the board
                clicked = init_grid.click(event.pos)
                if clicked is not None:
                    init_grid.select(clicked[0], clicked[1])
                    number = key = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_0:
                    key = 0
                if event.key == pygame.K_BACKSPACE:
                    print("Key deleted is entered")
                    key = None
                    if number is not None:
                        if len(str(number)) <= 1:
                            number = 0
                        else:
                            number = int(str(number)[:-1])
                if number is None:
                    number = key
                elif number is not None and key is not None:
                    number = int(str(number) + str(key))
            if init_grid.selected is not None and number is not None:
                if not board_is_set:
                    init_grid.sketch_init_board(number)
                if board_is_set:
                    if start:
                        init_grid.sketch(number)

                        init_grid.attempt_validate()

                    else:
                        number = None

                print(init_grid.selected)
                print("input value is " + str(number))
                key = None
    game_finish(sudoku_window)



def intro_window(font):
    main_window = make_display(1000, 1000, "ocean.jpg")
    square_text_box, tr_sqr, br_sqr = render_text(main_window,
                                                  "Square Dimension: ",
                                                  1,
                                                  300,
                                                  (255, 255, 255),
                                                  "American Typewriter",
                                                  40)
    input_box_sqr = pygame.Rect((tr_sqr[0] + 10, tr_sqr[1]), (200, br_sqr[1] - tr_sqr[1]))
    color_inactive = pygame.Color('grey')
    color_active = pygame.Color('green')
    color_sqr = color_bo = color_inactive
    active_sqr = False
    text_sqr = pre_text_sqr = ''
    square_dim_set = 0

    set_button = Button("Arial", 40, "ALL SET", pygame.Color("white"), pygame.Color("grey"), pygame.Color("green"))
    set_button_rect = set_button.create_button(main_window, 500, 600)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            # if square_dim_set != 0:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_sqr.collidepoint(event.pos):
                    active_sqr = not active_sqr
                else:
                    active_sqr = False
                if set_button_rect.collidepoint(event.pos):
                    if square_dim_set != 0:
                        set_button.press_the_button(main_window)
                        return square_dim_set

            if event.type == pygame.KEYDOWN:
                if active_sqr:
                    if event.key == pygame.K_RETURN:
                        square_dim_set = int(text_sqr)
                        active_sqr = not active_sqr
                        print(square_dim_set)
                    elif event.key == pygame.K_BACKSPACE:
                        text_sqr = text_sqr[:-1]
                    else:
                        text_sqr += event.unicode

            color_sqr = color_active if active_sqr else color_inactive

        pygame.draw.rect(main_window, color_sqr, input_box_sqr, 0)
        txt_surface_sqr = font.render(text_sqr, True, pygame.Color('white'), )
        main_window.blit(txt_surface_sqr, (tr_sqr[0] + 10, tr_sqr[1]))
        pygame.display.update()




if __name__ == "__main__":
    main()
    # python_ta.check_all()
