import os
import sys
import typer
from django.core.wsgi import get_wsgi_application


sys.path.append('C:\\Users\\ponnb\\Documents\\EpicEvents')


# Définis la variable d'environnement pour les settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialise les settings de Django pour accéder aux modèles
application = get_wsgi_application()

from cli_commands.cli_auth import login, get_user_info
from cli_commands.cli_user import add_user
from cli_commands.cli_commercial import add_client, update_client, delete_client

app = typer.Typer()

app.command()(login)
app.command()(get_user_info)
app.command()(add_user)
app.command()(add_client)
app.command()(update_client)
app.command()(delete_client)

if __name__ == "__main__":
    app()
