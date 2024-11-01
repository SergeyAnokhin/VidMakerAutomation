from base_converter import BaseConverter
from moviepy.editor import AudioFileClip, ColorClip
import os

class AudioReaderConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Reads an audio file from the directory and returns it as an audio clip.
        If an audio clip already exists, replaces the audio track with the new one.
        If no clips are provided, creates a new clip with the audio.
        """
        audio_file = None
        for file in os.listdir(self.directory):
            if file.endswith('.mp3'):
                audio_file = os.path.join(self.directory, file)
                break

        if audio_file is None:
            raise FileNotFoundError("No mp3 file found in directory.")

        audio_clip = AudioFileClip(audio_file)

        # If clips are empty or None, create a new video clip
        if not clips:
            new_clip = ColorClip(size=(640, 480), color=(0, 0, 0), duration=audio_clip.duration)
            new_clip = new_clip.set_audio(audio_clip)
            clips = [new_clip]
        else:
            # Add audio to all existing clips
            updated_clips = []
            for clip in clips:
                updated_clips.append(clip.set_audio(audio_clip))
            clips = updated_clips

        return clips
