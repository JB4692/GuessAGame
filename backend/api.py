from fastapi import FastAPI
from .src.utils import getNumBaseImages
from random import randint
import json

app = FastAPI()

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
            n = randint(0, 5)
            game_data =  data[n] 
    except FileNotFoundError as err:
        print(err)
    except json.JSONDecodeError as err:
        print(err)
    finally:
        return {"data" : game_data}