import os
from .base_converter import BaseConverter
from moviepy.editor import concatenate_videoclips, VideoFileClip
from rich.console import Console
import tempfile

console = Console()

class JoinConverter(BaseConverter):
    def convert(self, clips, metadata):
        """
        Joins multiple video clips into a single video clip by first saving
        each clip as a temporary file using specified config settings, and then 
        concatenating them into one final clip.
        
        Parameters:
            clips (list): A list of VideoClip objects to be joined.
            metadata (dict): Metadata related to the video processing, if any.

        Returns:
            VideoFileClip: The final concatenated clip.

        Raises:
            ValueError: If no clips are provided.
            TypeError: If any items in clips are not VideoClip instances.
        """
        
        if not clips:
            console.print("[red]No existing clips found. Cannot join clips without input.[/red]")
            raise ValueError("No existing clips found to join.")

        # Verify each clip is a VideoClip instance
        if not all(isinstance(clip, VideoFileClip) for clip in clips):
            console.print("[red]All items in 'clips' must be instances of VideoFileClip.[/red]")
            raise TypeError("All items in 'clips' must be VideoFileClip instances.")

        console.print(f"[bold blue]Processing Join Converter:[/bold blue] Joining {len(clips)} clips")

        # Config settings for saving temporary clips
        fps = self.config.get("fps", 24)
        codec = self.config.get("codec", "libx264")
        bitrate = self.config.get("bitrate", "2000k")
        preset = self.config.get("preset", "medium")
        temp_dir = tempfile.mkdtemp()
        temp_files = []

        # Save each clip as a temporary file
        for idx, clip in enumerate(clips):
            temp_filename = os.path.join(temp_dir, f"temp_clip_{idx}.mp4")
            console.print(f"[yellow]Saving clip {idx+1} as temporary file: {temp_filename}[/yellow]")
            
            clip.write_videofile(
                temp_filename,
                fps=fps,
                codec=codec,
                bitrate=bitrate,
                preset=preset,
                threads=4  
            )
            temp_files.append(temp_filename)

        # Load temporary files and concatenate
        video_clips = [VideoFileClip(f) for f in temp_files]
        joined_clip = concatenate_videoclips(video_clips)
        console.print(f"[green]Successfully joined {len(video_clips)} clips into a single clip with duration {joined_clip.duration} seconds.[/green]")

        # Clean up temporary files after concatenation
        for file in temp_files:
            os.remove(file)
        console.print("[blue]Temporary files cleaned up.[/blue]")

        return joined_clip
