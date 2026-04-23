from datetime import datetime
class Game():
    Board:list[list[str]]
    Status:bool
    lastMove:datetime
    def __init__(self):
        self.Board= [['','',''],
         ['','',''],
         ['','','']
         ]
        self.Status="Started"
        self.lastMove=datetime.now()

def row_win(player,game:Game):
    return any(all(cell == player for cell in row)for row in game.Board)
def col_win(player,game:Game):
    return any(all(row[i]==player for row in game.Board)for i in range(3))
def diag_win(player,game:Game):
    return all(game.Board[i][i]==player for i in range(3))or all(game.Board[i][2-i]==player for i in range(3))
def evaluate(game):
    #maybe return somethin else ?
    X = row_win('X',game) or col_win('X',game) or diag_win('X',game)
    O = row_win('O',game) or col_win('O',game) or diag_win('O',game)
    if X : 
        return "X"
    elif O :
        return "O"
    else : 
        return -1 
