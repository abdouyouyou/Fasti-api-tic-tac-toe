from pydantic import BaseModel,Field
class Move(BaseModel):
    gameid:int
    xposition:int
    yposition:int