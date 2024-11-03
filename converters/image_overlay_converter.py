from .base_converter import BaseConverter
from moviepy.editor import ImageClip, CompositeVideoClip, VideoFileClip
from moviepy.video.fx import all as vfx
from rich.console import Console
import os

console = Console()

class ImageOverlayConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Adds an image overlay to each video clip in the list.
        If no clips are provided, raises an error.
        """
        if not clip:
            self.log.error("No existing clips found. Cannot add image overlay without clips.")
            raise ValueError("No existing clips found to add image overlay.")

        self.log.log("[bold blue]🖼️ Processing Image Overlay: Adding image overlay to clips[/bold blue]")
        image_path = self.config.get('image', {}).get('path')
        if not image_path or not os.path.exists(image_path):
            self.log.error(f"Image file not found or path not specified: {image_path}")
            raise FileNotFoundError("Image file not found or path not specified.")

        resize = self.config.get('image', {}).get('resize', 1)
        position = self.config.get('image', {}).get('position', {'x': 'left', 'y': 'bottom'})
        timing = self.config.get('timing', {})
        start_time = timing.get('start_time', 0)
        duration = timing.get('duration', None)

        updated_clip = self.add_gif(
            gif_file=image_path,
            audio_duration=clip.duration,
            slideshow=clip,
            resize=resize,
            start_time=start_time,
            duration=duration,
            position=position
        )

        return updated_clip

    def add_gif(self, gif_file, audio_duration, slideshow, resize=1, start_time=-32, duration=None, position=None):
        if not gif_file or not os.path.isfile(gif_file):
            return slideshow
            
        has_mask = False
        
        if duration is None:
            if start_time < 0:
                duration = -start_time
            else:
                duration = (8.0 * 2.0)

        if start_time < 0:
            start_time = max(0, audio_duration + start_time)
            
        if position is None:
            position = ("left", "bottom")
        else:
            def convert_position(value):
                if isinstance(value, str):
                    if value.endswith('pt'):
                        return int(value.replace('pt', ''))
                    elif value.endswith('%'):
                        return float(value.replace('%', '')) / 100
                    elif value == 'center':
                        return 'center'
                return value
                
            x_pos = convert_position(position['x'])
            y_pos = convert_position(position['y'])
            position = (x_pos, y_pos)
        
        gif_clip = (
            VideoFileClip(gif_file, has_mask)
            .loop(duration=duration)
            .resize(resize * 0.5)
            .with_position(position)
            .with_start(start_time)
        )

        self.log.log(f"GIF: Duration: {start_time:3.0f} -> {start_time + duration:3.0f} secs")
        gif_clip = gif_clip.fx(vfx.mask_color, color=[0, 0, 0], threshold=100, stiffness=5)
        final_video = CompositeVideoClip([slideshow, gif_clip])
        return final_video
