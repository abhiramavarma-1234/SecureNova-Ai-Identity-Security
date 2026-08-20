import os
from urllib.parse import urlencode

import jwt
from jwt import PyJWKClient
from functools import wraps
from flask import jsonify

from flask import Flask, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
AUTH0_AUDIENCE = os.environ["AUTH0_AUDIENCE"]
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

jwks_client = PyJWKClient(JWKS_URL)

oauth = OAuth(app)

auth0 = oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email read:ai-data",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def validate_access_token():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None, "Missing Bearer token"

    token = auth_header.split(" ", 1)[1]

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUTH0_AUDIENCE,
            issuer=AUTH0_ISSUER,
        )

        return payload, None

    except jwt.ExpiredSignatureError:
        return None, "Token expired"

    except jwt.InvalidAudienceError:
        return None, "Invalid audience"

    except jwt.InvalidIssuerError:
        return None, "Invalid issuer"

    except jwt.InvalidTokenError as error:
        return None, f"Invalid token: {error}"


@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
        return f"""
        <h1>SecureNova AI Chat</h1>
        <h2>Welcome, {user.get("name", "User")}</h2>

        <p>Email: {user.get("email", "Not available")}</p>

        <p>
            <a href="/logout">Logout</a>
        </p>

        <pre>
        Access Token:
        {session.get("access_token", "Not available")}
        </pre>
        """

    return """
    <h1>SecureNova AI Chat</h1>
    <p>AI Identity Security Capstone</p>
    <a href="/login">Login with Auth0</a>
    """


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)

    return oauth.auth0.authorize_redirect(
        redirect_uri,
        audience=AUTH0_AUDIENCE,
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()

    userinfo = token.get("userinfo")

    if userinfo is None:
        userinfo = oauth.auth0.userinfo(token=token)

    session["user"] = userinfo
    session["access_token"] = token.get("access_token")
    session["id_token"] = token.get("id_token")

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    params = {
        "client_id": AUTH0_CLIENT_ID,
        "returnTo": os.environ["AUTH0_LOGOUT_URL"],
    }

    return redirect(
        f"https://{AUTH0_DOMAIN}/v2/logout?{urlencode(params)}"
    )


@app.route("/api/user-data")
def user_data():
    payload, error = validate_access_token()

    if error:
        return jsonify({
            "error": "unauthorized",
            "message": error
        }), 401

    permissions = payload.get("permissions", [])

    if "read:ai-data" not in permissions:
        return jsonify({
            "error": "forbidden",
            "message": "read:ai-data permission required"
        }), 403

    return jsonify({
        "message": "User-level AI data access granted",
        "permissions": permissions,
        "subject": payload.get("sub")
    })


@app.route("/api/admin")
def admin_data():
    payload, error = validate_access_token()

    if error:
        return jsonify({
            "error": "unauthorized",
            "message": error
        }), 401

    permissions = payload.get("permissions", [])

    if "write:admin" not in permissions:
        return jsonify({
            "error": "forbidden",
            "message": "write:admin permission required"
        }), 403

    return jsonify({
        "message": "Admin access granted",
        "permissions": permissions,
        "subject": payload.get("sub")
    })


@app.route("/test-api")
def test_api():
    if "access_token" not in session:
        return redirect("/login")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SecureNova API Authorization Test</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f5f5f5;
            }}

            h1 {{
                margin-bottom: 30px;
            }}

            .container {{
                display: flex;
                gap: 30px;
            }}

            .card {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                width: 45%;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }}

            button {{
                padding: 10px 18px;
                margin-bottom: 15px;
                cursor: pointer;
                border-radius: 5px;
                border: 1px solid #555;
                background: #fff;
            }}

            pre {{
                background: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                white-space: pre-wrap;
            }}

            .success {{
                font-weight: bold;
            }}

            .forbidden {{
                font-weight: bold;
            }}
        </style>
    </head>

    <body>

        <h1>SecureNova AI API Authorization Test</h1>

        <p>
            <strong>Authenticated User:</strong>
            Authorization testing using Auth0 RBAC
        </p>

        <div class="container">

            <div class="card">

                <h2>User API</h2>

                <p>
                    Required Permission:
                    <strong>read:ai-data</strong>
                </p>

                <button onclick="testUserAPI()">
                    Test User API
                </button>

                <pre id="userResult">Not tested yet</pre>

            </div>


            <div class="card">

                <h2>Admin API</h2>

                <p>
                    Required Permission:
                    <strong>write:admin</strong>
                </p>

                <button onclick="testAdminAPI()">
                    Test Admin API
                </button>

                <pre id="adminResult">Not tested yet</pre>

            </div>

        </div>


        <script>

            const accessToken = {session["access_token"]!r};


            async function testUserAPI() {{

                const response = await fetch("/api/user-data", {{
                    headers: {{
                        "Authorization": "Bearer " + accessToken
                    }}
                }});

                const data = await response.json();

                document.getElementById("userResult").textContent =
                    "HTTP " + response.status + "\\n\\n" +
                    JSON.stringify(data, null, 2);
            }}


            async function testAdminAPI() {{

                const response = await fetch("/api/admin", {{
                    headers: {{
                        "Authorization": "Bearer " + accessToken
                    }}
                }});

                const data = await response.json();

                document.getElementById("adminResult").textContent =
                    "HTTP " + response.status + "\\n\\n" +
                    JSON.stringify(data, null, 2);
            }}

        </script>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)