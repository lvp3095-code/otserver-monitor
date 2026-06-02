import requests
import re
import json
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
DATA_FILE = "last_levels.json"

# 🔽 COLOQUE AQUI SEUS 5 PERSONAGENS
PLAYERS = {
    "Player1": "https://dbolegacy.online/characterprofile.php?name=ADA%20todaVIDA",
    "Player2": "https://dbolegacy.online/characterprofile.php?name=A%20L%20D%20E%20B%20A%20R%20O%20N",
    "Player3": "https://dbolegacy.online/characterprofile.php?name=Wesllys",
    "Player4": "https://dbolegacy.online/characterprofile.php?name=ThuuG%20ADA",
    "Player5": "https://dbolegacy.online/characterprofile.php?name=TERRO%20DELES",
}

def load_levels():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_levels(levels):
    with open(DATA_FILE, "w") as f:
        json.dump(levels, f)

def get_level(url):
    html = requests.get(url, timeout=30).text
    match = re.search(r"Level[^0-9]*([0-9]+)", html, re.IGNORECASE)
    if not match:
        raise Exception("Level não encontrado")
    return int(match.group(1))

def notify(player, old, new):
    requests.post(
        WEBHOOK,
        json={
            "content": (
                "⚔️ **LEVEL UP DETECTADO!** ⚔️\n"
                f"Player: **{player}**\n"
                f"{old} → {new}"
            )
        },
        timeout=15
    )

def main():
    last_levels = load_levels()
    updated_levels = last_levels.copy()

    for player, url in PLAYERS.items():
        try:
            current_level = get_level(url)
            last_level = last_levels.get(player)

            if last_level is not None and current_level > last_level:
                notify(player, last_level, current_level)

            updated_levels[player] = current_level

        except Exception as e:
            print(f"Erro ao verificar {player}: {e}")

    save_levels(updated_levels)

if __name__ == "__main__":
    main()
