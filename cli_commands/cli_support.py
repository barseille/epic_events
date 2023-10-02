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
    
    
    
# @app.command()
# def add_event(contrat_id: int, start_date: str, end_date: str, attendees: int, notes: str = None):
#     user_info = get_user_info()
#     if user_info is None:
#         typer.echo("Tu dois te connecter d'abord.")
#         return

#     if user_info['role'] != 'SUPPORT':
#         typer.echo("Accès refusé. Seuls les membres du support peuvent ajouter des événements.")
#         return

#     try:
#         # Vérifier si le contrat existe et est signé
#         contrat = Contrat.objects.get(id=contrat_id)
#         if not contrat.is_signed:
#             typer.echo("Le contrat doit être signé avant de créer un événement.")
#             return
        
#         # Vérifier si un événement existe déjà pour ce contrat
#         existing_event = Event.objects.filter(contrat_id=contrat_id).first()
#         if existing_event:
#             typer.echo("Un événement existe déjà pour ce contrat.")
#             return
        
#         # Vérifier si le paiement a été reçu
#         if contrat.payment_received != 'OUI':
#             typer.echo("Le paiement doit être reçu avant de créer un événement.")
#             return

#         event = Event.objects.create(
#             contrat_id=contrat_id,
#             support_contact_id=user_info['id'],
#             start_date=start_date,
#             end_date=end_date,
#             attendees=attendees,
#             notes=notes
#         )
#         typer.echo(f"Événement pour le contrat {contrat_id} ajouté avec succès.")
#     except Exception as e:
#         typer.echo(f"Erreur : {e}")
#         raise Exit(code=1)
