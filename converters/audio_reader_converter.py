from .base_converter import BaseConverter
from moviepy.editor import AudioFileClip, ColorClip
import os
import time

class AudioReaderConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Reads an audio file from the directory and returns it as an audio clip.
        If an audio clip already exists, replaces the audio track with the new one.
        If no clip is provided, creates a new video clip with a solid color and adds the audio to it.
        """
        audio_file = None
        for file in os.listdir(self.directory):
            if file.endswith('.mp3'):
                audio_file = os.path.join(self.directory, file)
                break

        if audio_file is None:
            raise FileNotFoundError(f"No mp3 file found in directory: {self.directory}")

        start_time = self.config.get('start_time', None)
        end_time = self.config.get('end_time', None)

        # Load audio with start and end times if specified
        if start_time is not None or end_time is not None:
            audio_clip = AudioFileClip(audio_file).subclip(start_time, end_time)
        else:
            audio_clip = AudioFileClip(audio_file)

        # If clip is None, create a new one
        if clip is None:
            new_clip = ColorClip(size=(640, 480), color=(0, 0, 0), duration=audio_clip.duration)
            new_clip = new_clip.set_audio(audio_clip)
            return new_clip
        else:
            # Add audio to the existing clip
            updated_clip = clip.set_audio(audio_clip)
            return updated_clip
