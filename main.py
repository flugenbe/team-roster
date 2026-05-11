from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Player(BaseModel):
    number: int
    name: str
    position: str
    age: int
    isActive: bool = False

players = []

@app.post("/players")
def create_player(player: Player):
    if any(p.number == player.number for p in players):
        raise HTTPException(status_code=404, detail="That number is not available")
    else:
        players.append(player)
        return players

@app.get("/players", response_model=list[Player])
def list_players():
    return players

@app.get("/players/{player_number}", response_model=Player)
def get_player(player_number: int):
    try:
        player_id = players.number().index(player_number)
        return players[player_id]
    except ValueError:
        raise HTTPException(status_code=404, detail="Player not found")
