from math import ceil
import requests
import json

from requests.api import get
from Connection import Connection


def fetch_all_games(conn):
    collection = get_collection(conn)
    total_pages = ceil(collection["total"]/20)
    games = collection["colecao"]
    for pg in range(2, total_pages+1):
        next_page = get_collection(conn, pg=pg)
        games += next_page["colecao"]
    return games

def get_collection(conn, pg=1):
    url = f"https://ludopedia.com.br/api/v1/colecao?lista=colecao&page={pg}"
    headers = {
        "Content-type": "aplication-json",
        "Authorization": f"Bearer {conn.ACESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

if __name__ == '__main__':
    conn = Connection()
    games = fetch_all_games(conn)
    print(len(games))