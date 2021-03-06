# ...
#  ...
#   ...

#  black 
#   0 1 2      wh
#    3 4 5     i
#     6 7 8    te

#  EMPTY BOARD SIZE OF BOARD_SIZE
from Projects.base.util.colors import colors, pieces

class Hex:
    C_PLAYER1 = pieces.C_PLAYER1
    C_PLAYER2 = pieces.C_PLAYER2
    NEUTRAL = pieces.NEUTRAL

    '''
    valid_moves     - All the valid moves in the current board. Essentially
                    the list of empty cells.
    done            - Boolean value for the game being done or not. If done,
                    there must be a winner as Hex is a no-draw game.
    BOARD           - Game board in x by y dimension
    BOARD_SIZE      - Size of the board
    '''

    def __init__(self, BOARD_SIZE=[3, 3], BOARD=None, 
                 verbose=True, legality_check=False,
                 early_w_p1=False, early_w_p2=False, h=0,
                 h_player=None):
        '''
        Initializing a board. 

        args:
            BOARD_SIZE  - Size of the board, initially set to 3 by 3. [r, c]
            BOARD       - Predesigned board. An array of size r x c
        '''
        self.num_rows = BOARD_SIZE[0]
        self.num_cols = BOARD_SIZE[1]
        self.num_cells = self.num_rows * self.num_cols

        # to print game as a history
        self.game_history = [self.NEUTRAL] * self.num_cells
        self.cur_move_num = 1

        if BOARD:
            self.BOARD = BOARD
            # add check board_size
            # change valid moves to empty cells
            self.valid_moves = set(range(self.num_cells))
        else:
            self.BOARD = [self.NEUTRAL] * self.num_cells
            self.valid_moves = set(range(self.num_cells))
        self.done = False
        self.verbose = verbose

        self.legality_check = legality_check
        self.early_w_p1 = early_w_p1
        self.early_w_p2 = early_w_p2
        self.h = h
        self.h_player = h_player

        self.CHECK = False
 
    def step(self, color, action):
        '''
        Classic method to take a step, or make a move in the game. (Playing a stone
        on the board)

        args:
            color   - The color of the stone for the move being made.
            action  - The board position that the stone will be tried to place on.

        returns:
            Format >> [BOARD, done, result, reward]

            BOARD   - The current board position, state.
            done    - The truth value for if the game is over or not.
            result  - The winner of the game. If there is no winner yet (tie) returns
                    '=', otherwise returns the color that wins. The result returns 'f'
                    if the input given is invalid (If the move specified is illegal,
                    etc.).
            reward  - For the given player (color) if the current result is win the
                    reward is 1, if lose reward is -1 and 0 if it's a tie.
        '''
        if self.__placeStone(action, color): 
            result = self.game_status()
        else:
            if self.verbose:
                print('Valid moves are:', self.valid_moves)
            return 0, 0, 'f', 0
        
        if result == color:
            reward = 1
        elif result == '=':
            reward = 0
        else:
            reward = -1
        
        return self.BOARD, self.done, result, reward

    def rewind(self, action):
        '''
        Rewinding the action given; removing the move made on the given position
        and adding the new empty position to the valid_moves.

        args:
            action    - The position to empty. In the format [row, column]
        '''
        self.BOARD[action] = self.NEUTRAL
        self.valid_moves.append(action)

    def printBoard(self):
        '''
        Method for printing the board in a nice format.
        '''
        if not self.verbose:
            print("Verbose is off, output is not shown.")
            return
        if self.game_history.count(self.NEUTRAL) != self.BOARD.count(self.NEUTRAL):
            for x in range(len(self.game_history)):
                self.game_history[x] = self.BOARD[x] + '0' if self.BOARD[x] != self.NEUTRAL else self.NEUTRAL
        print(colors.C_PLAYER1 + '  ' + '{0: <3}'.format(self.C_PLAYER1) * self.num_cols + colors.ENDC)
        print(colors.BOLD + colors.C_PLAYER1 + ' ' + '-' * (self.num_cols * 3 +1) + colors.ENDC)
        for cell in range(self.num_cells):
            if cell % self.num_cols == 0: # first col
                print(colors.BOLD + colors.C_PLAYER2 + self.C_PLAYER2 + '\\ ' + colors.ENDC, end= '')
            if self.game_history[cell][0] == self.C_PLAYER1:
                clr = colors.C_PLAYER1
            elif self.game_history[cell][0] == self.C_PLAYER2:
                clr = colors.C_PLAYER2
            else:
                clr = colors.NEUTRAL
            print(clr + '{0: <3}'.format(self.game_history[cell]) + colors.ENDC, end='') 
            if cell % self.num_cols == self.num_cols-1: # last col
                print(colors.BOLD + colors.C_PLAYER2 + '\\' + self.C_PLAYER2 + '\n' + (' ' * (cell//self.num_cols)) + colors.ENDC, end = ' ')
        print(colors.BOLD + colors.C_PLAYER1 + '  ' + '-' * (self.num_cols * 3 +1) + colors.ENDC)        
        print(colors.BOLD + colors.C_PLAYER1 + ' ' * (self.num_rows+4) + '{0: <3}'.format(self.C_PLAYER1) * self.num_cols + colors.ENDC)

    def __checkEdge(self, color, node):
        '''
        Checks if the given node is the edge node for the given color.

        args:
            color   - The color of the player to check the edge for.
            node    - The location on the board we check if its the edge
                    for the given player or not.
        
        returns:
            format >> True/False

            True/False  - True if end of the board for given color 
                        False if not
        '''
        if (color == self.C_PLAYER2 and self.__find_col(node) == self.num_cols-1) or \
           (color == self.C_PLAYER1 and self.__find_row(node) == self.num_rows-1):
            return True
        return False

    def __find_row(self, node):
        return node // self.num_cols

    def __find_col(self, node):
        return node % self.num_cols

    def testConnections(self, cellToCheck):
        '''
        Testing the connections for a given cell.
        '''
        if self.verbose:
            print(str(cellToCheck), 'connections are', self.__cell_connections(cellToCheck))

    def __placeStone(self, cell, color):
        '''
        Placing a stone on the given board location.

        args:
            cell    - The location on the board to place the stone.
                    In the format [row, column]
            color   - The color of the stone.
        
        returns:
            True if the action was valid, and false otherwise.
        '''
        if self.BOARD[cell] != self.NEUTRAL:
            if self.verbose:
                print('Invalid Action Attempted')
            return False
        self.BOARD[cell] = color
        self.valid_moves.remove(cell)
        self.game_history[cell] = color + str(self.cur_move_num)                                
        self.cur_move_num += 1
        return True

    def __cell_connections(self, cell):
        '''
        Returns the neighbours of the given cell.

        args:
            cell    - The location on the board to check the neighboring cells for.
                    In the format [row, column]
        
        returns:
            format >> positions

            positions   - List of all the neighbouring cells to the cell.
                        Elements are in the format [row, column].
        '''
        row = self.__find_row(cell)
        col = self.__find_col(cell)

        positions = []
        if col + 1 < self.num_cols:
            positions.append(self.__pos_by_coord(row, col + 1))
        if col - 1 >= 0:
            positions.append(self.__pos_by_coord(row, col - 1))
        if row + 1 < self.num_rows:
            positions.append(self.__pos_by_coord(row + 1, col))
            if col - 1 >= 0:
                positions.append(self.__pos_by_coord(row + 1, col - 1))
        if row - 1 >= 0:
            positions.append(self.__pos_by_coord(row - 1, col))
            if col + 1 < self.num_cols:
                positions.append(self.__pos_by_coord(row - 1, col + 1))
        return positions
    
    def __pos_by_coord(self, r, c):
        return self.num_cols * r + c

    def game_status(self):
        '''
        Checks the game status by looking at the board and determining the winning player if any, returning
        the winner, or '=' if there is no winner.

        returns:
            format >> self.C_PLAYER2/self.C_PLAYER1/'='/'i'

            self.C_PLAYER2/self.C_PLAYER1/'=' - winner is white/black or its a tie ('=')
            'i'         - illegal game position
        '''
        # Check for legality
        if self.legality_check:
            if not self.check_legal():
                return 'i'

        # checking for black
        self.CHECK_BOARD = [False for _ in range(self.num_cells)] 
        for i in range(self.num_cols):
            pos = self.__pos_by_coord(0, i)
            if self.BOARD[pos] == self.C_PLAYER1:
                self.CHECK_BOARD[pos] = True
                self.__check_connections(self.__cell_connections(pos), self.C_PLAYER1)
                if self.done:
                    self.done = False
                    return self.C_PLAYER1
        # checking for white
        self.CHECK_BOARD = [False for _ in range(self.num_cells)]
        for i in range(self.num_rows):
            pos = self.__pos_by_coord(i, 0)
            if self.BOARD[pos] == self.C_PLAYER2:
                self.CHECK_BOARD[pos] = True
                self.__check_connections(self.__cell_connections(pos), self.C_PLAYER2)
                if self.done:
                    self.done = False
                    return self.C_PLAYER2
        return '=' 

    def __check_connections(self, connections, color):
        '''
        Checking and following all the given connections for the given color, and changes the done status
        to the winner if finds a connection to the edge of the board.

        args:
            connections - The connections to follow for searching the end edge.
            color       - The color to check the connections for
        '''
        for c in connections:
            if self.BOARD[c] == color and not self.CHECK_BOARD[c]:
                if self.__checkEdge(color, c):
                    self.done = True
                    return
                self.CHECK_BOARD[c] = True
                self.__check_connections(self.__cell_connections(c), color)

    def check_legal(self):
        # number of the stones are illegal
        first_Num = self.BOARD.count(self.C_PLAYER1)
        second_Num = self.BOARD.count(self.C_PLAYER2)
        if self.h_player == self.C_PLAYER1:
            first_Num += self.h
        else:
            second_Num += self.h
        if (first_Num + second_Num > self.num_cells) or \
           (first_Num - second_Num > 1 or second_Num > first_Num):
            return False
        
        # white wins with removing a white stone
        if self.early_w_p2 and self.check_early_win(self.C_PLAYER2):
            return False
        # black wins with removing a black stone
        if self.early_w_p1 and self.check_early_win(self.C_PLAYER1):
            return False

        return True
            
    def check_early_win(self, color):
        '''
        Returns false if any of the moves is not resulting with a win.

        The game should be win for any stone removed in color, to be
        a definite early win
        '''
        for c in range(len(self.BOARD)):
            if self.BOARD[c] != color:
                continue
            temp = self.BOARD[c]
            self.BOARD[c] = '.'; self.legality_check = False
            res = self.game_status()
            self.BOARD[c] = temp; self.legality_check = True
            if res != color:
                return False
        return True  

    def turn_info(self):
        '''
        Checks which players turn is it given the state and
        the number of hidden stones.
        
        Args:
            - state:    State to check the legality.
            - h:        Number of hidden stones.
        Returns:
            - C_PLAYER1/C_PLAYER2   Player whose turn it is.
        '''
        count_1 = self.BOARD.count(self.C_PLAYER1)
        count_2 = self.BOARD.count(self.C_PLAYER2)
        if self.h_player == self.C_PLAYER1:
            count_1 += self.h
        elif self.h_player == self.C_PLAYER2:
            count_2 += self.h

        if count_1 <= count_2:
            return self.C_PLAYER1
        else:
            return self.C_PLAYER2

def customBoard_print(board, num_cols, num_rows):
    '''
    Method for printing the board in a nice format.
    '''
    num_cells = num_cols * num_rows
    print(colors.C_PLAYER1 + '  ' + '{0: <3}'.format(pieces.C_PLAYER1) * num_cols + colors.ENDC)
    print(colors.BOLD + colors.C_PLAYER1 + ' ' + '-' * (num_cols * 3 +1) + colors.ENDC)
    for cell in range(num_cells):
        if cell % num_cols == 0: # first col
            print(colors.BOLD + colors.C_PLAYER2 + pieces.C_PLAYER2 + '\ ' + colors.ENDC, end= '')
        if board[cell] == pieces.C_PLAYER1:
            clr = colors.C_PLAYER1
        elif board[cell] == pieces.C_PLAYER2:
            clr = colors.C_PLAYER2
        else:
            clr = colors.NEUTRAL
        print(clr + '{0: <3}'.format(board[cell]) + colors.ENDC, end='') 
        if cell % num_cols == num_cols-1: # last col
            print(colors.BOLD + colors.C_PLAYER2 + '\\' + pieces.C_PLAYER2 + '\n' + (' ' * (cell//num_cols)) + colors.ENDC, end = ' ')
    print(colors.BOLD + colors.C_PLAYER1 + '  ' + '-' * (num_cols * 3 +1) + colors.ENDC)        
    print(colors.BOLD + colors.C_PLAYER1 + ' ' * (num_rows+4) + '{0: <3}'.format(pieces.C_PLAYER1) * num_cols + colors.ENDC)

def print_init_board(num_cols, num_rows):
    '''
    Print the board numbers
    '''
    num_cells = num_cols * num_rows
    print(colors.C_PLAYER1 + '  ' + '{0: <3}'.format(pieces.C_PLAYER1) * num_cols + colors.ENDC)
    print(colors.BOLD + colors.C_PLAYER1 + ' ' + '-' * (num_cols * 3 +1) + colors.ENDC)
    for cell in range(num_cells):
        if cell % num_cols == 0: # first col
            print(colors.BOLD + colors.C_PLAYER2 + pieces.C_PLAYER2 + '\ ' + colors.ENDC, end= '')
        print(colors.NEUTRAL + '{0: <3}'.format(cell) + colors.ENDC, end='') 
        if cell % num_cols == num_cols-1: # last col
            print(colors.BOLD + colors.C_PLAYER2 + '\\' + pieces.C_PLAYER2 + '\n' + (' ' * (cell//num_cols)) + colors.ENDC, end = ' ')
    print(colors.BOLD + colors.C_PLAYER1 + '  ' + '-' * (num_cols * 3 +1) + colors.ENDC)        
    print(colors.BOLD + colors.C_PLAYER1 + ' ' * (num_rows+4) + '{0: <3}'.format(pieces.C_PLAYER1) * num_cols + colors.ENDC)