from .base_converter import BaseConverter
from moviepy.editor import CompositeVideoClip
from rich.console import Console

console = Console()

class SplitConverter(BaseConverter):
    def process(self, clips, metadata):
        """
        Splits the input video clip into multiple parts as defined in the configuration.
        If no clips are provided, raises an error.
        """
        if not clips:
            console.print(f"[red]No existing clips found. Cannot split video without clips.[/red]")
            raise ValueError("No existing clips found to split.")

        console.print(f"[bold blue]Processing Split Converter:[/bold blue] Splitting clips")
        num_parts = self.config.get('parts', 3)  # Default to 3 parts if not specified
        split_clips = []

        for clip in clips:
            duration = clip.duration / num_parts
            console.print(f"[green]Splitting clip with duration {clip.duration} seconds into {num_parts} parts, each part duration: {duration} seconds.[/green]")
            split_clips.extend([clip.subclip(i * duration, (i + 1) * duration) for i in range(num_parts)])

        return split_clips

    def convert(self, clip, metadata):
        # not used
        pass