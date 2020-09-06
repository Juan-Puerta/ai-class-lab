from tic_tac_toe import TicTacToeGame

def play():
  game = TicTacToeGame()
  termino = False
  while not termino:
    game.play() 
    termino = game.is_over()
    game.print()

  game.print_result()

if __name__ == "__main__":
  play()
