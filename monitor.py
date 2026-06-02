import requests
import re
import json
import os

URL = "https://SEU_OTSERVER/character.php?name=PLAYER"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
DATA_FILE = "last_level.json"

def get_level():
    html = requests.get(URL, timeout=30).text
    match = re.search(r"Level[^0-9]*([0-9]+)", html)
    if not match:
        raise Exception("Level não encontrado na página")
    return int(match.group(1))

def load_last_level():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f).get("level")
    return None

def save_level(level):
    with open(DATA_FILE, "w") as f:
        json.dump({"level": level}, f)

def notify(old, new):
    requests.post(WEBHOOK, json={
        "content": f"⚔️ **Level UP detectado!**\nPlayer subiu de {old} → {new}"
    })

def main():
    current = get_level()
    last = load_last_level()

    if last and current > last:
        notify(last, current)

    save_level(current)

if __name__ == "__main__":
    main()
