from .base_converter import BaseConverter
from rich.console import Console
import tool
from moviepy.editor import VideoClip
from model import AudioPart

console = Console()

class SplitConverter(BaseConverter):
    def process(self, clips: list[VideoClip], metadata):
        """
        Splits the input video clip into multiple parts as defined in the configuration.
        If no clips are provided, raises an error.
        """
        if not clips:
            self.log.error(f"[red]No existing clips found. Cannot split video without clips.[/red]")
            raise ValueError("No existing clips found to split.")

        self.log.log(f"[bold blue]Processing Split Converter:[/bold blue] Splitting clips")
        num_parts = self.config.get('parts', 3)  # Default to 3 parts if not specified
        split_clips = []
        metadata["parts"] = num_parts
        metadata["audio_parts"] = []

        for clip in clips:
            duration = clip.duration / num_parts
            self.log.log(f"[green]Splitting clip with duration {clip.duration} seconds into {num_parts} parts, each part duration: {duration} seconds.[/green]")
            for i in range(num_parts):
                start_time, end_time = tool.get_segment_duration(clip.duration, i, num_parts)
                subclip: VideoClip = clip.subclip(start_time, end_time)
                self.log.log(f"[green]Subclip [bold]{i+1}[/bold] created with duration [{tool.transform_to_MMSS(subclip.duration)}] seconds. Period: [bold]{tool.transform_to_MMSS(start_time)} - {tool.transform_to_MMSS(end_time)}[/bold][/green]")
                subclip.filename = f"subclip_{i+1}.avi"
                metadata["audio_parts"].append(AudioPart(start_time, end_time, clip.audio.clips[0].filename))
                split_clips.append(subclip)

        return split_clips

    def convert(self, clip, metadata):
        # not used
        pass