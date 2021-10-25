from math import ceil
import requests
import json

from requests.api import get
from Connection import Connection


def fetch_all_games(conn, list_type='colecao'):
    collection = get_collection(conn, list_type=list_type)
    total_pages = ceil(collection["total"]/20)
    games = collection["colecao"]
    for pg in range(2, total_pages+1):
        next_page = get_collection(conn, pg=pg,list_type=list_type)
        games += next_page["colecao"]
    return games

def get_collection(conn, pg=1, list_type='colecao'):
    url = f"https://ludopedia.com.br/api/v1/colecao?lista={list_type}&page={pg}&tp_jogo=b"
    headers = {
        "Content-type": "aplication-json",
        "Authorization": f"Bearer {conn.ACESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

if __name__ == '__main__':
    conn = Connection()
    games = fetch_all_games(conn, list_type='jogados')
    for g in games:
        print(g['nm_jogo'])
    print(len(games))
