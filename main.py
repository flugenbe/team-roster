from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

class Player(BaseModel):
    number: int
    name: str
    position: str
    age: int
    is_active: bool = False

players = []

@app.post("/players")
def create_player(player: Player):
    if any(p.number == player.number for p in players):
        raise HTTPException(status_code=409, detail="That number is not available")
    elif player.number < 0:
        raise HTTPException(status_code=400, detail="Number cannot be negative")
    elif player.age < 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    else:
        players.append(player)
        return players

@app.get("/players", response_model=list[Player])
def list_players(active: bool | None = None):
    if active == None:
        return players
    return [p for p in players if p.is_active == active]

@app.get("/players/{player_number}", response_model=Player)
def get_player(player_number: int):
    match = next((p for p in players if p.number == player_number), None)
    if match == None:
        raise HTTPException(status_code=404, detail="Player not found")
    return match

@app.put("/players/{player_number}", response_model=Player)
def change_player_status(player_number: int,is_active: bool):
    match = next((p for p in players if p.number == player_number), None)
    if match == None:
        raise HTTPException(status_code=404, detail="Player not found")
    match.is_active=is_active
    return match

@app.delete("/players/{player_number}")
def delete_player(player_number: int):
    player_id = next((i for i, p in enumerate(players) if p.number == player_number), None)
    if player_id == None:
        raise HTTPException(status_code=404, detail="Player not found")
    players.pop(player_id)
    return {"number": player_number, "message": "Player deleted"}