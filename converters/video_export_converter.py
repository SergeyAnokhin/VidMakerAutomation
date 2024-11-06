from .base_converter import BaseConverter
from moviepy.editor import CompositeVideoClip
import os
import time

class VideoExportConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Exports the final video clip to a file.
        If no clip is provided, raises an error.
        """
        if clip is None:
            raise ValueError("No clip provided for export.")

        # Search for an mp3 file in the directory to determine the output file name
        audio_file = None
        for file in os.listdir(self.directory):
            if file.endswith('.mp3'):
                audio_file = os.path.splitext(file)[0]  # Get the file name without extension
                break

        if audio_file is None:
            raise FileNotFoundError(f"No mp3 file found in directory: {self.directory}. Cannot determine output file name.")

        output_path = os.path.join(self.directory, f"{audio_file}.mp4")

        # If the output file already exists, append a random timestamp to the file name
        if os.path.exists(output_path):
            timestamp = time.strftime("%H_%M_%S", time.localtime())
            output_path = os.path.join(self.directory, f"{audio_file}_{timestamp}.mp4")

        fps = self.config.get('quality', {}).get('fps', 24)  # Default FPS to 24
        codec = self.config.get('quality', {}).get('codec', 'libx264')  # Default codec to 'libx264'
        quality_preset = self.config.get('quality', {}).get('preset', 'medium')  # Default quality preset

        # Log exporting details
        self.log.log(f"[green]Exporting video to {output_path} with FPS: {fps}, Codec: {codec}, Quality: {quality_preset}[/green]")

        # clip = CompositeVideoClip([clip, metadata['right'], metadata['left']])

        # Export the video clip
        clip.write_videofile(output_path, fps=fps, codec=codec, preset=quality_preset, threads=4)

        return clip
