import os
import json
import urllib.request
import urllib.parse


XTREAM_URL = os.environ["XTREAM_URL"].rstrip("/")
XTREAM_USER = os.environ["XTREAM_USER"]
XTREAM_PASS = os.environ["XTREAM_PASS"]

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def test_xtream():

    params = urllib.parse.urlencode({
        "username": XTREAM_USER,
        "password": XTREAM_PASS
    })

    url = f"{XTREAM_URL}/player_api.php?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json,text/plain,*/*"
        }
    )

    print("Connexion au serveur Xtream...")

    try:

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            status = response.status
            body = response.read().decode("utf-8")

    except Exception as e:

        print("❌ Erreur Xtream :", str(e))
        raise

    print("HTTP Xtream :", status)

    if status != 200:
        raise Exception(
            f"Erreur HTTP Xtream : {status}"
        )

    try:
        data = json.loads(body)

    except Exception:
        raise Exception(
            "Le serveur Xtream n'a pas renvoyé du JSON valide."
        )

    user_info = data.get("user_info", {})

    if str(user_info.get("auth")) != "1":
        raise Exception(
            "Authentification Xtream refusée."
        )

    print("✅ Connexion Xtream réussie")
    print(
        "Statut :",
        user_info.get("status")
    )

    return user_info


def send_telegram(user_info):

    url = (
        "https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )

    message = (
        "✅ Test GitHub réussi !\n\n"
        "📡 Connexion IPTV : OK\n"
        f"👤 Statut : {user_info.get('status', 'inconnu')}\n\n"
        "GitHub peut maintenant surveiller NikosTV."
    )

    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    print("Envoi Telegram...")

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        body = response.read().decode("utf-8")

    result = json.loads(body)

    if not result.get("ok"):
        raise Exception(
            "Telegram a refusé le message : " +
            body
        )

    print("✅ Message Telegram envoyé")


if __name__ == "__main__":

    user_info = test_xtream()

    send_telegram(user_info)

    print("✅ TEST COMPLET RÉUSSI")
