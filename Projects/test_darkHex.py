from Projects.base.game.darkHex import DarkHex
from Projects.base.game.hex import print_init_board
from Projects.base.agent.RandomAgent import RandomAgent
from Projects.base.agent.SetPolicyAgent import FixedPolicyAgent_wTree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose_player", "-vp", action="store_true", 
                    help="Turn on outputs for the Fixed Policy player.", default=False)
args = parser.parse_args()

game = DarkHex(BOARD_SIZE=[3,4])
result = '='

actor1 = FixedPolicyAgent_wTree(game.C_PLAYER2, game.valid_moves)
actor2 = RandomAgent(game.C_PLAYER1)

i = 0
print('Player 1 (W) is played by the FixedPolicyAgent\n\
Player 2 (B) is you, please make a move according\n\
to the given table indexes. For 3x4 board here\n\
is the board indexes;\n')
print_init_board(num_cols=game.num_cols, num_rows=game.num_rows)

while result == '=':
    s = True
    if i % 2 == 0:
        result = 'f'
        if not args.verbose_player:
            game.verbose = False
        while result == 'f':
            action = actor1.step(observation=game.BOARDS[game.C_PLAYER2], success=s)
            board, done, result, reward = game.step(game.C_PLAYER2, action)
            s = False
        if args.verbose_player:    
            game.print_information_set(game.C_PLAYER2)
    else:
        result = 'f'
        game.verbose = True
        while result == 'f':
            try:
                action = int(input('move: ').strip())
                board, done, result, reward = game.step(game.C_PLAYER1, action)
            except KeyboardInterrupt:
                exit()
            except:
                print("Please enter a valid input, the format should be an int. i.e. 3. Valid indexes shown as in the board below;")
                print_init_board(num_cols=game.num_cols, num_rows=game.num_rows,
                                 p1=game.C_PLAYER1, p2=game.C_PLAYER2)
                continue
        game.print_information_set(game.C_PLAYER1)
    i+=1
game.verbose = True
print('\nGame is over, the winner is:', game.game_status())
print('Here is the end game referee board:')
game.printBoard()