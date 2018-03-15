import Sudoku

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array of integers
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    # First complete constraint propagation
    s = Sudoku(sudoku)
    s.solve()
    
    # Return complete board or start backtracking
    if s.check_complete():
        return (s.get_board())
    
    else:
        s = s.continue_solve()
        if s.check_complete():
            return s.get_board()
        else:
            unsolveable = np.full((s.get_size(), s.get_size()), -1, dtype = int)
            return unsolveable