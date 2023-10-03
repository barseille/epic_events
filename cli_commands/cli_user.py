import re
from EpicEvents.models import User, USER_ROLES
import typer
from typer import Exit

app = typer.Typer()


def is_valid_email(email: str) -> bool:
    """
    Vérifie si l'e-mail est valide en utilisant une expression régulière.
    Retourne True si l'e-mail est valide, sinon False.
    """
    regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w+$'
    return bool(re.search(regex, email))


def is_strong_password(password: str) -> bool:
    """
    Vérifie si le mot de passe est fort.
    Un mot de passe fort doit avoir au moins 8 caractères.
    Retourne True si le mot de passe est fort, sinon False.
    """
    return len(password) >= 8


@app.command()
def add_user(username: str, email: str, password: str, role: str):
    """
    Ajoute un nouvel utilisateur avec un rôle spécifié.
    Vérifie également la validité de l'e-mail et la force du mot de passe.
    """
    try:
        # Vérification du rôle
        if role not in [user_role[0] for user_role in USER_ROLES]:
            typer.echo("Le rôle spécifié n'est pas valide.")
            raise Exit(code=1)

        # Vérification de l'unicité du nom d'utilisateur et de l'e-mail
        if User.objects.filter(username=username).exists():
            typer.echo("Le nom d'utilisateur existe déjà.")
            raise Exit(code=1)

        if User.objects.filter(email=email).exists():
            typer.echo("L'e-mail existe déjà.")
            raise Exit(code=1)

        # Vérification de la validité de l'e-mail et de la force du mot de passe
        if not is_valid_email(email):
            typer.echo("L'e-mail n'est pas valide.")
            raise Exit(code=1)

        if not is_strong_password(password):
            typer.echo("Le mot de passe doit avoir au moins 8 caractères.")
            raise Exit(code=1)

        # Création de l'utilisateur
        User.objects.create_user(username=username, email=email, password=password, role=role)
        typer.echo(f"{role} {username} créé avec succès!")
    except Exception as e:
        typer.echo(f"Erreur lors de la création : {e}")
        raise Exit(code=1)
