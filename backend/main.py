from src.utils import *
from database import DBManager

dbm = DBManager()

gameData = getTopNGamesJSON(3)
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

for game in gameData:
    print(game)

    releaseDateData = game["release_dates"]
    platformsData = game["platforms"]
    genresData = game["genres"]
    print(releaseDateData, type(releaseDateData))
    print(platformsData)
    print(genresData)

    releaseDateHumanReadable = getEarliestReleaseDate(releaseDateData)

    platformsList = getPlatforms(platformsData) 
    platforms = ", ".join(platformsList)

    genresList = getGenres(genresData)
    genres = ", ".join(genresList)

    imgId = getCoverJSONByID(game["cover"])
    coverUrl = getCoverURL(game["cover"])

    params = (game["id"], 
              coverUrl, 
              game["name"], 
              genres, 
              platforms, 
              releaseDateHumanReadable, game["summary"], 
              game["rating"])
    
    dbm.execute(query, params)