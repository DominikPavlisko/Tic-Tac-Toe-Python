
AI_PLAYER = "O"
HUMAN_PLAYER = "X"


def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]


def is_winner(board, player):
    winning_positions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    return any(board[a] == board[b] == board[c] == player for a, b, c in winning_positions)


def is_draw(board):
    return " " not in board


def evaluate(board):
    if is_winner(board, AI_PLAYER):
        return 1
    if is_winner(board, HUMAN_PLAYER):
        return -1
    return 0


def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    if score != 0:
        return score
    if is_draw(board):
        return 0

    if is_maximizing:
        best_value = -9999
        for move in get_available_moves(board):
            board[move] = AI_PLAYER
            value = minimax(board, depth + 1, False)
            board[move] = " "
            best_value = max(best_value, value)
        return best_value

    else:
        best_value = 9999
        for move in get_available_moves(board):
            board[move] = HUMAN_PLAYER
            value = minimax(board, depth + 1, True)
            board[move] = " "
            best_value = min(best_value, value)
        return best_value


def get_best_move(board):
    best_score = -9999
    best_move = None

    for move in get_available_moves(board):
        board[move] = AI_PLAYER
        score = minimax(board, 0, False)
        board[move] = " "

        if score > best_score:
            best_score = score
            best_move = move

    return best_move