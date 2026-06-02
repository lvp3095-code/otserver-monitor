import requests
import re
import json
import os

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
DATA_FILE = "last_levels.json"

PLAYERS = {
    "ADA todaVIDA": "https://dbolegacy.online/characterprofile.php?name=ADA%20todaVIDA",
    "ALDEBARON": "https://dbolegacy.online/characterprofile.php?name=A%20L%20D%20E%20B%20A%20R%20O%20N",
    "Wesllys": "https://dbolegacy.online/characterprofile.php?name=Wesllys",
    "ThuuG ADA": "https://dbolegacy.online/characterprofile.php?name=ThuuG%20ADA",
    "Zeca Pau Gordinho": "https://dbolegacy.online//characterprofile.php?name=zeca+pau+gordinho",
    "TERRO DELES": "https://dbolegacy.online/characterprofile.php?name=TERRO%20DELES",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (OTServer Monitor)"
}

def load_levels():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_levels(levels):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(levels, f, indent=2)

def get_level(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    html = response.text

    # 🔥 BUSCA PELO HTML REAL DO SITE
    match = re.search(
        r'<b\s+class="lvl-highlight">\s*([0-9]+)\s*</b>',
        html,
        re.IGNORECASE
    )

    if not match:
        raise Exception("Level não encontrado na página")

    level = int(match.group(1))
    print(f"[OK] Level encontrado: {level}")

    return level

def notify(player, old, new):
    diff = new - old
    requests.post(
        WEBHOOK,
        json={
            "content": (
                "⚔️ **LEVEL UP DETECTADO!** ⚔️\n"
                f"Player: **{player}**\n"
                f"{old} → {new}  _( +{diff} )_"
            )
        },
        timeout=15
    )

def main():
    last_levels = load_levels()
    updated_levels = {}

    for player, url in PLAYERS.items():
        try:
            current_level = get_level(url)
            last_level = last_levels.get(player)

            if last_level is not None and current_level > last_level:
                notify(player, last_level, current_level)

            updated_levels[player] = current_level

        except Exception as e:
            print(f"[ERRO] {player}: {e}")

    save_levels(updated_levels)

if __name__ == "__main__":
    main()
