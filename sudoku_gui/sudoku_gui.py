# -*- coding: utf-8 -*-
# @Time    : 2020-07-18 1:10 AM
# @Author  : Yolanda (Yiqi) Zhi
# @FileName: sudoku_gui.py
# @Description:
# @Github:

import pygame

# initialize the font module
pygame.font.init()


class Cube:
    """
    A cube that is used to represent a cell in the sudoku board
    """

    def __init__(self, value: int, row: int, col: int, width: int, height: int):
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


if __name__ == "__main__":
    import python_ta

    # python_ta.check_all()
