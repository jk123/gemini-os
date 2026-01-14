#!/bin/bash
COMMAND=$1

if [ "$COMMAND" == "status" ]; then
    python3 -c "
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console(force_terminal=True)
table = Table(title='System Status', border_style='beige')
table.add_column('Component', style='cyan')
table.add_column('Status', style='green')

table.add_row('WebUI', 'Online')
table.add_row('Rich Library', 'Active')
table.add_row('Memory', 'Stable')

console.print(Panel(table, border_style='beige'))
"
    exit 0
fi

echo "Suoritetaan: $COMMAND"
