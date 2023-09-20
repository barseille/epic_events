from datetime import datetime
from EpicEvents.models import Contrat, CONTRAT_STATUTS, PAYMENT_STATUS
import typer

app = typer.Typer()

@app.command()
def add_contrat(client_id: int, status: str, start_date: str, end_date: str, price: int, payment_received: str, is_signed: bool):
    # Vérification du statut
    valid_status = False
    for contrat_status in CONTRAT_STATUTS:
        if status == contrat_status[0]:
            valid_status = True
            break

    if not valid_status:
        typer.echo("Le statut spécifié n'est pas valide.")
        return

    # Vérification du statut de paiement
    valid_payment_status = False
    for payment_status in PAYMENT_STATUS:
        if payment_received == payment_status[0]:
            valid_payment_status = True
            break

    if not valid_payment_status:
        typer.echo("Le statut de paiement spécifié n'est pas valide.")
        return
    # Vérification du format de la date
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        typer.echo("Le format de la date est invalide. Utilise le format YYYY-MM-DD.")
        return

    try:
        contrat = Contrat.objects.create(
            client_id=client_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            price=price,
            payment_received=payment_received,
            is_signed=is_signed
        )
        typer.echo(f"Contrat créé avec succès avec l'ID {contrat.id}!")
    except Exception as e:
        typer.echo(f"Erreur lors de la création du contrat : {e}")


@app.command()
def list_contrats():
    # Ici, tu peux ajouter le code pour lister tous les contrats
    # Par exemple, en utilisant l'ORM de Django pour récupérer tous les contrats de la base de données
    contrats = Contrat.objects.all()
    for contrat in contrats:
        typer.echo(f"ID: {contrat.id}, Client ID: {contrat.client_id}, Statut: {contrat.status}")

if __name__ == "__main__":
    app()