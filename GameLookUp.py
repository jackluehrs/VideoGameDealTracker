import os
import sys

import requests


gameList = [
    "ELDEN RING",
    "Hollow Knight",
    "Celeste",
    "Tabletop Simulator",
    "Safari-TV"
]

def LookUpGames(gameList):
    for i in gameList:
        PriceLookUp(i)

def PriceLookUp(name: str):
    url = "https://www.cheapshark.com/api/1.0/deals"
    params = {"title": name, "exact": 1}
    headers = {"User-Agent": "VideoGameDealTracker/1.0"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if response.status_code != 200 or not isinstance(data, list):
        print(f"CheapShark lookup failed for {name!r} ({response.status_code}): {data}")
        return
    ExtractGameInfo(data)

steamGamesStoreID = "1"
epicGamesStoreID = "25"

def ExtractGameInfo(gameInfo):
    for gameInfoStore in gameInfo:
        if gameInfoStore["storeID"] == steamGamesStoreID or gameInfoStore["storeID"] == epicGamesStoreID:
            if gameInfoStore["storeID"] == steamGamesStoreID:
                gamePlatform = "Steam"
            else:
                gamePlatform = "Epic Games"
            gameTitle = gameInfoStore["title"]
            gameSalePrice = gameInfoStore["salePrice"]
            gameRetailPrice = gameInfoStore["normalPrice"]
            if float(gameSalePrice) < float(gameRetailPrice):
                PostOnDiscord(str(gameTitle)+" is on sale on "+str(gamePlatform)+"! \nSale Price: "+str(gameSalePrice)+" \nRetailPrice: "+str(gameRetailPrice))


try:
    from discord_webhook import DISCORD_WEBHOOK_URL
except ImportError:
    DISCORD_WEBHOOK_URL = ""

botURL = os.environ.get("DISCORD_WEBHOOK_URL") or DISCORD_WEBHOOK_URL
if not botURL:
    sys.exit("No Discord webhook found. Copy discord_webhook.example.py to discord_webhook.py "
             "and add your URL, or set the DISCORD_WEBHOOK_URL environment variable.")
def PostOnDiscord(message):
    payload = {"content": message}
    try:
        response = requests.post(botURL,json=payload)
        if response.status_code == 204:
            print("Message sent successfully")
        else:
            print(f"Failed to send message. Discord responded with status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"A network error occurred while texting Discord: {e}")

LookUpGames(gameList)
