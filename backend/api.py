from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .src.database import DBManager

app = FastAPI()
dbm = DBManager()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"data" : "test"}

@app.get("/game")
def get_game():
    game_data = dbm.getRandomGame()
    return {"data" : game_data}


@app.get("/titles")
def get_titles():
    titles = []
    data = dbm.getTitles()
    if data:
        for game in data:
            titles.append(game["title"])

    return {"data" : titles}