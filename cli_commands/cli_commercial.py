import typer
from EpicEvents.models import Client
from django.core.exceptions import ObjectDoesNotExist
from cli_commands.cli_auth import get_user_info, load_tokens
from typer import Exit

app = typer.Typer()

# @app.command()
# def list_clients():
#     user_info = get_user_info()
#     if user_info is None:
#         typer.echo("Tu dois te connecter d'abord.")
#         return
    
#     if user_info['role'] != 'COMMERCIAL':
#         typer.echo("Accès refusé. Seuls les commerciaux peuvent lister des clients.")
#         return
#     try:
#         clients = Client.objects.all()
#         for client in clients:
#             typer.echo(f"ID: {client.id}, Nom: {client.name}, Email: {client.email}")
#     except Exception as e:
#         typer.echo(f"Erreur : {e}")

@app.command()
def list_clients():
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return
    
    if user_info['role'] != 'COMMERCIAL':
        typer.echo("Accès refusé. Seuls les commerciaux peuvent lister des clients.")
        return
    try:
        clients = Client.objects.all()
        for client in clients:
            typer.echo(f"ID: {client.id}, Nom: {client.name}, Email: {client.email}")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)

@app.command()
def add_client(name: str, email: str, phone: str = None, company_name: str = None):
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return

    if user_info['role'] != 'COMMERCIAL':
        typer.echo("Accès refusé. Seuls les commerciaux peuvent ajouter des clients.")
        return

    try:
        commercial_id = user_info['id']  
        client = Client.objects.create(
            name=name,
            email=email,
            phone=phone,
            company_name=company_name,
            commercial_contact_id=commercial_id  
        )
        typer.echo(f"Client {client.name} ajouté avec succès.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)


@app.command()
def update_client(client_id: int, name: str, email: str, phone: str = None, company_name: str = None):
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return

    if user_info['role'] != 'COMMERCIAL':
        typer.echo("Accès refusé. Seuls les commerciaux peuvent mettre à jour des clients.")
        return

    try:
        client = Client.objects.get(id=client_id)

        if client.commercial_contact_id != user_info['id']:
            typer.echo("Accès refusé. Tu n'es pas le commercial assigné à ce client.")
            return

        if name:
            client.name = name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if company_name:
            client.company_name = company_name

        client.save()
        typer.echo(f"Client {client.name} mis à jour avec succès.")
    except ObjectDoesNotExist:
        typer.echo("Client non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)


@app.command()
def delete_client(client_id: int):
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return

    if user_info['role'] != 'COMMERCIAL':
        typer.echo("Accès refusé. Seuls les commerciaux peuvent supprimer des clients.")
        return

    try:
        client = Client.objects.get(id=client_id)
        
        # Vérifie si le client a été créé par ce commercial
        if client.commercial_contact.id != user_info['id']:
            typer.echo("Accès refusé. Tu n'as pas créé ce client.")
            return

        client.delete()
        typer.echo(f"Client {client.name} supprimé avec succès.")
    except ObjectDoesNotExist:
        typer.echo("Client non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)



if __name__ == "__main__":
    app()
