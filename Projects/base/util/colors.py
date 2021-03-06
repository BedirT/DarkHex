class colors:
    TITLE = '\033[35m'
    MIDTEXT ='\033[32m'
    QUESTIONS = '\033[94m'
    C_PLAYER1 = '\033[96m'
    C_PLAYER2 = '\033[35m'
    NEUTRAL = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WARNING = '\033[31m'

class pieces:
    C_PLAYER1 = 'B'
    C_PLAYER2 = 'W'
    NEUTRAL = '.'

    # open_spiel states.
    kEmpty = '.'
    kWhite = 'o'
    kWhiteWin = 'O'
    kBlack = 'x'
    kBlackWin = 'X'
    kWhiteWest = 'p'
    kWhiteEast = 'q'
    kBlackNorth = 'y'
    kBlackSouth = 'z'