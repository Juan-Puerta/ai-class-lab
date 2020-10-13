import sys
import math
import functools
import datetime


PROFUNDIDAD_MAX = 3
ALPHA = -100000
BETA = 100000

def flatten_boxes(boxes):
    boxDef = []
    num = int(math.pow(len(boxes),1/2))
    for i,box in enumerate(boxes):
      a = int(box[0][1])
      b = box[1]
      if a!=1:
        b = b.replace('B','')
      if (i+1)>len(boxes)-num:
        for n in b:
            boxDef.append(f'{boxes[i][0]} {n}')
        continue
      b = b.replace('R','')
      for n in b:
            boxDef.append(f'{boxes[i][0]} {n}')

    return boxDef

def remove_move(boxes, move):
    move_box, move_side = move
    clone = boxes[:]

    for i, box in enumerate(clone):
        if box[0] == move_box:
            new_sides = box[1].replace(move_side, '')
            clone[i] = (box[0], new_sides) if new_sides != '' else None
            break

    nonone = list(filter(lambda b: not (b is None), clone))

    return nonone

def is_candidate_closed_by(box, move):
    move_box, move_side = move.split(' ')

    opposites = {
        'T': 'B',
        'B': 'T',
        'L': 'R',
        'R': 'L'
    }

    if box[0] == move_box and box[1] == move_side: # closes box
        return True
    if box[0] != move_box and box[1] == opposites[move_side] and move_box[0] == box[0][0]: # closes same cloumn
        return True
    elif box[0] != move_box and box[1] == opposites[move_side] and move_box[1] == box[0][1]: # closes same row
        return True

    return False

def closed_boxes(boxes, move):
    candidates = list(filter(lambda b: len(b[1]) == 1, boxes))
    closed = list(filter(lambda b: is_candidate_closed_by(b, move), candidates))

    return len(closed)

    # boxes [('A1', 'LTRB'), ('A2', 'LTRB'), ('B1', 'LTRB'), ('B2', 'LTRB')] - primera optimizacion, eliminar jugadas repetidas
def minimax(profundidad, alpha, beta, boxes, max_turn, max_score, min_score):
    if len(boxes) == 0 or profundidad == 0: # segunda optimizacion, cortar en profundidad y evaluar
        return max_score - min_score

    if max_turn:
        max_eval = alpha
        children =  flatten_boxes(boxes)
        for move in children:
            new_moves = remove_move(boxes, move)
            new_max_score = max_score + closed_boxes(boxes, move) # tercera optimizacion, usar numero de cajas cerradas para ordenar movimientos
            rating = minimax(profundidad-1, alpha, beta,new_moves, not max_turn, new_max_score, min_score)
            max_eval = max(rating, max_eval) # cuarta optimizacion, usar poda alfa-beta

            alpha = max(alpha, rating)
            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = beta
        children =  flatten_boxes(boxes)
        for move in children:
            new_moves = remove_move(boxes, move)
            new_min_score = min_score + closed_boxes(boxes, move)
            rating = minimax(profundidad-1, alpha, beta, new_moves, not max_turn, max_score, new_min_score)
            min_eval = min(rating, min_eval)

            beta = min(beta, rating)
            if beta <= alpha:
                break

        return min_eval

def move(boxes, player_score, opponent_score):
  max_eval = -1000
  children =  flatten_boxes(boxes)
  best_move = None
  for move in children:
      new_moves = remove_move(boxes, move)
      new_max_score = player_score + closed_boxes(boxes, move)
      #minimax(profundidad, alpha, beta, boxes, max_turn, max_score, min_score):
      rating = minimax(PROFUNDIDAD_MAX,ALPHA,BETA,new_moves, True, new_max_score, opponent_score)
      if rating > max_eval:
        max_eval = rating
        best_move = move

  return best_move

# game loop
while True:
    player_score, opponent_score = [int(i) for i in input().split()]

    boxes = []
    for i in range(int(input())):
        boxes.append(input())

    print(f'{move(boxes, player_score, opponent_score)} MSG {boxes}')


#start = datetime.datetime.now()
#minimax(PROFUNDIDAD_MAX,ALPHA,BETA,[('A1', 'LTRB'), ('A2', 'LTRB')], True, 0, 0)
#end = datetime.datetime.now()
#print((end-start).total_seconds()*1000)