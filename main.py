from chess import ChessGame

chess = ChessGame()

# chess.load_fenstring("8/8/8/8/8/8/8/3PK3")
# chess.load_fenstring('8/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
chess.load_fenstring()


while chess.running:
    chess.poll_events()

    if chess.move_made:
        chess.gen_legal_moves()
        chess.current_color *= -1

        chess.move_made = False

    chess.render_window()