import json
import requests
import typer
from typer import Exit

app = typer.Typer()
CONFIG_FILE = "cli_commands/.cli_config.json"


def save_tokens(access_token, refresh_token):
    """
    Sauvegarde les tokens d'accès et de rafraîchissement dans un fichier JSON.
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"access_token": access_token, "refresh_token": refresh_token}, f, indent=4)
    except Exception as e:
        typer.echo(f"Erreur lors de la sauvegarde des tokens : {e}")
        raise Exit(code=1)
    
    
def load_tokens():
    """
    Charge les tokens d'accès et de rafraîchissement depuis un fichier JSON.
    Retourne None, None si le fichier n'existe pas.
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            tokens = json.load(f)
            return tokens["access_token"], tokens["refresh_token"]
    except FileNotFoundError:
        return None, None
    except Exception as e:
        typer.echo(f"Erreur lors du chargement des tokens : {e}")
        raise Exit(code=1)

  
"""
les tokens ne sont pas générés lors de la création de l'utilisateur,
mais plutôt lors de la première connexion réussie de cet utilisateur.
Ces tokens sont ensuite sauvegardés et utilisés pour les interactions futures avec l'API
"""


@app.command()
def login(username: str, password: str):
    """
    Connecte l'utilisateur en utilisant son nom d'utilisateur et son mot de passe.
    Sauvegarde les tokens générés pour des utilisations futures.
    """
    try:
        response = requests.post("http://localhost:8000/api/token/", data={"username": username, "password": password})
        if response.status_code != 200:
            typer.echo(f"Erreur lors de la connexion : {response.status_code}, {response.text}")
            raise Exit(code=1)

        tokens = response.json()
        save_tokens(tokens["access"], tokens["refresh"])
        typer.echo("Connecté avec succès!")
    except Exception as e:
        typer.echo(f"Erreur lors de la récupération du token : {e}")
        raise Exit(code=1)


@app.command()
def refresh_token():
    """
    Cette fonction utilise le token de rafraîchissement pour obtenir un nouveau token d'accès.
    """
    try:
        # Charger les tokens existants
        access_token, refresh_token = load_tokens()
        if not refresh_token:
            typer.echo("Tu dois te connecter d'abord.")
            return

        # Utiliser le token de rafraîchissement pour obtenir un nouveau token d'accès
        response = requests.post("http://localhost:8000/api/token/refresh/", data={"refresh": refresh_token})

        # Vérifier si la requête a réussi
        if response.status_code != 200:
            typer.echo(f"Erreur lors du rafraîchissement du token : {response.status_code}, {response.text}")
            return

        # Sauvegarder le nouveau token d'accès
        new_tokens = response.json()
        save_tokens(new_tokens["access"], refresh_token)

        typer.echo("Token d'accès rafraîchi avec succès!")
    except Exception as e:
        typer.echo(f"Erreur lors du rafraîchissement du token : {e}")
        raise Exit(code=1)
    

def get_user_info():
    """
    Récupère les informations de l'utilisateur connecté en utilisant le token d'accès.
    """
    try:
        access_token, _ = load_tokens()  # On utilise seulement le token d'accès ici
        if not access_token:
            typer.echo("Tu dois te connecter d'abord.")
            raise Exit(code=1)

        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Change cette URL pour cibler l'utilisateur connecté
        response = requests.get("http://localhost:8000/api/users/me/", headers=headers)

        if response.status_code != 200:
            typer.echo(f"Erreur de la récupération des informations user : {response.status_code}, {response.text}")
            raise Exit(code=1)

        return response.json()
    except Exception as e:
        typer.echo(f"Une erreur s'est produite lors de la récupération des informations utilisateur : {e}")
        raise Exit(code=1)
