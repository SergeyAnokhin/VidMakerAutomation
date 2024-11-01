from base_converter import BaseConverter
from moviepy.editor import TextClip, CompositeVideoClip
from rich.console import Console

console = Console()

class TextOverlayConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Adds a text overlay to each video clip in the list.
        If no clips are provided, raises an error.
        """
        if not clips:
            console.print(f"[red]No existing clips found. Cannot add text overlay without clips.[/red]")
            raise ValueError("No existing clips found to add text overlay.")

        console.print(f"[bold blue]Processing Text Overlay:[/bold blue] Adding text overlay to clips")
        text = self.config.get('text', 'Default Text')
        position = self.config.get('position', {'x': '10pt', 'y': '10pt'})
        font = self.config.get('font', {'name': 'Arial', 'size': 24, 'color': 'white'})
        contour = self.config.get('contour', {'color': 'black', 'size': 2})

        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 0.0)  # Default fade-in to 0.0 seconds
        fade_out_duration = transition_config.get('fade_out', 0.0)  # Default fade-out to 0.0 seconds

        text_clip = TextClip(
            text,
            fontsize=font['size'],
            color=font['color'],
            font=font['name'],
            stroke_color=contour['color'],
            stroke_width=contour['size']
        ).set_position((position['x'], position['y'])).fadein(fade_in_duration).fadeout(fade_out_duration)

        updated_clips = []
        for clip in clips:
            console.print(f"[green]Adding text overlay to clip with duration {clip.duration} seconds.[/green]")
            updated_clips.append(CompositeVideoClip([clip, text_clip.set_duration(clip.duration)]))
        return updated_clips
