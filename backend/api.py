from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .src.utils import getNumBaseImages
from random import randint
import json

app = FastAPI()

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
    try:
        num_imgs = getNumBaseImages()
        game_data = None
        with open("games_data.json", "r") as file:
            data = json.load(file)
            n = randint(0, 4)
            game_data =  data[n] 
    except FileNotFoundError as err:
        print(err)
    except json.JSONDecodeError as err:
        print(err)
    finally:
        return {"data" : game_data}

@app.get("/titles")
def get_titles():
    try:
        titles = []
        with open("games_data.json", "r") as file:
            data = json.load(file)
            for game in data:
                titles.append(game["name"])
    except FileNotFoundError as err:
        print(err)
    except json.JSONDecodeError as err:
        print(err)
    finally:
        return {"data" : titles}