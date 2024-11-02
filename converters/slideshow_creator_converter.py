from .base_converter import BaseConverter
from moviepy.editor import ImageClip, CompositeVideoClip, concatenate_videoclips
from rich.console import Console
from rich.table import Table
import os
import time

console = Console()

class SlideshowCreatorConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Creates a slideshow from images in the directory and adds it to the clip.
        If no clip is provided, creates a new video clip from the images.
        """
        console.print("[bold blue]🚀 Starting Slideshow Creation...[/bold blue]")
        image_files = [
            os.path.join(self.directory, f) for f in os.listdir(self.directory)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.webp'))
        ]

        if not image_files:
            console.print(f"[red]❌ No image files found in directory: {self.directory}[/red]")
            raise FileNotFoundError(f"No image files found in directory: {self.directory}")

        height = self.config.get('slideshow', {}).get('height', 1024)  # Default image height to 1024
        console.print(f"[cyan]🖼️ Image height set to: {height} pixels[/cyan]")

        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 1.0)  # Default fade-in to 1.0 seconds
        fade_out_duration = transition_config.get('fade_out', 1.0)  # Default fade-out to 1.0 seconds

        console.print(f"[cyan]🌟 Transition fade-in duration: {fade_in_duration}s, fade-out duration: {fade_out_duration}s[/cyan]")

        duration_per_image = self.config.get('slideshow', {}).get('duration', None)
        if duration_per_image is None:
            total_duration = clip.duration if clip else None
            if total_duration:
                duration_per_image = max(total_duration / len(image_files), 2)  # Minimum duration of 2 seconds per image
                console.print(f"[cyan]⏱️ Calculated duration per image: {duration_per_image} seconds based on total clip duration[/cyan]")
            else:
                duration_per_image = 2  # Default duration if not specified, minimum 2 seconds
                console.print(f"[cyan]⏱️ Default duration per image set to minimum: {duration_per_image} seconds[/cyan]")
        else:
            console.print(f"[cyan]⏱️ Using specified duration per image: {duration_per_image} seconds[/cyan]")

        # Initialize table for detailed image information
        table = Table(title="Slideshow Image Details")
        table.add_column("No.", style="bold magenta")
        table.add_column("Filename", style="cyan")
        table.add_column("Original Size (WxH)", style="green")
        table.add_column("Resized Size (WxH)", style="yellow")
        table.add_column("Start Time (s)", style="blue")
        table.add_column("Duration (s)", style="red")

        image_clips = []

        for index, image_file in enumerate(image_files, start=1):
            image_clip = ImageClip(image_file)
            original_size = (image_clip.w, image_clip.h)

            if image_clip.h != height:
                new_width = int(image_clip.w * (height / image_clip.h))
                image_clip = image_clip.resize(height=height)
                resized_size = (new_width, height)
                console.print(f"[yellow]🔄 Resizing image {os.path.basename(image_file)} from {original_size} to {resized_size} pixels[/yellow]")
            else:
                resized_size = original_size

            image_clip = image_clip.set_duration(duration_per_image)
            image_clip = image_clip.fadein(fade_in_duration).fadeout(fade_out_duration)
            image_clips.append(image_clip)

            table.add_row(
                str(index),
                os.path.basename(image_file),
                f"{original_size[0]}x{original_size[1]}",
                f"{resized_size[0]}x{resized_size[1]}",
                time.strftime('%M:%S', time.gmtime((index - 1) * duration_per_image)),  # Start time based on order in slideshow
                str(duration_per_image)
            )

        console.print(table)

        # slideshow = CompositeVideoClip(image_clips, size=(image_clips[0].w, image_clips[0].h))
        slideshow = concatenate_videoclips(image_clips, method="compose")
        console.print("[bold blue]✅ Slideshow created successfully.[/bold blue]")

        if clip is None:
            console.print("[yellow]⚠️ No existing clip provided. Returning slideshow as new clip.[/yellow]")
            return slideshow

        console.print("[green]🛠️ Overlaying slideshow onto existing clip.[/green]")
        if clip.h != image_clips[0].h or clip.w != image_clips[0].w:
            original_clip_size = (clip.w, clip.h)
            clip = clip.resize(height=image_clips[0].h).crop(0, 0, width=image_clips[0].w, height=image_clips[0].h)
            resized_clip_size = (clip.w, clip.h)
            console.print(f"[yellow]🔄 Cropping and resizing incoming clip from {original_clip_size} to {resized_clip_size} pixels[/yellow]")
        updated_clip = CompositeVideoClip([clip, slideshow.set_duration(clip.duration)])
        console.print("[bold blue]🎉 Slideshow added to existing clip successfully.[/bold blue]")
        return updated_clip
