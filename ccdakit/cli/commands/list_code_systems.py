"""List all available code systems and value sets."""

import sys
from typing import Optional

from rich.console import Console
from rich.table import Table

console = Console()


def list_code_systems_command(
    search: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    List all available code systems with their OIDs.

    Args:
        search: Search term to filter code systems
        verbose: Show additional details like URLs and descriptions
    """
    from ccdakit.utils.code_systems import CodeSystemRegistry

    console.print("\n[bold cyan]Available Code Systems[/bold cyan]\n")

    # Get all code systems from the registry class attribute
    all_systems = CodeSystemRegistry.SYSTEMS

    # Filter if search term provided
    if search:
        search_lower = search.lower()
        filtered = {
            k: v
            for k, v in all_systems.items()
            if search_lower in k.lower() or search_lower in v.get("name", "").lower()
        }
        if not filtered:
            console.print(f"[red]No code systems found matching '{search}'[/red]")
            sys.exit(1)
        systems = filtered
    else:
        systems = all_systems

    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Code System", style="cyan", no_wrap=True)
    table.add_column("OID", style="yellow")

    if verbose:
        table.add_column("Description", style="dim")

    # Add rows
    for code, info in sorted(systems.items()):
        oid = info.get("oid", "N/A")
        if verbose:
            description = info.get("description", info.get("name", ""))
            table.add_row(code, oid, description)
        else:
            table.add_row(code, oid)

    console.print(table)
    console.print(f"\n[bold green]Total:[/bold green] {len(systems)} code systems")

    if not verbose:
        console.print("[dim]Tip: Use --verbose for more details[/dim]")

    # Show value sets as well
    console.print("\n[bold cyan]Available Value Sets[/bold cyan]\n")

    try:
        from ccdakit.utils.value_sets import ValueSetRegistry

        value_sets = ValueSetRegistry.VALUE_SETS

        vs_table = Table(show_header=True, header_style="bold magenta")
        vs_table.add_column("Value Set", style="cyan")
        vs_table.add_column("OID", style="yellow")

        if verbose:
            vs_table.add_column("Description", style="dim")

        for vs_code, vs_info in sorted(value_sets.items()):
            vs_oid = vs_info.get("oid", "N/A")
            if verbose:
                vs_desc = vs_info.get("description", vs_info.get("name", ""))
                vs_table.add_row(vs_code, vs_oid, vs_desc)
            else:
                vs_table.add_row(vs_code, vs_oid)

        console.print(vs_table)
        console.print(f"\n[bold green]Total:[/bold green] {len(value_sets)} value sets\n")

    except (ImportError, AttributeError):
        console.print("[yellow]Value set registry not available[/yellow]\n")
