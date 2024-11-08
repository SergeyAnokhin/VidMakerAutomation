from .base_converter import BaseConverter
from moviepy.editor import TextClip, CompositeVideoClip
from rich.console import Console

console = Console()

class TextOverlayConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Adds a text overlay to each video clip in the list.
        If no clips are provided, raises an error.
        """
        if not clip:
            console.print(f"[red]No existing clips found. Cannot add text overlay without clips.[/red]")
            raise ValueError("No existing clips found to add text overlay.")

        console.print(f"[bold blue]Processing Text Overlay:[/bold blue] Adding text overlay to clips")
        text = self.config.get('text', 'Default Text')
        start_time = self.config.get('start_time', 0)
        end_time = self.config.get('end_time', clip.duration)
        position = self.config.get('position', {'x': '10pt', 'y': '10pt'})
        font = self.config.get('font', {'name': 'Arial', 'size': 24, 'color': 'white'})
        contour = self.config.get('contour', {'color': 'black', 'size': 2})

        clip_height = clip.size[1]
        factor = clip_height / 1024
        font_size = font['size'] * factor


        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 0.0)  # Default fade-in to 0.0 seconds
        fade_out_duration = transition_config.get('fade_out', 0.0)  # Default fade-out to 0.0 seconds

        # Log all text properties to console
        console.print(f"[cyan]Text properties:[/cyan] Text: '{text}', Position: ({position['x']}, {position['y']}), Font: {font['name']}, Size: {font['size']}, Color: {font['color']}, Contour Color: {contour['color']}, Contour Size: {contour['size']}, Fade In: {fade_in_duration}s, Fade Out: {fade_out_duration}s")

        text_clip = TextClip(
            text,
            fontsize=font_size,
            color=font['color'],
            font=font['name'],
            stroke_color=contour['color'],
            stroke_width=contour['size']
        ).set_position((position['x'], position['y'])) \
        .set_end(end_time) \
        .set_start(start_time) \
        .fadein(fade_in_duration) \
        .fadeout(fade_out_duration)

        updated_clip = CompositeVideoClip([clip, text_clip])
        updated_clip.filename = clip.filename
        self.log.log(f"[green]Adding text overlay to clip with duration {clip.duration} seconds.[/green]")
        return updated_clip
