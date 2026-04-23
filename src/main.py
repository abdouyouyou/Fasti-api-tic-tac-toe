from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from random import randint
from datetime import datetime
from asyncio import sleep,create_task
from contextlib import asynccontextmanager
from game_logic import *
from schema import *

        
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

