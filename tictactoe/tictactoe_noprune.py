"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_occur, o_occur = 0, 0
    for row in board:
        x_occur += row.count(X)
        o_occur += row.count(O)
    if o_occur < x_occur:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_list = []
    for r_idx, row in enumerate(board):
        for c_idx, col in enumerate(row):
            if col == EMPTY:
                action_list.append((r_idx, c_idx))
    return action_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid Move")
    current_player = player(board)
    # Copy the board to return a new board without modifying the original
    new_board = copy.deepcopy(board)
    new_board[i][j] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if terminal(board):
        util_val = utility(board)
        if util_val == 1:
            return X
        elif util_val == -1:
            return O
        else:
            return None
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there are still empty squares
    board_full = True
    for row in board:
        if EMPTY in row:
            board_full = False
    if board_full:  # If the board is full, the game is over
        return True
    # Check if there's a winner
    util_val = utility(board)
    if util_val == 0:  # If there's no winner, the game is not over
        return False
    else:  # Otherwise, there is a winner, the game is over
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    scores = {X:1, O:-1, EMPTY:0}
    # Check the sums of the rows for a win
    for idx,row in enumerate(board):
        row_val = 0
        for row_idx, val in enumerate(row):
            row_val += scores[val]
            if row_val == 3:
                return 1
            elif row_val == -3:
                return -1
    # Check the sums of the columns for a win
    for c_idx in range(3):
        col_val = 0
        for r_idx in range(3):
            col_val += scores[board[r_idx][c_idx]]
        if col_val == 3:
            return 1
        elif col_val == -3:
            return -1
    # Check the sums of the diagonals for a win
    diag_vals = [0,0]
    diag_vals[0] = scores[board[0][0]] + scores[board[1][1]] + scores[board[2][2]]
    diag_vals[1] = scores[board[0][2]] + scores[board[1][1]] + scores[board[2][0]]
    if 3 in diag_vals:
        return 1
    elif -3 in diag_vals:
        return -1
    else:  # If we haven't found 3-in-a-row, there is no winner yet
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    # Copy the board so as not to affect current state
    new_board = copy.deepcopy(board)
    if player(board) == X:
        v, best_action = max_value(board)
    else:
        v, best_action = min_value(board)
    return best_action


def max_value(state):
    """
    Returns the maximum value and action that leads to it taken based on state.
    """
    if terminal(state):
        return utility(state), None
    best_action = None
    # Init with smaller-than-possible v
    v = -2
    for action in actions(state):
        temp_v, _ = min_value(result(state, action))
        if temp_v > v:
            v = temp_v
            best_action = action
    return v, best_action

def min_value(state):
    """
    Returns the minimum value and action that leads to it taken based on state.
    """
    if terminal(state):
        return utility(state), None
    best_action = None
    # Init with larger-than-possible v
    v = 2
    for action in actions(state):
        temp_v, _ = max_value(result(state, action))
        if temp_v < v:
            v = temp_v
            best_action = action
    return v, best_action
