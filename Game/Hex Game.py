import time
from collections import deque

# --- Constants ---
EMPTY = 0
PLAYER1 = 1   # X (top-to-bottom)
PLAYER2 = 2   # O (left-to-right)

NEIGHBORS = [(-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0)]

# ---------------- HexState ----------------
class HexState:
    def __init__(self, size, board=None, turn=PLAYER1):
        self.size = size
        if board is None:
            self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        else:
            self.board = [row[:] for row in board]
        self.turn = turn

    def copy(self):
        return HexState(self.size, self.board, self.turn)

    def get_legal_moves(self):
        moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == EMPTY:
                    moves.append((r, c))
        return moves

    def make_move(self, move):
        r, c = move
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            return self
        if self.board[r][c] != EMPTY:
            return self
        new_state = self.copy()
        new_state.board[r][c] = self.turn
        new_state.turn = PLAYER2 if self.turn == PLAYER1 else PLAYER1
        return new_state

    def winner(self):
        if self.check_win(PLAYER1):
            return PLAYER1
        if self.check_win(PLAYER2):
            return PLAYER2
        return None

    def is_terminal(self):
        return self.winner() is not None or len(self.get_legal_moves()) == 0

    def check_win(self, player):
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]
        stack = []
        if player == PLAYER1:  # top row to bottom
            for c in range(self.size):
                if self.board[0][c] == PLAYER1:
                    stack.append((0, c))
                    visited[0][c] = True
            while stack:
                r, c = stack.pop()
                if r == self.size - 1:
                    return True
                for dr, dc in NEIGHBORS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if not visited[nr][nc] and self.board[nr][nc] == PLAYER1:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
        else:  # left col to right col
            for r in range(self.size):
                if self.board[r][0] == PLAYER2:
                    stack.append((r, 0))
                    visited[r][0] = True
            while stack:
                r, c = stack.pop()
                if c == self.size - 1:
                    return True
                for dr, dc in NEIGHBORS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if not visited[nr][nc] and self.board[nr][nc] == PLAYER2:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
        return False

    # ------------ Pretty board (aligned) ------------
    def gameboard(self):
        n = self.size
        cell_w = 4
        row_label_w = 2
        base_indent = row_label_w

        # Header
        header = " " * base_indent + "".join(f"{c:>{cell_w}}" for c in range(n))
        print(header)

        for r in range(n):
            indent = " " * (2 * r)
            label = f"{r:>{row_label_w}}"
            cells = "".join(
                ("X" if self.board[r][c] == PLAYER1 else
                 "O" if self.board[r][c] == PLAYER2 else
                 ".").rjust(cell_w)
                for c in range(n)
            )
            print(indent + label + cells + "  O")
            print()

        bottom_indent = " " * (base_indent + 2 * (n - 1))
        bottom = bottom_indent + "".join(f"{'X':>{cell_w}}" for _ in range(n))
        print(bottom)
        print()

# ---------------- Evaluation ----------------
def shortest_path_length(state, player):
    n = state.size
    visited = [[False]*n for _ in range(n)]
    dist = [[float("inf")]*n for _ in range(n)]
    q = deque()

    if player == PLAYER1:  # top-to-bottom
        for c in range(n):
            if state.board[0][c] in (EMPTY, PLAYER1):
                q.append((0, c))
                dist[0][c] = 0
                visited[0][c] = True
    else:  # left-to-right
        for r in range(n):
            if state.board[r][0] in (EMPTY, PLAYER2):
                q.append((r, 0))
                dist[r][0] = 0
                visited[r][0] = True

    while q:
        r, c = q.popleft()
        for dr, dc in NEIGHBORS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if not visited[nr][nc] and state.board[nr][nc] in (EMPTY, player):
                    visited[nr][nc] = True
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

    best = float("inf")
    if player == PLAYER1:
        for c in range(n):
            best = min(best, dist[n-1][c])
    else:
        for r in range(n):
            best = min(best, dist[r][n-1])
    return best if best != float("inf") else n*n

def evaluate(state, player):
    opp = PLAYER1 if player == PLAYER2 else PLAYER2
    player_path = shortest_path_length(state, player)
    opp_path = shortest_path_length(state, opp)
    return opp_path - player_path

