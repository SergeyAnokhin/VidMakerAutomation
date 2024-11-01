from base_converter import BaseConverter
from moviepy.editor import ImageSequenceClip, CompositeVideoClip
import os
from rich.console import Console

console = Console()

class SlideshowCreatorConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Creates a slideshow from images found in the directory.
        If no clips are provided, creates a new slideshow clip.
        """
        console.print(f"[bold blue]Processing directory:[/bold blue] {self.directory}")
        image_files = sorted(
            [os.path.join(self.directory, f) for f in os.listdir(self.directory) if f.endswith(('.png', '.jpg', '.jpeg', '.jfif', '.webp'))]
        )

        if not image_files:
            console.print(f"[red]No image files found in directory: {self.directory}[/red]")
            raise FileNotFoundError("No image files found in directory.")

        console.print(f"[green]Found {len(image_files)} image files. Creating slideshow...[/green]")

        slideshow_config = self.config.get('slideshow', {})
        height = slideshow_config.get('height', 720)  # Default height to 720 if not specified

        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 1.0)  # Default fade-in to 1.0 seconds
        fade_out_duration = transition_config.get('fade_out', 1.0)  # Default fade-out to 1.0 seconds

        duration = self.config.get('duration', 2)  # Default to 2 seconds per image
        slideshow_clip = ImageSequenceClip(image_files, durations=[duration] * len(image_files))
        slideshow_clip = slideshow_clip.resize(height=height).fadein(fade_in_duration).fadeout(fade_out_duration)

        # If clips are empty or None, create a new clip
        if not clips:
            console.print("[yellow]No existing clips found. Creating a new slideshow clip.[/yellow]")
            clips = [slideshow_clip]
        else:
            console.print("[cyan]Adding slideshow to existing clips.[/cyan]")
            # Add slideshow to the existing clips
            updated_clips = []
            for clip in clips:
                updated_clips.append(CompositeVideoClip([clip, slideshow_clip.set_duration(clip.duration)]))
            clips = updated_clips
        
        return clips
