
import requests, json
from config import CLIENT_ID, ACCESS_TOKEN 

base_url = "https://api.igdb.com/v4/games"
data =  {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
         'data': 'fields id, cover, genres, name, parent_game, platforms, release_dates, summary, rating, rating_count; \
                  where rating_count >= 20; \
                  sort total_rating desc; \
                  limit 100;'}

response = requests.post(base_url, **data)
data = response.json()

json_file = []

for i in range(0, 3):
    cover_id = str(data[i]["cover"])
    cover_url = "https://api.igdb.com/v4/covers"
    cover_data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                'data': f'fields image_id; \
                            where id = {cover_id};'}

    cover_response = requests.post(cover_url, **cover_data)
    cover_data = cover_response.json()

    img_id = str(cover_data[0]["image_id"])
    img_url = f"https://images.igdb.com/igdb/image/upload/t_1080p/{img_id}.jpg"
    img_data = requests.get(img_url).content
    with open("./base_imgs/" + img_id + ".jpg", "wb") as handler:
        handler.write(img_data)

    temp_img_names = []

    for j in range(128, 1080, 128):
        temp_img_names.append(f"./crop_imgs/{cover_data[0]["image_id"]}_cropped_{j}.jpg")
        
        
    json_object = {
        "game_id" : data[i]["id"],
        "cover_id": cover_data[0]["image_id"],
        "name": data[i]["name"],
        "genres": data[i]["genres"],
        "platforms": data[i]["platforms"],
        "release_dates": data[i]["release_dates"],
        "summary": data[i]["summary"],
        "rating": data[i]["rating"],
        "base_img": f"{cover_data[0]["image_id"]}.jpg",
        "crop_img":temp_img_names
    }

    json_file.append(json_object)


with open("games_data.json", "w") as file:
    json.dump(json_file, file, indent=4)