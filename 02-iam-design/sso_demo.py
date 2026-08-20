import os

from flask import Flask, redirect, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
SSO_CLIENT_ID = os.environ["SSO_CLIENT_ID"]
SSO_CLIENT_SECRET = os.environ["SSO_CLIENT_SECRET"]

oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=SSO_CLIENT_ID,
    client_secret=SSO_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


@app.route("/")
def home():
    if "user" in session:
        user = session["user"]

        return f"""
        <h1>SecureNova SSO Demo</h1>

        <h2>SSO Login Successful</h2>

        <p>Name: {user.get("name", "User")}</p>
        <p>Email: {user.get("email", "Not available")}</p>

        <p>
            <a href="/logout">Logout</a>
        </p>
        """

    return """
    <h1>SecureNova SSO Demo</h1>

    <p>This is the second SecureNova application.</p>

    <a href="/login">Login with Auth0</a>
    """


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)

    return oauth.auth0.authorize_redirect(
        redirect_uri
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()

    userinfo = token.get("userinfo")

    if userinfo is None:
        userinfo = oauth.auth0.userinfo(token=token)

    session["user"] = userinfo

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )