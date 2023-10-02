import typer
from EpicEvents.models import Event, User
from django.core.exceptions import ObjectDoesNotExist
from cli_commands.cli_auth import get_user_info
from typer import Exit

app = typer.Typer()


@app.command()
def assign_support_to_event(event_id: int, support_id: int):
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return

    if user_info['role'] != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent assigner du support aux événements.")
        return

    try:
        event = Event.objects.get(id=event_id)
        support_user = User.objects.get(id=support_id)

        if support_user.role != 'SUPPORT':
            typer.echo("L'utilisateur assigné doit être un membre de l'équipe de support.")
            return

        event.support_contact = support_user
        event.save()
        typer.echo(f"Membre du support {support_id} assigné à l'événement {event_id} avec succès.")

    except ObjectDoesNotExist:
        typer.echo("Événement ou utilisateur non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)



@app.command()
def update_event(event_id: int, start_date: str = None, end_date: str = None, attendees: int = None, notes: str = None):
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return

    if user_info['role'] != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent mettre à jour des événements.")
        return

    try:
        event = Event.objects.get(id=event_id)
        
        if event.support_contact_id != user_info['id']:
            typer.echo("Accès refusé. Seul l'auteur de l'événement peut le mettre à jour.")
            return
        
        if start_date:
            event.start_date = start_date
        if end_date:
            event.end_date = end_date
        if attendees:
            event.attendees = attendees
        if notes:
            event.notes = notes

        event.save()
        typer.echo(f"Événement {event_id} mis à jour avec succès.")
    except ObjectDoesNotExist:
        typer.echo("Événement non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)

@app.command()
def delete_event(event_id: int):
    user_info = get_user_info()
    if user_info is None:
        typer.echo("Tu dois te connecter d'abord.")
        return

    if user_info['role'] != 'SUPPORT':
        typer.echo("Accès refusé. Seuls les membres du support peuvent supprimer des événements.")
        return

    try:
        event = Event.objects.get(id=event_id)
        
        if event.support_contact_id != user_info['id']:
            typer.echo("Accès refusé. Seul l'auteur de l'événement peut le supprimer.")
            return
        
        event.delete()
        typer.echo(f"Événement {event_id} supprimé avec succès.")
    except ObjectDoesNotExist:
        typer.echo("Événement non trouvé.")
    except Exception as e:
        typer.echo(f"Erreur : {e}")
        raise Exit(code=1)

if __name__ == "__main__":
    app()
