# -*- coding: utf-8 -*-
# @Time    : 2020-07-18 1:10 AM
# @Author  : Yolanda (Yiqi) Zhi
# @FileName: sudoku_gui.py
# @Description:
# @Github:

import pygame
from sudoku_text import board_valid
from typing import List, Tuple

# initialize the font module
pygame.font.init()


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

    # def click(self, pos: Tuple[int, int]) -> None:







if __name__ == "__main__":
    import python_ta

    # python_ta.check_all()
