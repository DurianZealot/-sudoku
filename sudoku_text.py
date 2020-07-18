"""
A sudoku solver with text for display.

-*- coding: utf-8 -*-
 @Time    : 2020-07-17 3:21 AM
 @Author  : Yolanda (Yiqi) Zhi
 @FileName: sudoku_text.py
 @Github:
"""
from typing import List, Optional, Tuple


def main() -> None:
    """A main function of the sudoku solver"""
    print("Welcome to the sudoku solver!")

    # prompt users to tell the square size of the sudoku
    # Example: A 12 * 12 soduoku board has SQUARE_DIM=3, BOARD_DIM=4
    while True:
        try:
            square_dim = int(input("Please enter the square dimension of"
                                   " your sudoku board: "))
            break
        except ValueError:
            print("Invalid input. Try again please.")
    while True:
        try:
            board_dim = int(input("Please enter the board dimension of "
                                  "your sudoku board: "))
            break
        except ValueError:
            print("Invalid input. Try again please.")

    # get the user input sudoku board
    print("Now it is time to enter your sudoku board for solving.")

    to_solve_board = read_a_board(square_dim, board_dim)
    print_board(square_dim, board_dim, to_solve_board)
    solve_board(square_dim, to_solve_board)
    print("Solution")
    print_board(square_dim, board_dim, to_solve_board)


def read_a_board(square_dim: int, board_dim: int) -> List[List]:
    """Read and return a user input sudoku board"""
    board = []
    for row in range(board_dim**2):
        row_arr = []
        print("It is line {}".format(row+1))
        for col in range(square_dim**2):
            print("it is column {}".format(col+1))
            while True:
                try:
                    num = int(input("Enter the number: "))
                    break
                except ValueError:
                    print("Invalid input. Try again.")

            row_arr.append(num)
        board.append(row_arr)
    return board


def solve_board(square_dim: int, board: [List[List]]) -> bool:
    """A recursive function to solve the soduku board. If sudoku is
     solved, return true. Otherwise, return False"""
    found_pos = find_empty(board)
    if found_pos is None:
        return True
    for num in range(1, square_dim ** 2 + 1):
        if board_valid(square_dim, board, num, found_pos):
            board[found_pos[0]][found_pos[1]] = num
            if solve_board(square_dim, board):
                return True
            else:
                board[found_pos[0]][found_pos[1]] = 0
    return False


def board_valid(square_dim: int,
                board: [List[List]],
                num: int,
                position: Tuple[int, int]) -> bool:
    """Check if a purposed input @num at @position will make @board
    valid or not
    """
    row_pos, col_pos = position[0], position[1]

    # Check validation on the same row
    for col in range(len(board[0])):
        if col != col_pos and board[row_pos][col] == num:
            return False

    # Check validation on the same column
    for row in range(len(board)):
        if row != row_pos and board[row][col_pos] == num:
            return False

    # Check validation in the same square
    sqr_col = col_pos // square_dim
    sqr_row = row_pos // square_dim
    for col in range(sqr_col * square_dim, (sqr_col + 1) * square_dim):
        for row in range(sqr_row * square_dim, (sqr_row + 1) * square_dim):
            if (row, col) != position and board[row][col] == num:
                return False
    return True


def print_board(square_dim: int, board_dim: int, board: List[List]) -> None:
    """Print out a sukudo board"""
    board_len = len(board)
    seperate_line = "- " * (square_dim + 1) * (board_dim + 1)

    for row in range(board_len + 1):
        if row % square_dim == 0:
            print(seperate_line)
            if row == board_len:
                break
        for col in range(len(board[0])):
            if col % square_dim == 0 and col != 0:
                print(" | ", end="")
            if col == board_dim * square_dim - 1:
                print(board[row][col])
            else:
                print(str(board[row][col]) + " ", end="")


def find_empty(board: List[List]) -> Optional[Tuple[int, int]]:
    """Find a spot on @board that is not filled. If not found, return None"""
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return None


if __name__ == "__main__":
    import python_ta

    # python_ta.check_all()

    board_test = [
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

    board_easy = [
        [0, 2, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 7, 0, 5, 8, 0, 6, 0],
        [0, 0, 0, 3, 0, 0, 8, 2, 7],
        [0, 5, 3, 0, 0, 0, 0, 7, 4],
        [0, 0, 0, 4, 2, 3, 0, 0, 0],
        [8, 4, 0, 0, 0, 0, 6, 3, 0],
        [1, 3, 5, 0, 0, 7, 0, 0, 0],
        [0, 8, 0, 1, 4, 0, 3, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 5, 0]
    ]

    board_medium = [
        [0, 0, 0, 1, 3, 0, 0, 0, 0],
        [3, 4, 0, 0, 9, 0, 0, 0, 6],
        [0, 0, 0, 0, 0, 6, 3, 0, 4],
        [0, 0, 3, 0, 0, 1, 5, 0, 0],
        [2, 1, 0, 3, 6, 5, 0, 4, 7],
        [0, 0, 4, 8, 0, 0, 1, 0, 0],
        [8, 0, 2, 6, 0, 0, 0, 0, 0],
        [6, 0, 0, 0, 4, 0, 0, 8, 3],
        [0, 0, 0, 0, 8, 7, 0, 0, 0]
    ]

    board_hard = [
        [0, 5, 0, 9, 0, 8, 0, 0, 3],
        [0, 8, 4, 0, 6, 0, 0, 0, 9],
        [7, 0, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 3, 0, 0, 1, 0],
        [4, 0, 0, 8, 2, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 7, 6],
        [2, 0, 3, 0, 7, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 3, 0]
    ]

    # solve_board(3, board_hard)
    # print_board(3, 3, board_hard)
    main()
