import requests
import time
import json
from src.database import DBManager
from src.config import CLIENT_ID, ACCESS_TOKEN

dbm = DBManager()

headers = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

game_body = """
fields id, name, summary, rating, total_rating, rating_count, genres.name, platforms.name, release_dates.human, cover.image_id;
where rating_count >= 20; \
sort total_rating desc; \
limit 500;
"""


response = requests.post(
    "https://api.igdb.com/v4/games",
    headers=headers,
    data=game_body
)


gameData = response.json()

# Now process safely
data_to_insert = []

for i, game in enumerate(gameData):
    genres_data = game.get("genres", [])
    
    if isinstance(genres_data, list):
        genres = ", ".join([g.get("name", "Unknown") for g in genres_data if isinstance(g, dict)])
    else:
        print(f"genres is not a list: {type(genres_data)}")
        genres = ""
    
    # Platforms
    platforms_data = game.get("platforms", [])
    if isinstance(platforms_data, list):
        platforms = ", ".join([p.get("name", "Unknown") for p in platforms_data if isinstance(p, dict)])
    else:
        platforms = ""
    
    # Cover URL
    cover = game.get("cover", {})
    if isinstance(cover, dict) and cover.get("image_id"):
        cover_url = f"https://images.igdb.com/igdb/image/upload/t_1080p/{cover['image_id']}.jpg"
    else:
        cover_url = ""
    
    # Release date
    release_dates = game.get("release_dates", [])
    if isinstance(release_dates, list) and release_dates:
        earliest = release_dates[0].get("human", "") if isinstance(release_dates[0], dict) else ""
    else:
        earliest = ""
    
    data_to_insert.append((
        game.get("id"),
        cover_url,
        game.get("name", ""),
        genres,
        platforms,
        earliest,
        game.get("summary", ""),
        game.get("rating", 0)
    ))

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
print(f"Processed {len(data_to_insert)} games")

start = time.time()
cursor = dbm.connection.cursor()
cursor.executemany(query, data_to_insert)
cursor.connection.commit()
insertTime = time.time() - start
print(f"Inserted {len(data_to_insert)} games into DB in {insertTime:.2f} seconds.")
