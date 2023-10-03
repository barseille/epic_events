import os
import sys
import typer
from django.core.wsgi import get_wsgi_application

from cli_commands.cli_auth import login, get_user_info
from cli_commands.cli_user import add_user
from cli_commands.cli_commercial import add_client, update_client, delete_client, add_event_commercial
from cli_commands.cli_admin import add_contrat, update_contrat, delete_contrat
from cli_commands.cli_support import update_event, delete_event, assign_support_to_event

# Utiliser un chemin relatif pour plus de portabilité
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Définis la variable d'environnement pour les settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialise les settings de Django pour accéder aux modèles
application = get_wsgi_application()

# Initialise l'application Typer
app = typer.Typer()

# Ajoute les commandes CLI à l'application Typer
app.command()(login)
app.command()(get_user_info)
app.command()(add_user)

app.command()(add_client)
app.command()(update_client)
app.command()(delete_client)
app.command()(add_event_commercial)

app.command()(add_contrat)
app.command()(update_contrat)
app.command()(delete_contrat)

app.command()(assign_support_to_event)
app.command()(update_event)
app.command()(delete_event)


if __name__ == "__main__":
    app()
