import os
import secrets
import threading
import webbrowser

import requests
from flask import Flask, request
from dotenv import load_dotenv


load_dotenv()

DOMAIN = os.environ["AUTH0_DOMAIN"]
CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
AUDIENCE = os.environ["AUTH0_AUDIENCE"]
REDIRECT_URI = os.environ["AUTH0_CALLBACK_URL"]


app = Flask(__name__)

authorization_code = None


@app.route("/callback")
def callback():
    global authorization_code

    authorization_code = request.args.get("code")

    if authorization_code:
        return """
        <h2>Authorization successful.</h2>
        <p>You can close this browser tab and return to the terminal.</p>
        """

    return "Authorization failed."


def get_tokens(code):

    response = requests.post(
        f"https://{DOMAIN}/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
    )

    return response


def refresh(refresh_token):

    return requests.post(
        f"https://{DOMAIN}/oauth/token",
        data={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token
        }
    )


def main():

    print("=" * 60)
    print("SECURENOVA BLUE TEAM")
    print("AUTH0 REFRESH TOKEN ROTATION TEST")
    print("=" * 60)

    state = secrets.token_urlsafe(16)

    authorize_url = (
        f"https://{DOMAIN}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&audience={AUDIENCE}"
        f"&scope=openid%20profile%20email%20offline_access"
        f"&state={state}"
    )

    server_thread = threading.Thread(
        target=lambda: app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False
        )
    )

    server_thread.daemon = True
    server_thread.start()

    print("\nOpening Auth0 login...")
    webbrowser.open(authorize_url)

    print("\nComplete the login in your browser.")
    print("Waiting for authorization...")

    while authorization_code is None:
        pass

    token_response = get_tokens(authorization_code)

    if token_response.status_code != 200:
        print("\nAuthorization code exchange failed.")
        print(token_response.text)
        return

    tokens = token_response.json()

    refresh_token_1 = tokens.get("refresh_token")

    if not refresh_token_1:
        print("\nNo refresh token was returned.")
        print("Check offline_access and Allow Offline Access.")
        return

    print("\nInitial refresh token: OBTAINED")

    # First refresh-token exchange
    first_refresh = refresh(refresh_token_1)

    if first_refresh.status_code != 200:
        print("\nFirst refresh failed.")
        print(first_refresh.text)
        return

    first_tokens = first_refresh.json()

    refresh_token_2 = first_tokens.get("refresh_token")

    print("First refresh: SUCCESS")

    if refresh_token_2:
        print("New refresh token: OBTAINED")
    else:
        print("New refresh token was not returned.")
        return

    # Replay the old refresh token
    print("\nReplaying OLD refresh token...")

    replay = refresh(refresh_token_1)

    print("\nReplay HTTP status:", replay.status_code)

    if replay.status_code == 200:
        print("RESULT: OLD REFRESH TOKEN ACCEPTED")
        print("Rotation protection FAILED")
        print(replay.text)

    else:
        print("RESULT: OLD REFRESH TOKEN REJECTED")
        print("Rotation protection: WORKING")
        print("Auth0 response:")
        print(replay.text)


if __name__ == "__main__":
    main()