from .base_converter import BaseConverter
from moviepy.editor import ImageClip, CompositeVideoClip
from rich.console import Console
import os
import traceback

console = Console()

class SlideshowCreatorConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Creates a slideshow from images in the directory and adds it to the clips.
        If no clips are provided, creates a new video clip from the images.
        """
        console.print(f"[bold blue]Processing Slideshow Creator:[/bold blue] Creating slideshow from images")

        image_files = [
            os.path.join(self.directory, f) for f in os.listdir(self.directory)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.webp'))
        ]

        if not image_files:
            console.print(f"[red]No image files found in directory: {self.directory}[/red]")
            raise FileNotFoundError("No image files found in directory.")

        height = self.config.get('slideshow', {}).get('height', 1024)  # Default image height to 1024
        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 1.0)  # Default fade-in to 1.0 seconds
        fade_out_duration = transition_config.get('fade_out', 1.0)  # Default fade-out to 1.0 seconds

        image_clips = []
        total_duration = self.config.get('slideshow', {}).get('duration', None)
        if total_duration:
            duration_per_image = max(total_duration / len(image_files), 2)  # Minimum duration of 2 seconds per image
        else:
            duration_per_image = 2  # Default duration if not specified, minimum 2 seconds

        for image_file in image_files:
            console.print(f"[cyan]Adding image {os.path.basename(image_file)} to slideshow with height: {height} pixels[/cyan]")
            image_clip = ImageClip(image_file)
            if image_clip.h != height:
                console.print(f"[yellow]Resizing image {os.path.basename(image_file)} to height: {height} pixels[/yellow]")
                image_clip = image_clip.resize(height=height)
            image_clip = image_clip.set_duration(duration_per_image)

            image_clip = image_clip.fadein(fade_in_duration).fadeout(fade_out_duration)
            image_clips.append(image_clip)

        slideshow = CompositeVideoClip(image_clips, size=(image_clips[0].w, image_clips[0].h))

        # If no existing clips, return slideshow as the only clip
        if not clips:
            console.print("[yellow]No existing clips found. Creating a new slideshow clip.[/yellow]")
            return [slideshow]

        # Add slideshow to all existing clips
        updated_clips = []
        for clip in clips:
            console.print(f"[green]Adding slideshow to existing clip with duration {clip.duration} seconds.[/green]")
            updated_clips.append(CompositeVideoClip([clip, slideshow.set_duration(clip.duration)]))

        return updated_clips
