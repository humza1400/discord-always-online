import os
import sys
import json
import time
import requests
import websocket
import random
import threading
from websocket import create_connection

status = ['online', 'idle', 'dnd']
headers = {"Authorization": "", "Content-Type": "application/json"}
tokens = []

with open('tokens.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    token = line.strip().split()[0]
    tokens.append(token)

def validate_token(token):
    headers["Authorization"] = token
    validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
    if validate.status_code != 200:
        print(f"\x1b[31m[ERROR] Invalid token {token}\x1b[0m")
        return False
    else:
        userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
        username = userinfo["username"]
        discriminator = userinfo["discriminator"]
        userid = userinfo["id"]
        print(f"\033[32mLogged in as {username}#{discriminator} ({userid}).\033[0m")
        return True

def onliner(token, status):
    while True:
        try:
            ws = create_connection('wss://gateway.discord.gg/?v=9&encoding=json')
            start = json.loads(ws.recv())
            heartbeat = start['d']['heartbeat_interval']
            if status == "online":
                if random.random() < 0.40:
                    auth = {"op": 2,"d": {"token": token,"properties": {"$os": "iOS","$browser": "Discord iOS","$device": "iPhone"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
                else:
                    auth = {"op": 2,"d": {"token": token,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
            else:
                auth = {"op": 2,"d": {"token": token,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
            ws.send(json.dumps(auth))
            online = {"op":1,"d":"None"}
            time.sleep(heartbeat / 1000)
            ws.send(json.dumps(online))
        except:
            print(f"\x1b[31m[ERROR] Failed to connect to gateway for token {token}\x1b[0m")
            time.sleep(10)

def run_onliner():
    try:
        user_tokens = [token for token in tokens if validate_token(token)]
        threads = []
        for token in user_tokens:
            thread = threading.Thread(target=onliner, args=(token, random.choice(status)))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Closing websocket connections...")
        for ws in websockets:
            ws.close()

run_onliner()