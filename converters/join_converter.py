from .base_converter import BaseConverter
from moviepy.editor import concatenate_videoclips
from rich.console import Console

console = Console()

class JoinConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Joins multiple video clips into a single video clip.
        If no clips are provided, raises an error.
        """
        if not clips:
            console.print(f"[red]No existing clips found. Cannot join clips without input.[/red]")
            raise ValueError("No existing clips found to join.")

        console.print(f"[bold blue]Processing Join Converter:[/bold blue] Joining {len(clips)} clips")
        joined_clip = concatenate_videoclips(clips)
        console.print(f"[green]Successfully joined {len(clips)} clips into a single clip with duration {joined_clip.duration} seconds.[/green]")

        return [joined_clip]
