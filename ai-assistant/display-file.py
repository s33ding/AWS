from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path

def display_file(path="/tmp/ai-assistant.txt"):
    console = Console()

    file = Path(path)
    if not file.exists():
        console.print(f"[red]❌ File not found:[/red] {path}")
        return

    content = file.read_text()

    console.print(Panel.fit(f"📁 Output saved to: [green]{path}[/green]", style="bold cyan"))
    console.print(Markdown(content))

if __name__ == "__main__":
    display_file()

