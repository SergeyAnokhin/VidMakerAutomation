import pprint
import tool
from .base_converter import BaseConverter
from moviepy.editor import ImageClip, CompositeVideoClip, concatenate_videoclips, VideoClip
from rich.console import Console
from rich.table import Table
import os
import time

console = Console()

class SlideshowCreatorConverter(BaseConverter):
    def convert(self, clip: VideoClip, metadata, index: int):
        """
        Creates a slideshow from images in the directory and adds it to the clip.
        If no clip is provided, creates a new video clip from the images.
        """
        self.log.log("[bold blue]🚀 Starting Slideshow Creation...[/bold blue]")
        
        image_files = [
            os.path.join(self.directory, f) for f in sorted(os.listdir(self.directory))
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.webp')) and not f.lower().startswith("cover")
        ]

        if not image_files:
            self.log.log(f"[red]❌ No image files found in directory: {self.directory}[/red]")
            raise FileNotFoundError(f"No image files found in directory: {self.directory}")

        total_duration = clip.duration if clip else None
        self.log.log(f"[cyan]🎞Input clip duration: ⏱️ {tool.transform_to_MMSS(total_duration)}[/cyan]")

        duration_per_image = self.config.get('slideshow', {}).get('duration', None)
        if duration_per_image is None:
            if total_duration:
                duration_per_image = max(total_duration / len(image_files), 2)  # Minimum duration of 2 seconds per image
                self.log.log(f"[cyan]⏱️ Calculated duration per image: {duration_per_image} seconds based on total clip duration[/cyan]")
            else:
                duration_per_image = 2  # Default duration if not specified, minimum 2 seconds
                self.log.log(f"[cyan]⏱️ Default duration per image set to minimum: {duration_per_image} seconds[/cyan]")
        else:
            self.log.log(f"[cyan]⏱️ Using specified duration per image: {duration_per_image} seconds[/cyan]")

        # Process images to generate clips
        image_clips = self._process_images(image_files, duration_per_image, total_duration)

        slideshow = concatenate_videoclips(image_clips, method="compose")
        self.log.log("[bold blue]✅ Slideshow created successfully.[/bold blue]")

        if clip is None:
            self.log.log("[yellow]⚠️ No existing clip provided. Returning slideshow as new clip.[/yellow]")
            return slideshow

        self.log.log("[green]🛠️ Overlaying slideshow onto existing clip.[/green]")

        # if width (image_clips[0].w) smaller tahn 720 display big error
        if image_clips[0].w < 720:
            self.log.log("[red]❌ Image width is too small. Minimum width is 720 pixels.[/red]")
            raise ValueError("Image width is too small. Minimum width is 720 pixels.")

        if clip.h != image_clips[0].h or clip.w != image_clips[0].w:
            original_clip_size = (clip.w, clip.h)
            self.log.log(f"[yellow]🔄 First image size ↔{image_clips[0].w} ↕{image_clips[0].h} pixels[/yellow]")
            if image_clips[0].w > clip.w:
                clip = clip.resize(width=image_clips[0].w).crop(0, 0, width=image_clips[0].w, height=image_clips[0].h)
            else:
                clip = clip.resize(height=image_clips[0].h).crop(0, 0, width=image_clips[0].w, height=image_clips[0].h)
            resized_clip_size = (clip.w, clip.h)
            self.log.log(f"[yellow]🔄 Resizing and cropping incoming clip from {original_clip_size} to {resized_clip_size} pixels[/yellow]")

        updated_clip = CompositeVideoClip([clip, slideshow.set_duration(clip.duration)])
        self.log.log("[bold blue]🎉 Slideshow added to existing clip successfully.[/bold blue]")
        return updated_clip

    def _process_images(self, image_files, duration_per_image, total_duration):
        """
        Processes images and creates individual clips for each image, adding them to the provided list.
        """
        
        transition_config = self.config.get('transition', {})
        fade_in_duration = transition_config.get('fade_in', 1.0)  # Default fade-in to 1.0 seconds
        fade_out_duration = transition_config.get('fade_out', 1.0)  # Default fade-out to 1.0 seconds
        fade_in_first_image = transition_config.get('fade_in_first_image', True)  # Default to True

        height = self.config.get('slideshow', {}).get('height', 1024)  # Default image height to 1024
        width = self.config.get('slideshow', {}).get('width', None)  # Default image width to 1024
        # ratio = self.config.get('slideshow', {}).get('ratio', "crop")  # Default to "crop"
        self.log.log(f"[cyan]🖼️ Image height set to: ↕{height} pixels[/cyan]")
        cover = self.config.get('cover', {})  
        cover_name = cover.get('name', None)  
        cover_duration = cover.get('duration', duration_per_image or 5)  
        self.log.log(f"[cyan]🖼 cover name: {cover_name} Duration: ⌛{cover_duration} [/cyan]")
        self.log.log(f"[cyan]🌟 Transition fade-in duration: ⬆{fade_in_duration}s, fade-out duration: ⬇{fade_out_duration}s[/cyan]")
        
        # Initialize table for detailed image information
        table = Table(title="Slideshow Image Details")
        table.add_column("No.", style="bold magenta")
        table.add_column("Filename", style="cyan")
        table.add_column("Original Size (WxH)", style="green")
        table.add_column("Resized Size (WxH)", style="yellow")
        table.add_column("Start Time", style="blue")
        table.add_column("Duration (s)", style="red")

        image_clips = []

        # Track when each image starts
        start_time = 0
        index = 1
        
        if cover_name is not None and len(cover_name) > 0:
            cover_file = [
                os.path.join(self.directory, f) for f in sorted(os.listdir(self.directory))
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif', '.webp')) and f.lower().startswith(cover_name)
            ]                
            if len(cover_file) == 1:
                result = self._process_image(cover_duration, total_duration, fade_in_duration, fade_out_duration, fade_in_first_image, height, width, table, start_time, index, cover_file[0])
                index += 1            
                start_time += cover_duration
                image_clips.append(result)
            
        
        # Cycle through images repeatedly until the total duration is reached
        while start_time < total_duration:
            for image_file in image_files:
                if start_time >= total_duration:
                    break

                result = self._process_image(duration_per_image, total_duration, fade_in_duration, fade_out_duration, 
                                             fade_in_first_image, height, width, table, start_time, index, image_file)
                index += 1            
                start_time += duration_per_image
                if result != None:
                    image_clips.append(result)
                
        self.log.print(table)
        return image_clips

    def _process_image(self, duration_per_image, total_duration, fade_in_duration, fade_out_duration, fade_in_first_image, 
                       height, width, table, start_time, index, image_file):
        image_clip = ImageClip(image_file)
        original_size = (image_clip.w, image_clip.h)
        result = None

                # Сначала изменяем размер по высоте
        if image_clip.h != height:
            new_width = int(image_clip.w * (height / image_clip.h))
            image_clip = image_clip.resize(height=height)
                    
                # Обрабатываем ширину
        if width is not None and image_clip.w != width:
            excess_width = image_clip.w - width
            if excess_width > 0:
                crop_left = excess_width // 2
                image_clip = image_clip.crop(x1=crop_left, width=width)
                self.log.log(f"[yellow]✂️ Cropping image {os.path.basename(image_file)} to width {width}[/yellow]")
            else:
                        # Добавляем черные полосы по бокам
                from moviepy.editor import ColorClip
                background = ColorClip(size=(width, height), color=(0,0,0))
                background = background.set_duration(duration_per_image)
                x_position = (width - image_clip.w) // 2
                image_clip = CompositeVideoClip([background, image_clip.set_position((x_position, 0))])
                self.log.log(f"[yellow]⬛ Adding black bars to image {os.path.basename(image_file)}[/yellow]")

        resized_size = (image_clip.w, image_clip.h)

                # Determine if the image fits within the total duration
        if start_time < total_duration:
                    # Image fits within the total duration
            image_clip = image_clip.set_duration(duration_per_image)
            if index == 1 and not fade_in_first_image:
                image_clip = image_clip.fadeout(fade_out_duration)
            else:
                image_clip = image_clip.fadein(fade_in_duration).fadeout(fade_out_duration)
            start_time_formatted = tool.transform_to_MMSS(start_time)
            result = image_clip
            # image_clips.append(image_clip)
        else:
                    # Mark as not shown (optional if needed)
            start_time_formatted = "-"

                # Add details to the table
        table.add_row(
                    str(index),
                    os.path.basename(image_file),
                    f"↔{original_size[0]} ↕{original_size[1]}",
                    f"↔{resized_size[0]} ↕{resized_size[1]}",
                    start_time_formatted,
                    str(duration_per_image)
                )
        
        return result
        