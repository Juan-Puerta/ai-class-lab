import re
from random import *

_PLAYER = "player"
_MACHINE = "machine"

_PLAYER_SYMBOL = "x"
_MACHINE_SYMBOL = "o"

class TicTacToeGame():
  def __init__(self):
    self.board = [None] * 9
    self.turn = _PLAYER
    self.is_game_over = False
    self.winner = None
    self.listica = list(range(len(self.board)))

  def is_over(self): # TODO: Finish this function by adding checks for a winning game (rows, columns, diagonals)
    
    #Analizar Diagonales
    if(self.analizarGano(0,4,8)):
      return True
    elif(self.analizarGano(2,4,6)):
      return True
    #Analizar Verticales
    elif(self.analizarGano(0,3,6)):
      return True
    elif(self.analizarGano(1,4,7)):
      return True
    elif(self.analizarGano(2,5,8)):
      return True
    #Analizar Horizontales
    elif(self.analizarGano(0,1,2)):
      return True
    elif(self.analizarGano(3,4,5)):
      return True
    elif(self.analizarGano(6,7,8)):
      return True
    #Otros
    elif (self.board.count(None) == 0):
      return True
    else:
      return False

  def analizarGano(self, a, b, c):

    if((self.board[a] != None) and (self.board[b] != None) and (self.board[c] != None)):
      if(self.board[a] == self.board[b] == self.board[c]):

        self.is_game_over = True
        if(self.board[a] == _PLAYER_SYMBOL):
          self.winner = _PLAYER
        else:
          self.winner = _MACHINE
        return True

    else:

      return False


  def play(self):
    if self.turn == _PLAYER:
      if(self.winner is None):
        self.player_turn()
        self.turn = _MACHINE
    else:
      if(self.winner is None):
        self.machine_turn()
        self.turn = _PLAYER

  def player_choose_cell(self):
    print("Input empty cell bewtween 0 and 8")

    player_cell = input().strip()
    match = re.search("\d", player_cell)

    if not match:
      print("Input is not a number, please try again")

      return self.player_choose_cell()

    player_cell = int(player_cell)

    if(player_cell >= len(self.board) or player_cell <= -1):
      print("Choise a number within the range")
      return self.player_choose_cell()

    if self.board[player_cell] is not None:
      print("Cell is already taken, try again")

      return self.player_choose_cell()

    self.listica.remove(player_cell)
    return player_cell

  def player_turn(self):
    chosen_cell = self.player_choose_cell()

    self.board[chosen_cell] = _PLAYER_SYMBOL

  def machine_turn(self):
    # TODO: Implement this function to make the machine choose a random cell (use random module)
    # The result of this function should be that self.board now has one more random cell occupied
      n = choice(self.listica)
      self.listica.remove(n)
      self.board[n] = _MACHINE_SYMBOL

  def format_board(self):
    # TODO: Implement this function, it must be able to print the board in the following format:
    #  x|o| 
    #   | | 
    #   | | 
    tableroCadena = ''
    for x in range(0, len(self.board)):
      if((x+1) % 3 != 0):
        if(self.board[x] == None):
          tableroCadena = tableroCadena + ' |' 
        else:
          tableroCadena = tableroCadena + self.board[x] + '|'
      else:
        if(self.board[x] == None):
          tableroCadena = tableroCadena + ' ' + '\n'
        else:
          tableroCadena = tableroCadena + self.board[x] + '\n'
    return tableroCadena

  def print(self):
    print("Player turn:" if self.turn == _MACHINE else "Machine turn:")
    print(self.format_board())
    print()

  def print_result(self):
    # TODO: Implement this function in order to print the result based on the self.winner
    if (self.winner is None):
      self.winner = "Nadie"
    print("El ganador es " + self.winner)
