import os
import yaml
from converters.audio_reader_converter import AudioReaderConverter
from rich.console import Console
from icecream import ic
import traceback

from converters.channel_bars_visualizer import ChannelBarsVisualizer
from converters.image_overlay_converter import ImageOverlayConverter
from converters.join_converter import JoinConverter
from converters.slideshow_creator_converter import SlideshowCreatorConverter
from converters.split_converter import SplitConverter
from converters.text_overlay_converter import TextOverlayConverter
from converters.two_basses_visualization_convertor import TwoSpotsVisualizationConverter
from converters.video_export_converter import VideoExportConverter
from hierarchical_logger import HierarchicalLogger

console = Console()

# Load configuration file
def load_config(config_path):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

# Find all directories starting with 'Clip'
def get_clip_directories(base_directory):
    return [
        os.path.join(base_directory, d) for d in os.listdir(base_directory)
        if os.path.isdir(os.path.join(base_directory, d)) and d.lower().startswith('clip')
    ]

# Main processing function
def process_directory(directory, tasks):
    for task in tasks:
        console.rule(f"Processing Task: {task['name']}")
        converters = task.get('converters', [])
        clips = []
        metadata = {}
        logger = HierarchicalLogger(directory=directory)


        for converter_data in converters:
            converter_type = converter_data['type']
            config = converter_data.get('config', {})
            converter = create_converter(converter_type, directory, config, logger)

            if converter:
                clips = converter.process(clips, metadata)
            else:
                console.print(f"[red]Unknown converter type: {converter_type}[/red]")

# Create converter instance
def create_converter(converter_type, directory, config, logger: HierarchicalLogger):
    converter_map = {
        "AudioReaderConverter": AudioReaderConverter,
        "SlideshowCreatorConverter": SlideshowCreatorConverter,
        "TextOverlayConverter": TextOverlayConverter,
        "ImageOverlayConverter": ImageOverlayConverter,
        "SplitConverter": SplitConverter,
        "TwoSpotsVisualizationConverter": TwoSpotsVisualizationConverter,
        "ChannelBarsVisualizer": ChannelBarsVisualizer,
        "JoinConverter": JoinConverter,
        "VideoExportConverter": VideoExportConverter,
    }
    converter_class = converter_map.get(converter_type)
    if converter_class:
        return converter_class(directory, config, logger)
    return None

if __name__ == "__main__":
    # Set base directory
    base_directory = '.'
    
    # Get directories to process
    clip_directories = get_clip_directories(base_directory)
    if not clip_directories:
        console.print(f"[yellow]No clip directories found in {base_directory}.[/yellow]")
        exit(1)

    # Process each directory
    for directory in clip_directories:
        console.rule(f"Processing Directory: {directory}", characters="=")
        try:
            config_path = os.path.join(directory, 'config.yaml')
            if os.path.exists(config_path):
                config = load_config(config_path)
                tasks = config.get('tasks', [])
                process_directory(directory, tasks)
            else:
                console.print(f"[red]No config.yaml found in directory {directory}. Skipping...[/red]")
        except Exception as e:
            console.print(f"[red]Error processing directory {directory}: {str(e)}[/red]")
            console.print(f"[red]{traceback.format_exc()}[/red]")