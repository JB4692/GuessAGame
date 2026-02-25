
import os, requests
from config import CLIENT_ID, ACCESS_TOKEN

base_url = "https://api.igdb.com/v4/popularity_primitives"
data =  {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
         'data': 'fields game_id,value,popularity_type; sort value desc; limit 10; where popularity_type = 1;'}

response = requests.post(base_url, **data)
data = response.json()

for i in range(0, 10):
    game_id = str(data[i]["game_id"])
    game_url = "https://api.igdb.com/v4/games"
    game_data =     cover_data = {'headers': {'Client-ID': f'{CLIENT_ID}', 'Authorization': f'Bearer {ACCESS_TOKEN}'},
                                  'data': f'fields name; where id = {game_id};'}

    game_response = requests.post(game_url, **game_data)
    game_data = game_response.json()
    print(game_data)
    
    
