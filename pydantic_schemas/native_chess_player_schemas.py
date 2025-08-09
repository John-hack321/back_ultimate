from pydantic import BaseModel
import enum

# for now lets just create the enum types we will go to validation later on

class GameVerdict(enum.IntEnum):
    win = 1
    loss = 2
    draw = 0
    stalemate = 3
    checkmate = 4