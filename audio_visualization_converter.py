from base_converter import BaseConverter
from moviepy.editor import AudioFileClip, CompositeVideoClip
from moviepy.video.fx.all import colorx
from rich.console import Console
import os

console = Console()

class AudioVisualizationConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Adds an audio visualization overlay to each video clip in the list.
        If no clips are provided, raises an error.
        """
        if not clips:
            console.print(f"[red]No existing clips found. Cannot add audio visualization without clips.[/red]")
            raise ValueError("No existing clips found to add audio visualization.")

        console.print(f"[bold blue]Processing Audio Visualization:[/bold blue] Adding audio visualization to clips")
        audio_path = self.config.get('audio', {}).get('path')
        if not audio_path or not os.path.exists(audio_path):
            console.print(f"[red]Audio file not found or path not specified: {audio_path}[/red]")
            raise FileNotFoundError("Audio file not found or path not specified.")

        bar_count = self.config.get('visualization', {}).get('bar_count', 30)  # Default bar count to 30
        height = self.config.get('visualization', {}).get('height', 150)  # Default visualization height to 150
        palette = self.config.get('visualization', {}).get('palette', 'COLORMAP_MAGMA')  # Default palette to 'COLORMAP_MAGMA'

        # Create an audio clip
        audio_clip = AudioFileClip(audio_path)

        # Placeholder for visualization (needs actual implementation for creating visual bars)
        visualization_clip = colorx(audio_clip.to_ImageClip(), 0.5).set_duration(audio_clip.duration)

        updated_clips = []
        for clip in clips:
            console.print(f"[green]Adding audio visualization to clip with duration {clip.duration} seconds.[/green]")
            updated_clips.append(CompositeVideoClip([clip, visualization_clip.set_duration(clip.duration)]))
        return updated_clips
