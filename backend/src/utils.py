import requests, json, os
from .config import CLIENT_ID, ACCESS_TOKEN
from .database import DBManager
from typing import Any

def getTopNGamesJSON(n):
    """
    top n games to get -> all their game data as json (list of dicts)
    """

    base_url = "https://api.igdb.com/v4/games"
    data =  {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
            'data': f'fields id, cover, genres, name, parent_game, platforms, release_dates, summary, rating, rating_count; \
                    where rating_count >= 20; \
                    sort total_rating desc; \
                    limit {n};'}

    response = requests.post(base_url, **data)
    game_data = response.json()

    return game_data


def getCoverJSONByID(id):
    """
    "cover" id -> json of game cover data. use image_id for identifier for URL from IGDB 
    """

    base_url = "https://api.igdb.com/v4/covers"
    data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields image_id; \
                            where id = {id};'}

    response = requests.post(base_url, **data)
    cover_data = response.json()

    return cover_data


def getEarliestReleaseDate(ids: list[int]) -> str:
    """
    list of release date (non-human readable) -> the earliest release date as string
    """
    min_id: int = min(ids)
    base_url = "https://api.igdb.com/v4/release_dates"
    data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields *; \
                            where id = {min_id};'}

    response = requests.post(base_url, **data)
    release_dates = response.json()

    return release_dates[0]["human"]


def getPlatforms(ids: list[int]) -> list[str]:
    """
    list of platform ids -> list of platforms as strings/their names
    """
    listOfPlatforms = []
    
    for id in ids:
        baseUrl = "https://api.igdb.com/v4/platforms"
        data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields *; \
                        where id = {id};'}

        response = requests.post(baseUrl, **data)
        platformJson = response.json()
        listOfPlatforms.append(platformJson[0]["name"])
    
    return listOfPlatforms


def getGenres(ids: list[int]) -> list[str]:
    """
    list of genre ids -> list of genres as strings/their names
    """
    listOfGenres = []
    
    for id in ids:
        baseUrl = "https://api.igdb.com/v4/genres"
        data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields *; \
                        where id = {id};'}

        response = requests.post(baseUrl, **data)
        platformJson = response.json()
        listOfGenres.append(platformJson[0]["name"])
    
    return listOfGenres


def getCoverURL(id: int) -> str:
    """
    cover id -> URL to the game's cover art in 1080p 
    """

    base_url = "https://api.igdb.com/v4/covers"
    data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields image_id; \
                            where id = {id};'}

    response = requests.post(base_url, **data)
    cover_data = response.json()

    return f"https://images.igdb.com/igdb/image/upload/t_1080p/{cover_data[0]["image_id"]}.jpg"

def insertIntoDb(data: Any, dbm: DBManager) -> None:
    query = """INSERT INTO games (gameId ,
                              coverUrl,
                              title ,
                              genre,
                              platform ,
                              releaseDate,
                              summary ,
                              rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT DO NOTHING""" 

    for game in data:

        releaseDateData = game["release_dates"]
        platformsData = game["platforms"]
        genresData = game["genres"]

        releaseDateHumanReadable = getEarliestReleaseDate(releaseDateData)

        platformsList = getPlatforms(platformsData) 
        platforms = ", ".join(platformsList)

        genresList = getGenres(genresData)
        genres = ", ".join(genresList)

        coverUrl = getCoverURL(game["cover"])

        params = (game["id"], 
                coverUrl, 
                game["name"], 
                genres, 
                platforms, 
                releaseDateHumanReadable, game["summary"], 
                game["rating"])
        
        dbm.execute(query, params)
        print("Inserted into DB:", game["name"])

# ======================= OLD STUFF ========================================================

def getNumBaseImages():
    return len(os.listdir("./base_imgs/"))


def downloadCoverImage1080p(id):
    """Downloads the cover image of the game's cover using image_id. Dimensions: 1920x1080p."""

    url = f"https://images.igdb.com/igdb/image/upload/t_1080p/{id}.jpg"
    data = requests.get(url).content
    with open("./base_imgs/" + id + ".jpg", "wb") as handler:
        handler.write(data)


def createGameJSONFile(game_data, cover_data):
    """Uses the lists of json data passed in to create a file of all the game objects."""

    json_file = []

    for i in range(0, len(game_data)):
        crop_img_names = []
        count = 0
        for j in range(128, 1080, 128):
            crop_img_names.append(f"./crop_imgs/{cover_data[i]["image_id"]}_cropped_{count}.jpg")
        
        json_object = {
            "game_id" : game_data[i]["id"],
            "cover_id": cover_data[i]["image_id"],
            "name": game_data[i]["name"],
            "genres": game_data[i]["genres"],
            "platforms": game_data[i]["platforms"],
            "release_dates": game_data[i]["release_dates"],
            "summary": game_data[i]["summary"],
            "rating": game_data[i]["rating"],
            "base_img": f"{cover_data[i]["image_id"]}.jpg",
            "crop_img":crop_img_names
        }

        json_file.append(json_object)


    with open("games_data.json", "w") as file:
        json.dump(json_file, file, indent=4)
    
