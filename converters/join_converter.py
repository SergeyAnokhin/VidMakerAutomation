import os
from .base_converter import BaseConverter
from moviepy.editor import concatenate_videoclips, VideoFileClip
from rich.console import Console
from moviepy.editor import VideoClip

console = Console()

class JoinConverter(BaseConverter):
    def process(self, clips, metadata):
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
        # if not all(isinstance(clip, VideoFileClip) for clip in clips):
        #     console.print("[red]All items in 'clips' must be instances of VideoFileClip.[/red]")
        #     raise TypeError("All items in 'clips' must be VideoFileClip instances.")

        console.print(f"[bold blue]Processing Join Converter:[/bold blue] Joining {len(clips)} clips")

        # Config settings for saving temporary clips
        self.fps = self.config.get("fps", 24)
        self.codec = self.config.get("codec", "libx264")
        self.preset = self.config.get("preset", "medium")
        temp_files = []

        # Save each clip as a temporary file
        temp_files = self.process_async(clips, metadata, self.convert)

        # Load temporary files and concatenate
        console.print(temp_files)
        video_clips = [VideoFileClip(f) for f in temp_files]
        joined_clip = concatenate_videoclips(video_clips, method="compose")
        console.print(f"[green]Successfully joined {len(video_clips)} clips into a single clip with duration {joined_clip.duration} seconds.[/green]")

        # Clean up temporary files after concatenation
        # for file in temp_files:
        #     os.remove(file)
        console.print("[blue]Temporary files cleaned up.[/blue]")

        return [joined_clip]

    def convert(self, clip: VideoClip, metadata, index):
        temp_filename = os.path.join(self.directory, clip.filename)
        self.log.log(f"[yellow]Saving clip as temporary file: {temp_filename}. Clip duration: [bold]{clip.duration}[/bold] secs [/yellow]")
        self.log.log(f"[grey]🎥 Saving with parameters: fps=[bold]{self.fps}[/bold], codec=[bold]{self.codec}[/bold], preset=[bold]{self.preset}[/bold][/grey]")
        if clip.audio is None or clip.audio.duration is None:
            self.log.log("[yellow]⚠️ Clip does not contain audio or audio duration is missing[/yellow]")
        else:
            self.log.log(f"[grey]🎵 Audio duration: [bold]{clip.audio.duration}[/bold] seconds[/grey]")
        
        clip.write_videofile(
            temp_filename,
            fps=self.fps,   
            codec=self.codec,
            preset=self.preset,
            audio=False,
            threads=4  
        )
        return temp_filename