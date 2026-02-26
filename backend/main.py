from src.utils import *
from src.images import *
"""
1. get get Top X games
2. get covers for each game
3. Download cover image
4. create the json file of all the games
5. Load json file
6. create images from base images and save them.
"""
n = getNumBaseImages()
print(n)

# game_json_list = getTopNGamesJSON(5)

# cover_json_list = []

# for i, game in enumerate(game_json_list):
#     cover_json = getCoverJSONByID(game["cover"])
    
#     downloadCoverImage1080p(cover_json[0]["image_id"])
#     # print(f"Downloaded: {game["name"]}")

#     cover_json_list.append(cover_json[0])

# createGameJSONFile(game_json_list, cover_json_list)