# ---------------- Minimax (with nodes + time) ----------------
def minimax_with_time(state, depth, player):
    nodes = [0]
    def rec(s, d, player):
        nodes[0] += 1
        if d == 0 or s.is_terminal():
            return evaluate(s, player), None
        best_move = None
        if s.turn == player:
            best_val = -10**9
            for m in s.get_legal_moves():
                child = s.make_move(m)
                val, _ = rec(child, d-1, player)
                if val > best_val:
                    best_val = val
                    best_move = m
            return best_val, best_move
        else:
            best_val = 10**9
            for m in s.get_legal_moves():
                child = s.make_move(m)
                val, _ = rec(child, d-1, player)
                if val < best_val:
                    best_val = val
                    best_move = m
            return best_val, best_move

    t0 = time.time()
    score, move = rec(state, depth, player)
    elapsed = time.time() - t0
    return score, move, elapsed, nodes[0]

# ---------------- Alpha-Beta (with nodes + time) ----------------
def alphabeta_with_time(state, depth, player):
    nodes = [0]
    def rec(s, d, alpha, beta, player):
        nodes[0] += 1
        if d == 0 or s.is_terminal():
            return evaluate(s, player), None
        best_move = None
        if s.turn == player:
            value = -10**9
            for m in s.get_legal_moves():
                child = s.make_move(m)
                val, _ = rec(child, d-1, alpha, beta, player)
                if val > value:
                    value = val
                    best_move = m
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = 10**9
            for m in s.get_legal_moves():
                child = s.make_move(m)
                val, _ = rec(child, d-1, alpha, beta, player)
                if val < value:
                    value = val
                    best_move = m
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move

    t0 = time.time()
    score, move = rec(state, depth, -10**9, 10**9, player)
    elapsed = time.time() - t0
    return score, move, elapsed, nodes[0]

# ---------------- Safe input ----------------
def safe_int(prompt, default):
    try:
        v = input(prompt).strip()
        if v == "":
            return default
        return int(v)
    except:
        return default

# ---------------- Modes ----------------
def human_vs_ai(algorithm):
    size = safe_int("Enter board size (e.g. 3): ", 3)
    depth = safe_int("Enter AI depth (1-3 recommended): ", 2)
    game = HexState(size)
    human = PLAYER1
    ai = PLAYER2
    total_mm_time = total_ab_time = 0.0
    total_mm_nodes = total_ab_nodes = 0

    while not game.is_terminal():
        game.gameboard()
        if game.turn == human:
            try:
                r,c = map(int, input("Your move (row col): ").split())
            except:
                print("Invalid input. Try again.")
                continue
            if (r,c) not in game.get_legal_moves():
                print("Illegal move. Pick an empty cell.")
                continue
            game = game.make_move((r,c))
        else:
            print("AI thinking...")
            if algorithm == "minimax":
                _, move, t, n = minimax_with_time(game, depth, ai)
                print(f"Minimax -> move: {move}, time:{t:.4f}s, nodes:{n}")
                total_mm_time += t
                total_mm_nodes += n
            else:
                _, move, t, n = alphabeta_with_time(game, depth, ai)
                print(f"Alpha-Beta -> move: {move}, time:{t:.4f}s, nodes:{n}")
                total_ab_time += t
                total_ab_nodes += n
            game = game.make_move(move)

    game.gameboard()
    winner = game.winner()
    print("You win!" if winner == human else "AI wins!")
    print("\n-- FINAL REPORT --")
    if algorithm == "minimax":
        print(f"Minimax total time: {total_mm_time:.4f}s, nodes: {total_mm_nodes}")
    else:
        print(f"Alpha-Beta total time: {total_ab_time:.4f}s, nodes: {total_ab_nodes}")
    print("-------------------\n")

