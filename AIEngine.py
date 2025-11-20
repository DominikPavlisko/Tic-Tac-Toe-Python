class AIEngine:

    def __init__(self, ai_mark="O", human_mark="X"):
        self.ai = ai_mark
        self.human = human_mark

    def get_best_move(self, engine):
        best_score = float("-inf")
        best_move = None

        for (r, c) in engine.get_empty_cells():
            clone = engine.clone()
            clone.board[r][c] = self.ai
            clone.current_player = self.human

            score = self.minimax(clone, False)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    def minimax(self, engine, maximizing):
        winner = engine.check_winner()
        if winner == self.ai:
            return +1
        if winner == self.human:
            return -1
        if engine.is_draw():
            return 0

        if maximizing:
            best = float("-inf")
            for (r, c) in engine.get_empty_cells():
                clone = engine.clone()
                clone.board[r][c] = self.ai
                clone.current_player = self.human

                score = self.minimax(clone, False)
                best = max(best, score)
            return best

        else:
            best = float("inf")
            for (r, c) in engine.get_empty_cells():
                clone = engine.clone()
                clone.board[r][c] = self.human
                clone.current_player = self.ai

                score = self.minimax(clone, True)
                best = min(best, score)
            return best
