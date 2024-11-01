from .base_converter import BaseConverter
from moviepy.editor import AudioFileClip, ColorClip
from rich.console import Console
import os
import traceback

console = Console()

class AudioReaderConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Reads an audio file from the directory and returns it as an audio clip.
        If an audio clip already exists, replaces the audio track with the new one.
        If no clips are provided, creates a new video clip with a solid color and adds the audio to it.
        """
        console.print(f"[bold blue]Processing Audio Reader:[/bold blue] Adding audio to clips")
        audio_file = None
        for file in os.listdir(self.directory):
            if file.endswith('.mp3'):
                audio_file = os.path.join(self.directory, file)
                break

        if audio_file is None:
            console.print(f"[red]No mp3 file found in directory: {self.directory}[/red]")
            raise FileNotFoundError("No mp3 file found in directory.")

        start_time = self.config.get('start_time', None)
        end_time = self.config.get('end_time', None)

        # Load audio with start and end times if specified
        if start_time is not None or end_time is not None:
            console.print(f"[cyan]Applying audio subclip from {start_time}s to {end_time}s 🎵✨[/cyan]")
            audio_clip = AudioFileClip(audio_file).subclip(start_time, end_time)
        else:
            audio_clip = AudioFileClip(audio_file)

        # Log audio file name and duration
        formatted_duration = f"{int(audio_clip.duration // 60)}:{int(audio_clip.duration % 60):02d}"
        console.print(f"[magenta]Found audio file: {os.path.basename(audio_file)} with duration: {formatted_duration} minutes[/magenta]")

        # If clips are empty or None, create a new clip
        if not clips:
            console.print("[yellow]No existing clips found. Creating a new video clip with audio.[/yellow]")
            new_clip = ColorClip(size=(640, 480), color=(0, 0, 0), duration=audio_clip.duration)
            new_clip = new_clip.set_audio(audio_clip)
            clips = [new_clip]
        else:
            # Add audio to all existing clips
            updated_clips = []
            for clip in clips:
                console.print(f"[green]Adding audio to existing clip with duration {clip.duration} seconds.[/green]")
                updated_clips.append(clip.set_audio(audio_clip))
            clips = updated_clips

        return clips
