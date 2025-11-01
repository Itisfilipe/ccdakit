"""List all available document templates."""

import json
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def list_templates_command(
    template_name: Optional[str] = None,
    show_content: bool = False,
) -> None:
    """
    List all available C-CDA document templates.

    Args:
        template_name: Specific template to show (e.g., 'minimal_ccd', 'full_ccd')
        show_content: Display the full template content
    """
    from ccdakit.utils.templates import DocumentTemplates

    console.print("\n[bold cyan]Available Document Templates[/bold cyan]\n")

    try:
        templates_instance = DocumentTemplates()
        available = templates_instance.list_templates()

        if not available:
            console.print("[yellow]No templates available[/yellow]")
            return

        # If specific template requested
        if template_name:
            if template_name not in available:
                console.print(f"[red]Template '{template_name}' not found[/red]")
                console.print("\n[yellow]Available templates:[/yellow]")
                for t in available:
                    console.print(f"  • {t}")
                sys.exit(1)

            # Load and display the template
            template_data = templates_instance.load_template(template_name)

            if show_content:
                # Show full JSON content
                console.print(Panel(
                    json.dumps(template_data, indent=2),
                    title=f"[bold]{template_name}[/bold]",
                    border_style="cyan"
                ))
            else:
                # Show summary
                console.print(f"[bold cyan]Template:[/bold cyan] {template_name}\n")

                # Show structure
                if isinstance(template_data, dict):
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Field", style="cyan")
                    table.add_column("Type", style="yellow")
                    table.add_column("Preview", style="dim")

                    for key, value in template_data.items():
                        value_type = type(value).__name__
                        if isinstance(value, (dict, list)):
                            preview = f"{len(value)} items"
                        elif isinstance(value, str):
                            preview = value[:50] + "..." if len(value) > 50 else value
                        else:
                            preview = str(value)
                        table.add_row(key, value_type, preview)

                    console.print(table)

                console.print("\n[dim]Tip: Use --show-content to see full template[/dim]")

        else:
            # List all templates
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Template Name", style="cyan")
            table.add_column("Description", style="dim")

            # Template descriptions
            descriptions = {
                "minimal_ccd": "Minimal Continuity of Care Document with core sections",
                "full_ccd": "Complete CCD with all standard sections",
                "discharge_summary": "Hospital discharge summary template",
                "progress_note": "Progress note template",
            }

            for template in sorted(available):
                desc = descriptions.get(template, "C-CDA document template")
                table.add_row(template, desc)

            console.print(table)
            console.print(f"\n[bold green]Total:[/bold green] {len(available)} templates available")
            console.print("\n[dim]Tip: Specify template name to view details[/dim]")
            console.print("[dim]Example: ccdakit list-templates minimal_ccd[/dim]\n")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
