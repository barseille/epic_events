import re
from EpicEvents.models import User, USER_ROLES
import typer

app = typer.Typer()

def is_valid_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    else:
        return False

def is_strong_password(password):
    if len(password) >= 8:
        return True
    else:
        return False


from typer import Exit

@app.command()
def add_user(username: str, email: str, password: str, role: str):
    try:
        # Vérification du rôle
        valid_role = False
        for user_role in USER_ROLES:
            if role == user_role[0]:
                valid_role = True
                break
            
        if not valid_role:
            typer.echo("Le rôle spécifié n'est pas valide.")
            raise Exit(code=1)
        
        if User.objects.filter(username=username).exists():
            typer.echo("Le nom d'utilisateur existe déjà.")
            raise Exit(code=1)
        
        if User.objects.filter(email=email).exists():
            typer.echo("L'e-mail existe déjà.")
            raise Exit(code=1)

        if not is_valid_email(email):
            typer.echo("L'e-mail n'est pas valide.")
            raise Exit(code=1)

        if not is_strong_password(password):
            typer.echo("Le mot de passe doit avoir au moins 8 caractères.")
            raise Exit(code=1)

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        typer.echo(f"{role} {username} créé avec succès!")
    except Exception as e:
        typer.echo(f"Erreur lors de la création : {e}")
        raise Exit(code=1)


# @app.command()
# def add_user(username: str, email: str, password: str, role: str):
    
#     # Vérification du rôle
#     valid_role = False
#     for user_role in USER_ROLES:
#         if role == user_role[0]:
#             valid_role = True
#             break
        
#     if not valid_role:
#         typer.echo("Le rôle spécifié n'est pas valide.")
#         return
    
#     if User.objects.filter(username=username).exists():
#         typer.echo("Le nom d'utilisateur existe déjà.")
#         return
    
#     if User.objects.filter(email=email).exists():
#         typer.echo("L'e-mail existe déjà.")
#         return

#     if not is_valid_email(email):
#         typer.echo("L'e-mail n'est pas valide.")
#         return

#     if not is_strong_password(password):
#         typer.echo("Le mot de passe doit avoir au moins 8 caractères.")
#         return

#     try:
#         user = User.objects.create_user(username=username, email=email, password=password, role=role)
#         typer.echo(f"{role} {username} créé avec succès!")
#     except Exception as e:
#         typer.echo(f"Erreur lors de la création : {e}")