def human_vs_both():
    size = safe_int("Enter board size (e.g. 3): ", 3)
    depth = safe_int("Enter AI depth (1-3 recommended): ", 2)
    game = HexState(size)
    human = PLAYER1
    ai = PLAYER2

    total_mm_time = total_ab_time = 0.0
    total_mm_nodes = total_ab_nodes = 0

    while not game.is_terminal():
        game.gameboard()
        if game.turn == human:
            try:
                r,c = map(int, input("Your move (row col): ").split())
            except:
                print("Invalid input. Try again.")
                continue
            if (r,c) not in game.get_legal_moves():
                print("Illegal move. Pick an empty cell.")
                continue
            game = game.make_move((r,c))
        else:
            print("AI thinking (both algorithms)...")
            score_mm, move_mm, t_mm, n_mm = minimax_with_time(game, depth, ai)
            score_ab, move_ab, t_ab, n_ab = alphabeta_with_time(game, depth, ai)

            print(f"Minimax -> move: {move_mm}, score:{score_mm}, time:{t_mm:.4f}s, nodes:{n_mm}")
            print(f"Alpha-Beta -> move: {move_ab}, score:{score_ab}, time:{t_ab:.4f}s, nodes:{n_ab}")
            print("Same move?:", move_mm == move_ab)

            total_mm_time += t_mm
            total_mm_nodes += n_mm
            total_ab_time += t_ab
            total_ab_nodes += n_ab

            move = move_ab
            print("AI chooses (Alpha-Beta):", move)
            game = game.make_move(move)

    game.gameboard()
    winner = game.winner()
    print("You win!" if winner == human else "AI wins!")

    print("\n===== FINAL COMPARISON REPORT =====")
    print(f"Minimax total time:     {total_mm_time:.4f}s   | total nodes: {total_mm_nodes}")
    print(f"Alpha-Beta total time:  {total_ab_time:.4f}s   | total nodes: {total_ab_nodes}")
    print(f"Combined total time:    {(total_mm_time + total_ab_time):.4f}s   | total nodes: {(total_mm_nodes + total_ab_nodes)}")
    print("===================================\n")

def ai_vs_ai():
    size = safe_int("Enter board size (e.g. 3): ", 3)
    depth = safe_int("Enter AI depth (1-3 recommended): ", 2)
    game = HexState(size)
    ai1 = PLAYER1   # Minimax
    ai2 = PLAYER2   # Alpha-Beta

    total_mm_time = total_ab_time = 0.0
    total_mm_nodes = total_ab_nodes = 0

    print("AI1 = Minimax (X)  vs  AI2 = Alpha-Beta (O)\n")
    while not game.is_terminal():
        game.gameboard()
        if game.turn == ai1:
            _, move, t, n = minimax_with_time(game, depth, ai1)
            print(f"AI1 (Minimax) -> {move}, time:{t:.4f}s, nodes:{n}")
            total_mm_time += t
            total_mm_nodes += n
        else:
            _, move, t, n = alphabeta_with_time(game, depth, ai2)
            print(f"AI2 (Alpha-Beta) -> {move}, time:{t:.4f}s, nodes:{n}")
            total_ab_time += t
            total_ab_nodes += n
        game = game.make_move(move)

    game.gameboard()
    winner = game.winner()
    if winner == ai1:
        print("AI1 (Minimax) wins!")
    elif winner == ai2:
        print("AI2 (Alpha-Beta) wins!")
    else:
        print("Draw / no winner.")

    print("\n===== AI vs AI REPORT =====")
    print(f"AI1 Minimax -> total time: {total_mm_time:.4f}s, nodes: {total_mm_nodes}")
    print(f"AI2 AlphaBeta -> total time: {total_ab_time:.4f}s, nodes: {total_ab_nodes}")
    if total_ab_time < total_mm_time:
        print("Analysis: Alpha-Beta was faster overall (pruned nodes).")
    else:
        print("Analysis: Minimax was faster in this run (rare).")
    print("===========================\n")

# ---------------- Main menu ----------------
def main_menu():
    while True:
        print("\n===== HEX GAME MENU =====")
        print("1. Play against Minimax")
        print("2. Play against Alpha-Beta")
        print("3. Play against BOTH (compare each AI turn & final report)")
        print("4. AI vs AI (Minimax vs Alpha-Beta)")
        print("5. Quit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            human_vs_ai("minimax")
        elif choice == "2":
            human_vs_ai("alphabeta")
        elif choice == "3":
            human_vs_both()
        elif choice == "4":
            ai_vs_ai()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
