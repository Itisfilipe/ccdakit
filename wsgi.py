"""WSGI entry point for Render deployment."""

from ccdakit.cli.web.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
