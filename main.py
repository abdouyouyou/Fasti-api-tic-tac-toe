from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from random import randint
from datetime import datetime
from asyncio import sleep,create_task
from contextlib import asynccontextmanager
class Move(BaseModel):
    gameid:int
    xposition:int
    yposition:int
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
        
async def cleanup():
    while True:
        pop=[]
        print("started cleaning")
        for gameid,game in games.items():
            if game.Status=="Finished":
                games.pop(gameid)
            else:
                diff =datetime.now()-game.lastMove 
                if diff.seconds>40:
                    pop.append(gameid)
        for gameid in pop:
            games.pop(gameid)
        print("done cleaning")
        await sleep(60) 

@asynccontextmanager
async def lifespan(app:FastAPI):
    task = create_task(cleanup())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)



games:dict[int,Game]
games={}
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

@app.get('/start')
def start(): 
    gameid=randint(0,999999)
    game=Game()
    games[gameid]=game
    return {"Game":"Started",
            "Gameid":gameid}

@app.post("/playmove")
def playmove(move:Move):
    xposition = move.xposition
    yposition = move.yposition
    try:
        game=games[move.gameid]
        game.lastMove=datetime.now()
        if game.Board[xposition][yposition]!='':
            raise HTTPException(404,"This position is already played try another one")
        else:
            game.Board[xposition][yposition]='X'
            eval = evaluate(game)
            if eval =='X':
                game.Status="Finished"
                return {"Gameid":move.gameid,
                        "Game":"X won",
                        "Board":game.Board}
            while(1):
                xpos = randint(0,2)
                ypos = randint(0,2)
                if game.Board[xpos][ypos]=='':
                    game.Board[xpos][ypos]='O'
                    break
            eval=evaluate(game)
            if eval=='O':
                game.Status="Finished"
                return {"Gameid":move.gameid,
                        "Game":"O won",
                        "Board":game.Board}
            return {"Gameid":move.gameid,
                        "Game":"Still going",
                        "Board":game.Board}
    except KeyError :
        raise HTTPException(404,"This Game Either expired or is finished please start a new one by accessing the /start path :)")

@app.get("/getall")
def getall():
    return{
        "games":list(games.keys())
    }

