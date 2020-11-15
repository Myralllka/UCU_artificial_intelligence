import random
import operator
from libcheckers.enum import PieceClass, Player, GameOverReason

def pick_next_move(board, player):
    return find_best_move(board, player, board.owner, 4, float("-inf"), float('inf'))[0]


def heuristic_evaluation(board, maximizing_player, score, regular_value=1, queens_value=5):
    for owner, piece_class in zip(board.owner, board.piece_class):
        if owner == maximizing_player:
            score += regular_value if piece_class == PieceClass.MAN else queens_value
        elif owner is not None:
            score -= regular_value if piece_class == PieceClass.MAN else queens_value
    return score


def find_best_move(board, curr_player, maximizing_player, depth, alpha, beta):
    game_over_reason = board.check_game_over(curr_player)
    if game_over_reason is not None:
        if (game_over_reason == GameOverReason.DRAW):
            return None, 0
        elif (maximizing_player == Player.WHITE and game_over_reason == GameOverReason.WHITE_WON) or (
                maximizing_player == Player.BLACK and game_over_reason == GameOverReason.BLACK_WON):
            return None, float("inf")
        else:
            return None, float("-inf")
    else:
        if depth != 0:
            available_moves, best_move = board.get_available_moves(curr_player), None
            next_player = Player.WHITE if curr_player == Player.BLACK else Player.BLACK
            if (curr_player == maximizing_player):
                score = float("-inf")
                op = operator.ge
            else:
                score = float("inf")
                op = operator.lt
            for move in available_moves:
                tmp_board = move.apply(board)
                tmp_score = find_best_move(tmp_board, next_player, maximizing_player, depth - 1, alpha, beta)[1]
                if op(tmp_score, score):
                    score, best_move = tmp_score, move
                alpha = min(alpha, score)
                if alpha >= beta:
                    break
            return best_move, score
        else:
            return None, heuristic_evaluation(board, maximizing_player, 0)
