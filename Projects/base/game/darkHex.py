from copy import deepcopy

from Projects.base.game.hex import Hex

C_PLAYER1 = 'B'
C_PLAYER2 = 'W'

class DarkHex(Hex):

    def __init__(self, BOARD_SIZE=[3, 3], verbose=True,
                       custom_board_C_PLAYER1=[],
                       custom_board_C_PLAYER2=[]):
        '''
        Initializing a board. 

        args:
            BOARD_SIZE  - Size of the board, initially set to 3 by 3. [num_R, num_C]
        '''
        super().__init__(BOARD_SIZE=BOARD_SIZE, verbose=verbose)

        self.rev_color = {C_PLAYER2: C_PLAYER1, C_PLAYER1: C_PLAYER2}

        self.BOARDS = {C_PLAYER2: deepcopy(self.BOARD), C_PLAYER1: deepcopy(self.BOARD)}

        if custom_board_C_PLAYER1:
            self.BOARDS[C_PLAYER1] = custom_board_C_PLAYER1
        if custom_board_C_PLAYER2:
            self.BOARDS[C_PLAYER2] = custom_board_C_PLAYER2
        self.__set_board()
        self.num_moves = {C_PLAYER2: 0, C_PLAYER1: 0}
        self.num_opp_known = {C_PLAYER2: 0, C_PLAYER1: 0}

        self.valid_moves_colors = {C_PLAYER2: deepcopy(self.valid_moves), C_PLAYER1: deepcopy(self.valid_moves)}

    def rewind(self, action):
        '''
        Rewinding the action given; removing the move made on the given position
        and adding the new empty position to the valid_moves.

        args:
            action    - The position to empty. In the format [row, column]
        '''
        self.BOARD[action] = '.'
        self.valid_moves.append(action)

        self.BOARDS[C_PLAYER1][action] = '.'
        self.valid_moves_colors[C_PLAYER1].append(action)

        self.BOARDS[C_PLAYER2][action] = '.'
        self.valid_moves_colors[C_PLAYER2].append(action)

    def __set_board(self):
        for i, c in enumerate(self.BOARDS[C_PLAYER1]):
            if c == C_PLAYER1:
                self.BOARD[i] = c
        for i, c in enumerate(self.BOARDS[C_PLAYER2]):
            if c == C_PLAYER2:
                self.BOARD[i] = c

    def print_information_set(self, player):
        if not self.verbose:
            print("Verbose is off, output is not shown.")
            return
        self.printBoard_for_player(player)
        print('Number of hidden {} stones: {}'\
               .format(self.rev_color[player], \
                       self.totalHidden_for_player(player)))

    def totalHidden_for_player(self, player):
        return self.num_moves[self.rev_color[player]] \
               - self.num_opp_known[player]

    def printBoard_for_player(self, player):
        '''
        Method for printing the players visible board in a nice format.
        '''
        print('  ' + '{0: <3}'.format(C_PLAYER1) * self.num_cols)
        print(' ' + '-' * (self.num_cols * 3 +1))
        for cell in range(self.num_cells):
            if cell % self.num_cols == 0: # first col
                print('W\ ', end= '')
            print('{0: <3}'.format(self.BOARDS[player][cell]), end='') 
            if cell % self.num_cols == self.num_cols-1: # last col
                print('\W\n' + (' ' * (cell//self.num_cols)), end = ' ')
        print('  ' + '-' * (self.num_cols * 3 +1))        
        print(' ' * (self.num_rows+4) + '{0: <3}'.format(C_PLAYER1) * self.num_cols)

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
            return 0, 0, 'f', 0
        
        if result == color:
            reward = 1
        elif result == '=':
            reward = 0
        else:
            reward = -1
        
        return self.BOARD, self.done, result, reward

    def __placeStone(self, cell, color):
        '''
        Placing a stone on the given board location for the main board and 
        the board for player -color-. If the move is invalid (there is a
        stone already placed in the location provided) the function will
        return False, otherwise make the move and return True.

        args:
            cell    - The location on the board to place the stone.
                      int format
            color   - The color of the stone.
        
        returns:
            True if the action was valid, and false otherwise.
        '''
        if self.BOARDS[color][cell] != '.':
            if self.verbose:
                print('Invalid Move.')
                print('Valid moves are:', self.valid_moves_colors[color])
            return False
        if self.BOARD[cell] != '.':
            self.BOARDS[color][cell] = self.rev_color[color]
            self.valid_moves_colors[color].remove(cell)
            self.num_opp_known[color] += 1
            if self.verbose:
                print('This cell is taken.')
                print('Valid moves are:', self.valid_moves_colors[color])
                self.print_information_set(color)
            return False
        self.BOARD[cell] = color
        self.valid_moves.remove(cell)
        self.BOARDS[color][cell] = color
        self.valid_moves_colors[color].remove(cell)

        self.num_moves[color] += 1

        self.game_history[cell] = color + str(self.cur_move_num)
        self.cur_move_num += 1
        return True