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
    #if initial_state() is True:
        #return X
    
    #if terminal(board) is True:
        #return X
    
    x_count = 0
    o_count = 0
    
    
    for row in board:
        for cell in row:
            if cell == X:
                x_count+=1
            elif cell == O:
                o_count+=1
    
    if x_count > o_count:
        return O
    else:
        return X
                

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    if terminal(board):
        return all_actions
       
    for row in range(len(board)):
        for cell in range(len(board[row])):
            if board[row][cell] is EMPTY:
                my_tuple = (row, cell)
                all_actions.add(my_tuple)

    return all_actions    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        raise Exception("No action provided")

    my_board = copy.deepcopy(board)
    # action is a tuple (i, j)
    # if i < 0 or greater than 2
    # if j < 0 or greater than 2
    # illegal action
    if not 0 <= action[0] <= 2 or not 0 <= action[1] <= 2:
        raise Exception("illegal action")
    
    if player(board) is O:
        if my_board[action[0]][action[1]] is EMPTY:
            my_board[action[0]][action[1]] = O
        else:
            raise Exception("cell is not empty to place O")
            
        
    elif player(board) is X:
        if my_board[action[0]][action[1]] is EMPTY:
            my_board[action[0]][action[1]] = X
        else:
            raise Exception("cell is not empty to place X")
    
    return my_board
        
    # action on the board by the player
    # board, action -> resulting new board
    
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # vertically: 
    #  0,0; 1,0; 2,0
    #  0,1; 1,1; 2,1
    #  0,2; 1,2; 2,2
    
    # horizontally:
    #  0,0; 0,1; 0,2
    #  1,0; 1,1; 1,2
    #  2,0; 2,1; 2,2
    
    # diagonally:
    
    # 0,2; 1,1; 2,0
    # 0,0; 1,1; 2,2

    # vertical
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
        
    # horizotal
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]
        
    # diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board [0][2] != EMPTY:
        return board[0][2]
    
    
            
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if winner
    if winner(board) is O or winner(board) is X:
        return True
    
    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        print("Game is already over. No actions available.")
        return None
    
    # function MIN_VALUE
    # if terminal state -> return utility(state)
    # v = infinity
    # for action in actions(state)
    # v = min(v, max_value(result(state, action)))
    # return v
    
    def MIN_VALUE(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, MAX_VALUE(result(board, action)))
        return v

    # function MAX_VALUE
    # if terminal state -> return utility(state)
    # v = - inf
    # for action in actions(state):
    # v = max(v, MIN_VALUE(result(state, action)))
    # return v
    
    def MAX_VALUE(board):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, MIN_VALUE(result(board, action)))
        return v
    
    best_action = None
    current_player = player(board)
    
    if not actions(board): 
        return None
    
    # maximize for X
    if current_player == X:
        best_value = float('-inf')
        for action in actions(board):
            value = MIN_VALUE(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    
    # minimize for O
    elif current_player == O:
        best_value = float('inf')
        for action in actions(board):
            value = MAX_VALUE(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
                
    return best_action
   