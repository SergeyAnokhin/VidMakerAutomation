from .base_converter import BaseConverter
from moviepy.editor import CompositeVideoClip
from rich.console import Console
import os

console = Console()

class VideoExportConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Exports the final video clip to a file.
        If no clips are provided, raises an error.
        """
        if not clips:
            console.print(f"[red]No existing clips found. Cannot export video without clips.[/red]")
            raise ValueError("No existing clips found to export.")

        console.print(f"[bold blue]Processing Video Export:[/bold blue] Exporting final video")
        # Search for an mp3 file in the directory and use its name for the output file
        audio_file = None
        for file in os.listdir(self.directory):
            if file.endswith('.mp3'):
                audio_file = os.path.splitext(file)[0]  # Get the file name without extension
                break

        if audio_file is None:
            console.print(f"[red]No mp3 file found in directory: {self.directory}. Cannot determine output file name.[/red]")
            raise FileNotFoundError("No mp3 file found in directory.")

        output_path = os.path.join(self.directory, f"{audio_file}.mp4")
        fps = self.config.get('export', {}).get('fps', 24)  # Default FPS to 24
        codec = self.config.get('export', {}).get('codec', 'libx264')  # Default codec to 'libx264'
        quality_preset = self.config.get('export', {}).get('quality_preset', 'medium')  # Default quality preset

        final_clip = CompositeVideoClip(clips)
        console.print(f"[green]Exporting video to {output_path} with FPS: {fps}, Codec: {codec}, Quality: {quality_preset} 🎬✨[/green]")
        final_clip.write_videofile(output_path, fps=fps, codec=codec, preset=quality_preset)

        return clips
