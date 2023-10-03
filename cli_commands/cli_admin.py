import typer
from EpicEvents.models import Contrat
from django.core.exceptions import ObjectDoesNotExist
from cli_commands.cli_auth import get_user_info
from typer import Exit

app = typer.Typer()


@app.command()
def add_contrat(client_id: int,
                status: str,
                start_date: str,
                end_date: str,
                price: int,
                payment_received: str,
                is_signed: bool,
                author_id):
    """
    Ajoute un nouveau contrat.
    Seuls les utilisateurs avec le rôle 'ADMINISTRATION' peuvent exécuter cette commande.
    """
    try:
        user_info = get_user_info()
        if user_info is None:
            typer.echo("Tu dois te connecter d'abord.")
            return

        if user_info['role'] != 'ADMINISTRATION':
            typer.echo("Accès refusé. Seuls les administrateurs peuvent ajouter des contrats.")
            return

        Contrat.objects.create(
            client_id=client_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            price=price,
            payment_received=payment_received,
            is_signed=is_signed,
            contrat_author_id=author_id
        )
        typer.echo(f"Contrat pour le client {client_id} ajouté avec succès.")
        
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)


@app.command()
def update_contrat(contrat_id: int,
                   status: str = None,
                   start_date: str = None,
                   end_date: str = None,
                   price: int = None,
                   payment_received: str = None,
                   is_signed: bool = None,
                   author_id: int = None):
    """
    Met à jour un contrat existant.
    Seuls les utilisateurs avec le rôle 'ADMINISTRATION' peuvent exécuter cette commande.
    """
    try:
        user_info = get_user_info()
        if user_info is None:
            typer.echo("Tu dois te connecter d'abord.")
            return

        if user_info['role'] != 'ADMINISTRATION':
            typer.echo("Accès refusé. Seuls les administrateurs peuvent mettre à jour des contrats.")
            return

        contrat = Contrat.objects.get(id=contrat_id)
        
        if status:
            contrat.status = status
        if start_date:
            contrat.start_date = start_date
        if end_date:
            contrat.end_date = end_date
        if price:
            contrat.price = price
        if payment_received:
            contrat.payment_received = payment_received
        if is_signed is not None:
            contrat.is_signed = is_signed
        if author_id is not None:
            contrat.contrat_author_id = author_id

        contrat.save()
        typer.echo(f"Contrat {contrat_id} mis à jour avec succès.")
        
    except ObjectDoesNotExist:
        typer.echo("Contrat non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)


@app.command()
def delete_contrat(contrat_id: int):
    """
    Supprime un contrat existant.
    Seuls les utilisateurs avec le rôle 'ADMINISTRATION' peuvent exécuter cette commande.
    """
    try:
        user_info = get_user_info()
        if user_info is None:
            typer.echo("Tu dois te connecter d'abord.")
            return

        if user_info['role'] != 'ADMINISTRATION':
            typer.echo("Accès refusé. Seuls les administrateurs peuvent supprimer des contrats.")
            return

        contrat = Contrat.objects.get(id=contrat_id)
        contrat.delete()
        typer.echo(f"Contrat {contrat_id} supprimé avec succès.")
        
    except ObjectDoesNotExist:
        typer.echo("Contrat non trouvé.")
        
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)


if __name__ == "__main__":
    app()
