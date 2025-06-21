import tkinter as tk
from copy import deepcopy

class ChessGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("شطرنج حرفه‌ای با Tkinter")
        self.root.geometry("650x720")
        self.root.resizable(False, False)

        # فریم صفحه شطرنج
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        # تعریف رنگ‌ها برای خانه‌ها
        self.color_light = "#EEEED2"
        self.color_dark = "#769656"

        # نگهداری خانه‌ها و مهره‌ها
        self.tiles = {}
        self.selected = None  # خانه انتخاب شده (برای حرکت)
        self.turn = 'w'       # نوبت سفید ('w') یا سیاه ('b')
        self.move_log = []    # ثبت حرکات

        # وضعیت بازی (ادامه، مات، تساوی)
        self.game_over = False

        # تعریف صفحه شطرنج با آرایه ۸x۸ و مهره‌ها
        self.board = self.init_board()

        # کاراکترهای مهره‌ها برای نمایش در UI
        self.piece_symbols = {
            'wp': '♙', 'wr': '♖', 'wn': '♘', 'wb': '♗', 'wq': '♕', 'wk': '♔',
            'bp': '♟', 'br': '♜', 'bn': '♞', 'bb': '♝', 'bq': '♛', 'bk': '♚',
            '--': ''
        }

        # ساختار صفحه UI
        self.create_board_ui()

        # برچسب وضعیت نوبت یا پایان بازی
        self.status_label = tk.Label(self.root, text="نوبت سفید", font=("Arial", 20))
        self.status_label.pack(pady=10)

        self.update_board_ui()

        self.root.mainloop()

    def init_board(self):
        # تنظیم موقعیت شروع مهره‌ها
        return [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp'] * 8,
            ['--'] * 8,
            ['--'] * 8,
            ['--'] * 8,
            ['--'] * 8,
            ['wp'] * 8,
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]

    def create_board_ui(self):
        # ساخت خانه‌ها با رنگ و bind کلیک
        for r in range(8):
            for c in range(8):
                frame = tk.Frame(self.board_frame, width=80, height=80)
                frame.grid(row=r, column=c)
                color = self.color_light if (r + c) % 2 == 0 else self.color_dark
                label = tk.Label(frame, bg=color, font=("Arial", 48))
                label.pack(expand=True, fill='both')
                label.bind("<Button-1>", lambda e, row=r, col=c: self.tile_clicked(row, col))
                self.tiles[(r, c)] = label

    def update_board_ui(self):
        # بروزرسانی مهره‌ها و رنگ خانه‌ها
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                self.tiles[(r, c)].config(text=self.piece_symbols[piece])
                # رنگ خانه‌ها دوباره ست شود (در صورت هایلایت)
                color = self.color_light if (r + c) % 2 == 0 else self.color_dark
                self.tiles[(r, c)].config(bg=color)
        self.highlight_selected()
        self.update_status()

    def highlight_selected(self):
        # رنگ خانه انتخاب شده و خانه‌های قابل حرکت
        if self.selected:
            r, c = self.selected
            self.tiles[(r, c)].config(bg="yellow")
            moves = self.get_legal_moves(r, c)
            for (mr, mc) in moves:
                self.tiles[(mr, mc)].config(bg="lightblue")

    def update_status(self):
        # بروزرسانی متن وضعیت نوبت یا پایان بازی
        if self.game_over:
            if self.is_checkmate(self.turn):
                winner = "سیاه" if self.turn == 'w' else "سفید"
                self.status_label.config(text=f"مات! برنده: {winner}")
            else:
                self.status_label.config(text="تساوی!")
        else:
            player = "سفید" if self.turn == 'w' else "سیاه"
            self.status_label.config(text=f"نوبت {player}")

    def tile_clicked(self, r, c):
        if self.game_over:
            return
        piece = self.board[r][c]

        if self.selected:
            # اگر خانه انتخاب شده و خانه جدید کلیک شده است
            if (r, c) == self.selected:
                # کلیک روی خانه انتخاب شده: لغو انتخاب
                self.selected = None
                self.update_board_ui()
                return
            if self.is_legal_move(self.selected, (r, c)):
                # اگر حرکت قانونی بود، حرکت انجام شود
                self.make_move(self.selected, (r, c))
                self.selected = None
                self.update_board_ui()
                self.switch_turn()
                self.check_game_over()
            else:
                # اگر حرکت غیرقانونی بود، اگر مهره خانه جدید متعلق به نوبت بود انتخاب شود
                if piece != '--' and piece[0] == self.turn:
                    self.selected = (r, c)
                    self.update_board_ui()
        else:
            # اگر خانه انتخاب نشده، اگر مهره متعلق به نوبت بود انتخاب شود
            if piece != '--' and piece[0] == self.turn:
                self.selected = (r, c)
                self.update_board_ui()

    def switch_turn(self):
        # تغییر نوبت
        self.turn = 'b' if self.turn == 'w' else 'w'

    def make_move(self, start, end):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        self.board[r2][c2] = piece
        self.board[r1][c1] = '--'
        self.move_log.append((start, end, piece))

    def is_legal_move(self, start, end):
        # بررسی قانونی بودن حرکت
        legal_moves = self.get_legal_moves(*start)
        return end in legal_moves

    def get_legal_moves(self, r, c):
        piece = self.board[r][c]
        if piece == '--':
            return []
        color = piece[0]
        p_type = piece[1]

        moves = []
        if p_type == 'p':
            moves = self.pawn_moves(r, c, color)
        elif p_type == 'r':
            moves = self.sliding_moves(r, c, color, [(1,0), (-1,0), (0,1), (0,-1)])
        elif p_type == 'n':
            moves = self.knight_moves(r, c, color)
        elif p_type == 'b':
            moves = self.sliding_moves(r, c, color, [(1,1), (1,-1), (-1,1), (-1,-1)])
        elif p_type == 'q':
            moves = self.sliding_moves(r, c, color, [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)])
        elif p_type == 'k':
            moves = self.king_moves(r, c, color)
        else:
            moves = []

        # فیلتر کردن حرکت‌ها که موجب چک نشدن شاه خودی شوند
        legal_filtered = []
        for move in moves:
            temp_board = deepcopy(self.board)
            sr, sc = r, c
            er, ec = move
            temp_board[er][ec] = temp_board[sr][sc]
            temp_board[sr][sc] = '--'
            if not self.is_in_check(color, temp_board):
                legal_filtered.append(move)

        return legal_filtered

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def pawn_moves(self, r, c, color):
        moves = []
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1

        # حرکت مستقیم جلو
        if self.in_bounds(r + direction, c) and self.board[r + direction][c] == '--':
            moves.append((r + direction, c))
            # حرکت دو خانه جلو در شروع بازی
            if r == start_row and self.board[r + 2 * direction][c] == '--':
                moves.append((r + 2 * direction, c))

        # ضربه زدن قطری
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if self.in_bounds(nr, nc):
                target = self.board[nr][nc]
                if target != '--' and target[0] != color:
                    moves.append((nr, nc))

        # (پروموشن، en passant و ...) اضافه نشده است

        return moves

    def sliding_moves(self, r, c, color, directions):
        moves = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                target = self.board[nr][nc]
                if target == '--':
                    moves.append((nr, nc))
                else:
                    if target[0] != color:
                        moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return moves

    def knight_moves(self, r, c, color):
        moves = []
        steps = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                target = self.board[nr][nc]
                if target == '--' or target[0] != color:
                    moves.append((nr, nc))
        return moves

    def king_moves(self, r, c, color):
        moves = []
        steps = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                target = self.board[nr][nc]
                if target == '--' or target[0] != color:
                    moves.append((nr, nc))
        # (کستلینگ اضافه نشده)
        return moves

    def find_king(self, color, board=None):
        if board is None:
            board = self.board
        for r in range(8):
            for c in range(8):
                if board[r][c] == color + 'k':
                    return (r, c)
        return None

    def is_in_check(self, color, board=None):
        if board is None:
            board = self.board
        king_pos = self.find_king(color, board)
        if king_pos is None:
            return False
        enemy_color = 'b' if color == 'w' else 'w'

        # بررسی اینکه آیا شاه در دسترس حرکت مهره‌های حریف هست
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != '--' and piece[0] == enemy_color:
                    moves = self.get_raw_moves(r, c, board)
                    if king_pos in moves:
                        return True
        return False

    def get_raw_moves(self, r, c, board):
        # دریافت حرکت‌های خام بدون چک کردن چک (برای محاسبه چک)
        piece = board[r][c]
        if piece == '--':
            return []
        color = piece[0]
        p_type = piece[1]

        moves = []
        if p_type == 'p':
            moves = self.raw_pawn_moves(r, c, color, board)
        elif p_type == 'r':
            moves = self.raw_sliding_moves(r, c, color, [(1,0), (-1,0), (0,1), (0,-1)], board)
        elif p_type == 'n':
            moves = self.raw_knight_moves(r, c, color, board)
        elif p_type == 'b':
            moves = self.raw_sliding_moves(r, c, color, [(1,1), (1,-1), (-1,1), (-1,-1)], board)
        elif p_type == 'q':
            moves = self.raw_sliding_moves(r, c, color, [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)], board)
        elif p_type == 'k':
            moves = self.raw_king_moves(r, c, color, board)
        return moves

    def raw_pawn_moves(self, r, c, color, board):
        moves = []
        direction = -1 if color == 'w' else 1
        # حرکت مستقیم یک خانه بدون توجه به چک
        if self.in_bounds(r + direction, c) and board[r + direction][c] == '--':
            moves.append((r + direction, c))
        # ضربه قطری
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if self.in_bounds(nr, nc):
                target = board[nr][nc]
                if target != '--' and target[0] != color:
                    moves.append((nr, nc))
        return moves

    def raw_sliding_moves(self, r, c, color, directions, board):
        moves = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                target = board[nr][nc]
                if target == '--':
                    moves.append((nr, nc))
                else:
                    if target[0] != color:
                        moves.append((nr, nc))
                    break
                nr += dr
                nc += dc
        return moves

    def raw_knight_moves(self, r, c, color, board):
        moves = []
        steps = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                target = board[nr][nc]
                if target == '--' or target[0] != color:
                    moves.append((nr, nc))
        return moves

    def raw_king_moves(self, r, c, color, board):
        moves = []
        steps = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                target = board[nr][nc]
                if target == '--' or target[0] != color:
                    moves.append((nr, nc))
        return moves

    def is_checkmate(self, color):
        # چک کردن اگر شاه در چک است و هیچ حرکت قانونی ندارد => مات
        if not self.is_in_check(color):
            return False
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != '--' and piece[0] == color:
                    if self.get_legal_moves(r, c):
                        return False
        return True

    def is_stalemate(self, color):
        # تساوی وقتی که شاه در چک نیست ولی حرکت قانونی ندارد
        if self.is_in_check(color):
            return False
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != '--' and piece[0] == color:
                    if self.get_legal_moves(r, c):
                        return False
        return True

    def check_game_over(self):
        # بررسی پایان بازی
        if self.is_checkmate(self.turn):
            self.game_over = True
        elif self.is_stalemate(self.turn):
            self.game_over = True

if __name__ == "__main__":
    ChessGame()
