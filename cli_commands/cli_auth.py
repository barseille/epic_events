import json
import requests
import typer
app = typer.Typer()

CONFIG_FILE = ".cli_config.json"

def save_tokens(access_token, refresh_token):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"access_token": access_token, "refresh_token": refresh_token}, f)

def load_tokens():
    try:
        with open(CONFIG_FILE, "r") as f:
            tokens = json.load(f)
            return tokens["access_token"], tokens["refresh_token"]
    except FileNotFoundError:
        return None, None

@app.command()
def login(username: str, password: str):
    response = requests.post("http://localhost:8000/api/token/", data={"username": username, "password": password})
    if response.status_code != 200:
        typer.echo(f"Erreur lors de la connexion : {response.status_code}, {response.text}")
        return
    try:
        tokens = response.json()
        save_tokens(tokens["access"], tokens["refresh"])
        typer.echo("Connecté avec succès!")
    except Exception as e:
        typer.echo(f"Erreur lors de la récupération du token : {e}")


@app.command()
def get_data():
    access_token, refresh_token = load_tokens()
    if not access_token:
        typer.echo("Tu dois te connecter d'abord.")
        return

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("http://localhost:8000/api/data/", headers=headers)

    if response.status_code == 401:  # Token expiré
        response = requests.post("http://localhost:8000/api/token/refresh/", data={"refresh": refresh_token})
        new_tokens = response.json()
        save_tokens(new_tokens["access"], refresh_token)
        headers["Authorization"] = f"Bearer {new_tokens['access']}"
        response = requests.get("http://localhost:8000/api/data/", headers=headers)

    data = response.json()
    typer.echo(f"Données récupérées: {data}")