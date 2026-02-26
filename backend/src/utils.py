import requests, json, os
from .config import CLIENT_ID, ACCESS_TOKEN

def getNumBaseImages():
    return len(os.listdir("./base_imgs/"))

def getTopNGamesJSON(n):
    """Returns JSON of top n number games from IGDB based on their rating."""

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
    Returns the JSON of the game with passed in id.
    From IGDB API, pass in the game's "cover" id. 
    Used to get the image_id field.   
    """

    base_url = "https://api.igdb.com/v4/covers"
    data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields image_id; \
                            where id = {id};'}

    response = requests.post(base_url, **data)
    cover_data = response.json()

    return cover_data

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
        for j in range(128, 1080, 128):
            crop_img_names.append(f"./crop_imgs/{cover_data[i]["image_id"]}_cropped_{j}.jpg")
        
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
    

