# -*- coding: utf-8 -*-
# @Time    : 2020-07-18 1:10 AM
# @Author  : Yolanda (Yiqi) Zhi
# @FileName: sudoku_gui.py
# @Description:
# @Github:


import pygame
from typing import List, Tuple, Optional
from sudoku_text import board_valid




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

    def draw(self, window: pygame.Surface) -> None:
        """
        Render a cell with number
        """

        font = pygame.font.SysFont("Marker Felt", 40)

        gap = self.width / 9
        col_des = self.col * gap
        row_des = self.row * gap

        # if the slot is to be filled and the user is trying to fill it. Display the number in grey
        if self.temp != 0 and self.value == 0:
            # generate a Surface num_text to display
            num_text = font.render(str(self.temp), True, (128, 128, 128), None)
            # blit the number on the grid surface
            window.blit(num_text, (
                col_des + (gap / 2 - num_text.get_width() / 2), row_des + (gap / 2 - num_text.get_height() / 2)))
        # if the slot is filled, display the number in black
        elif self.value != 0:
            num_text = font.render(str(self.value), True, (0, 0, 0), None)
            window.blit(num_text, (
                col_des + (gap / 2 - num_text.get_width() / 2), row_des + (gap / 2 - num_text.get_height() / 2)))

        # if the slot is empty, do not draw

        # if the slot is select by the user, draw a red square
        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), pygame.Rect(col_des, row_des, gap, gap), 5)

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


class Grid:
    """
    A Sudoku Grid, consists of Cubes
    """

    def __init__(self, rows: int, cols: int, board: List[List[int]], width: int, height: int):
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

    def set_up_cell(self, row: int, col: int, value: int) -> None:
        """
        Set up a cell
        """

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
        cube_width = self.width / 9
        for row in range(self.rows + 1):
            if row % 3 == 0:
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
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].unselect()

        self.cubes[row][col].select()
        self.selected = (row, col)

    def click(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Get the click from the user and transcribe it as information based on the grid. If out of range of the board, return None. Otherwise, return (row, col) of the cube being clicked.
        """
        x, y = pos
        if 0<= x <= self.width and 0<= y <= self.height:
            cube_width = self.width / 9
            x = x // cube_width
            y = y // cube_width
            return (int(x), int(y))
        else:
            return None

    def is_finished(self) -> bool:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cubes[row][col].get_value () != 0:
                    return False
        return True


def make_display(width: int, height: int, background=None) -> pygame.Surface:
    window = pygame.display.set_mode((width, height))
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


def main():
    font = pygame.font.Font("/Library/Fonts/Herculanum.ttf", 50)
    pygame.display.set_caption("Sudoku")
    sudoku_img = pygame.image.load("icon.png")
    pygame.display.set_icon(sudoku_img)
    sqr_dim, board_dim = intro_window(font)
    # sudoku_window = make_display(1000, 1000, "sudoku_background.jpeg")
    # pygame.display.update()
    # while True:
    #     events = pygame.event.get()
    #     for event in events:
    #         print(event)


def intro_window(font):
    main_window = make_display(1000, 1000, "ocean.jpg")
    square_text_box, tr_sqr, br_sqr = render_text(main_window,
                                                  "Square Dimension: ",
                                                  1,
                                                  300,
                                                  (255, 255, 255),
                                                  "American Typewriter",
                                                  40)
    board_text_box, tr_bo, br_bo = render_text(main_window,
                                               "Board Dimension: ",
                                               1,
                                               300 + square_text_box.get_height() + 100,
                                               (255, 255, 255),
                                               "American Typewriter",
                                               40)
    input_box_sqr = pygame.Rect((tr_sqr[0] + 10, tr_sqr[1]), (200, br_sqr[1] - tr_sqr[1]))
    input_box_bo = pygame.Rect((tr_bo[0] + 10, tr_bo[1]), (200, br_bo[1] - tr_bo[1]))
    color_inactive = pygame.Color('grey')
    color_active = pygame.Color('green')
    color_sqr = color_bo = color_inactive
    active_sqr = active_bo = False
    text_sqr = pre_text_sqr = ''
    text_bo = pre_text_bo = ''
    square_dim_set = 0
    bo_dim_set = 0

    set_button = Button("Arial", 40, "ALL SET", pygame.Color("white"), pygame.Color("grey"), pygame.Color("green"))
    set_button_rect = set_button.create_button(main_window, 500, 600)

    while True:
        events = pygame.event.get()
        for event in events:
            # if square_dim_set != 0 and bo_dim_set != 0:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_sqr.collidepoint(event.pos):
                    active_sqr = not active_sqr
                else:
                    active_sqr = False
                if input_box_bo.collidepoint(event.pos):
                    active_bo = not active_sqr
                else:
                    active_bo = False
                if set_button_rect.collidepoint(event.pos):
                    if square_dim_set != 0 and bo_dim_set != 0:
                        set_button.press_the_button(main_window)
                        return (square_dim_set, bo_dim_set)

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

                if active_bo:
                    if event.key == pygame.K_RETURN:
                        bo_dim_set = int(text_bo)
                        active_bo = not active_bo
                        print(bo_dim_set)
                    elif event.key == pygame.K_BACKSPACE:
                        text_bo = text_bo[:-1]
                    else:
                        text_bo += event.unicode
            color_sqr = color_active if active_sqr else color_inactive
            color_bo = color_active if active_bo else color_inactive

        pygame.draw.rect(main_window, color_sqr, input_box_sqr, 0)
        pygame.draw.rect(main_window, color_bo, input_box_bo, 0)
        txt_surface_sqr = font.render(text_sqr, True, pygame.Color('white'), )
        txt_surface_bo = font.render(text_bo, True, pygame.Color('white'), )
        main_window.blit(txt_surface_sqr, (tr_sqr[0] + 10, tr_sqr[1]))
        main_window.blit(txt_surface_bo, (tr_bo[0] + 10, tr_bo[1]))
        pygame.display.update()




if __name__ == "__main__":
    main()
    # python_ta.check_all()
