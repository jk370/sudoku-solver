import numpy as np
from copy import deepcopy

class Sudoku:
    def __init__(self, sudoku):
        '''Initialises sudoku board'''
        self.sudoku = sudoku
        self.size = 9
        self.legals = {}
        
    def get_size(self):
        '''Returns the size of the board'''
        return self.size
    
    def get_board(self):
        '''Returns the current state of the sudoku board'''
        return self.sudoku
    
    def set_board(self, board):
        '''Sets the current state of the sudoku board'''
        self.sudoku = board
    
    def print_board(self):
        '''Prints the current state of the board'''
        for i in range (0,self.size):
            print(self.sudoku[i])
        print("\n")
    
    def is_legal_move(self, row, col, move):
        '''Checks if move is legal in the given location'''
        legal_row = self.check_row(row, move)
        legal_col = self.check_col(col, move)
        legal_grid = self.check_grid(row, col, move)
        return ((legal_row and legal_col) and legal_grid)
    
    def place_tile(self, row, col, tile):
        '''Places the tile at the given row and column'''
        self.sudoku[row][col] = tile
    
    def check_row(self, row, move):
        '''Checks if the given move is legal in that row'''
        legal = True
        for i in range(0, self.size):
            if self.sudoku[row][i] == move:
                legal = False
                
        return legal
    
    def check_col(self, col, move):
        '''Checks if the given move is legal in that column'''
        legal = True
        for i in range(0, self.size):
            if self.sudoku[i][col] == move:
                legal = False
                
        return legal
    
    def check_grid(self, row, col, move):
        '''Check if the given move is legal in that grid'''
        hor_grid = (col // 3) * 3
        ver_grid = (row // 3) * 3
        legal = True
        
        for i in range(ver_grid, ver_grid + 3):
            for j in range(hor_grid, hor_grid+3):
                if self.sudoku[i][j] == move:
                    legal = False

        return legal
    
    def solve(self):
        '''Solves all the single options on the game board'''
        while True:
            # Assign starting variables
            self.legals = {}
            legal_moves = []
            changes = 0
            # Loop through game board
            for row in range(0, self.size):
                for col in range(0, self.size):
                    # Check if number has not already been placed
                    if self.sudoku[row][col] == 0:
                        # Test each number against constraints
                        for test in range(1, self.size+1):
                            if self.is_legal_move(row, col, test):
                                legal_moves.append(test)
                        # Take move if it is the only legal move
                        if len(legal_moves) == 1:
                            self.place_tile(row, col, legal_moves[0])
                            changes += 1
                        # Else add legal moves to dictionary
                        else:
                            self.legals[(row,col)] = legal_moves
                        # Reset legal moves list for next cell
                        legal_moves = []

            # Break loop if there are no more single move constraints            
            if changes == 0:
                break
                
    def check_complete(self):
        '''Checks if the board has been filled'''
        complete = True
        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.sudoku[row][col] == 0:
                    complete = False
                    break
        
        return complete
    
    def continue_solve(self):
        '''Continues solvings puzzles not satisfied by constraints through backtracking'''
        min_length = 9
        # Find square with lowest number of legal moves
        for value in self.legals.values():
            if len(value) < min_length:
                min_length = len(value)
        
        # Return -1 array if board is unsolveable (no legal moves)
        if min_length == 0:
            unsolveable_board = np.full((self.get_size(), self.get_size()), -1, dtype = int)
            unsolveable = Sudoku(unsolveable_board)
            return unsolveable
        
        # Otherwise, start backtracking
        for key in self.legals.keys():
            if len(self.legals[key]) == min_length:
                # Begin backtracking with least possible options
                for move in self.legals[key]:
                    row, col = key
                    # Create new board and try first move
                    new_board = Sudoku(deepcopy(self.sudoku))
                    new_board.place_tile(row, col, move)
                    # Attempt to solve remainder through constraints only
                    new_board.solve()
                    # If this complete the board, return it
                    if new_board.check_complete():
                        return new_board
                    # Else recursively call backtracking with slightly more filled in board
                    else:
                        new_board = new_board.continue_solve()
                        # Return board if it has been complete, else move onto next move
                        if new_board.check_complete() and new_board.get_board()[0][0] != -1:
                            return new_board
                return self
                               