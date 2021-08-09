from chess import ChessGame, WindowManager

chess = ChessGame()
window = WindowManager(800, 800)

chess.set_square_size(window.square_size)
# chess.load_fenstring("8/5p2/8/5P2/8/8/3p4/4K3")
# chess.load_fenstring('8/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
chess.load_fenstring()

while chess.running:
    window.poll_events(chess)
    window.render_window(chess.board)
