from .base_converter import BaseConverter
from moviepy.editor import ImageClip, CompositeVideoClip
from rich.console import Console
import os

console = Console()

class ImageOverlayConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Adds an image overlay to each video clip in the list.
        If no clips are provided, raises an error.
        """
        if not clips:
            console.print(f"[red]No existing clips found. Cannot add image overlay without clips.[/red]")
            raise ValueError("No existing clips found to add image overlay.")

        console.print(f"[bold blue]Processing Image Overlay:[/bold blue] Adding image overlay to clips")
        image_path = self.config.get('image', {}).get('path')
        if not image_path or not os.path.exists(image_path):
            console.print(f"[red]Image file not found or path not specified: {image_path}[/red]")
            raise FileNotFoundError("Image file not found or path not specified.")

        position = self.config.get('position', {'x': '10pt', 'y': '10pt'})
        timing = self.config.get('timing', {})
        start_time = timing.get('start_time', 0)
        end_time = timing.get('end_time', None)

        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 0.0)  # Default fade-in to 0.0 seconds
        fade_out_duration = transition_config.get('fade_out', 0.0)  # Default fade-out to 0.0 seconds

        image_clip = ImageClip(image_path).set_position((position['x'], position['y']))
        if end_time:
            image_clip = image_clip.set_duration(end_time - start_time)

        image_clip = image_clip.fadein(fade_in_duration).fadeout(fade_out_duration)

        updated_clips = []
        for clip in clips:
            console.print(f"[green]Adding image overlay to clip with duration {clip.duration} seconds.[/green]")
            updated_clips.append(CompositeVideoClip([clip, image_clip.set_start(start_time).set_duration(clip.duration)]))
        return updated_clips
