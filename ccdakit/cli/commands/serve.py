"""Serve command implementation."""

from rich.console import Console

from ccdakit.cli.web.app import create_app

console = Console()


def serve_command(host: str = "127.0.0.1", port: int = 8000, debug: bool = False) -> None:
    """
    Start the web UI server.

    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    console.print("\n[bold cyan]Starting ccdakit web UI...[/bold cyan]")
    console.print(f"[green]Server:[/green] http://{host}:{port}")
    console.print("[dim]Press Ctrl+C to stop the server[/dim]\n")

    app = create_app()
    app.run(host=host, port=port, debug=debug)
