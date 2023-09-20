import os
# Définis la variable d'environnement pour les settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
# Initialise les settings de Django pour accéder aux modèles
application = get_wsgi_application()

import typer
from cli_commands.cli_auth import login, get_data
from cli_commands.cli_user import add_user
from cli_commands.cli_contrat import add_contrat, list_contrats

app = typer.Typer()

app.command()(login)
app.command()(get_data)
app.command()(add_user)
app.command()(add_contrat)
app.command()(list_contrats)


if __name__ == "__main__":
    app()
