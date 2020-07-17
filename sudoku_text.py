"""
A sudoku game and a solver with text for display.

-*- coding: utf-8 -*-
 @Time    : 2020-07-17 3:21 AM
 @Author  : Yolanda (Yiqi) Zhi
 @FileName: sudoku_text.py
 @Github:
"""
from typing import List, Optional, Tuple

SQUARE_DIM = 2
BOARD_DIM = 1


def print_board(square_dim: int, board_dim: int, board: List[List]) -> None:
    """Print out a sukudo board"""
    board_len = len(board)
    seperate_line = "- " * (square_dim + 1) * (board_dim + 1)

    for row in range(board_len+1):
        if row % SQUARE_DIM == 0:
            print(seperate_line)
            if row == board_len:
                break
        for col in range(len(board[0])):
            if col % SQUARE_DIM == 0 and col != 0:
                print(" | ", end="")
            if col == board_dim * square_dim - 1:
                print(board[row][col])
            else:
                print(str(board[row][col]) + " ", end="")


def find_empty(board: List[List]) -> Optional[Tuple[int, int]]:
    """Find a spot that is not filled. If not found, return None"""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return None


if __name__ == "__main__":
    import python_ta

    python_ta.check_all()

    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    board_2 = [
        [1, 2, 3, 4], [1, 2, 3, 4],
        [1, 2, 3, 4], [1, 2, 3, 4]
    ]

    board_3 = [
        [1, 2],
        [3, 4]
    ]

    # print_board(SQUARE_DIM, BOARD_DIM, board_3)
    # print(find_empty(board))
