import tool
from .base_converter import BaseConverter
from moviepy.editor import AudioFileClip, ColorClip
from rich.console import Console
import os

console = Console()

class AudioReaderConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Reads an audio file from the directory and adds it to the clip.
        If no clip is provided, creates a new audio clip from the audio file.
        """
        self.log.log("[bold blue]🎵 Starting Audio Reading...[/bold blue]")
        audio_files = [
            os.path.join(self.directory, f) for f in os.listdir(self.directory)
            if f.lower().endswith(('.mp3', '.wav', '.aac'))
        ]

        if not audio_files:
            self.log.error(f"No audio files found in directory: {self.directory}")
            raise FileNotFoundError(f"No audio files found in directory: {self.directory}")

        if len(audio_files) > 1:
            self.log.warn(f"Multiple audio files found in directory: {self.directory}. Using the first one found.")

        audio_file = audio_files[0]
        
        start_time = self.config.get('start_time', 0)
        end_time = self.config.get('end_time', None)

        # Load audio with start and end times if specified
        if start_time != 0 or end_time is not None:
            self.log.log(f"[cyan]✂️ Cropping audio from {start_time} to {end_time} seconds[/cyan]")
            audio_clip = AudioFileClip(audio_file).subclip(start_time, end_time)
        else:
            audio_clip = AudioFileClip(audio_file)

        self.log.log(f"[cyan]🔊 Audio file loaded: {audio_file} with duration {tool.transform_to_MMSS(audio_clip.duration)} seconds[/cyan]")

        if clip is None:
            self.log.warn("No existing video clip provided. Returning audio as new clip.")
            clip = ColorClip(size=(1024, 1024), color=(0, 0, 0), duration=audio_clip.duration)
        else:
            self.log.log("[green]🛠️ Adding audio to existing video clip.[/green]")

        return clip.set_audio(audio_clip)
