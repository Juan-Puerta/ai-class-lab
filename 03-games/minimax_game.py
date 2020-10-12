import functools

def flatten_boxes(boxes):
    return functools.reduce(
        lambda m, box: m + list(map(lambda side: f'{box[0]} {side}',list(box[1])))
    , boxes, [])

def remove_move(boxes, move):
    move_box, move_side = move.split(' ')
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
def minimax(boxes, max_turn, max_score, min_score):
    if len(boxes) == 0: # segunda optimizacion, cortar en profundidad y evaluar
        return max_score - min_score

    if max_turn:
        max_eval = -1000
        children =  flatten_boxes(boxes)
        for move in children:
            new_moves = remove_move(boxes, move)
            new_max_score = max_score + closed_boxes(boxes, move) # tercera optimizacion, usar numero de cajas cerradas para ordenar movimientos
            rating = minimax(new_moves, not max_turn, new_max_score, min_score)
            max_eval = max(rating, max_eval) # cuarta optimizacion, usar poda alfa-beta
        return max_eval
    else:
        min_eval = 1000
        children =  flatten_boxes(boxes)
        for move in children:
            new_moves = remove_move(boxes, move)
            new_min_score = min_score + closed_boxes(boxes, move)
            rating = minimax(new_moves, not max_turn, max_score, new_min_score)
            min_eval = min(rating, min_eval)
        return min_eval
minimax([('A1', 'LTRB'), ('A2', 'LTRB')], True, 0, 0)