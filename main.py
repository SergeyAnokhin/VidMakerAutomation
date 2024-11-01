import os
import yaml
import AudioReaderConverter
import AudioVisualizationConverter
import ImageOverlayConverter
import SlideshowCreatorConverter
# from converters import *
from rich.console import Console
from icecream import ic

import TextOverlayConverter
import VideoExportConverter

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

        for converter_data in converters:
            converter_type = converter_data['type']
            config = converter_data.get('config', {})
            converter = create_converter(converter_type, directory, config)

            if converter:
                clips = converter.convert(clips, metadata)
            else:
                console.print(f"[red]Unknown converter type: {converter_type}[/red]")

# Create converter instance
def create_converter(converter_type, directory, config):
    converter_map = {
        "AudioReaderConverter": AudioReaderConverter,
        "SlideshowCreatorConverter": SlideshowCreatorConverter,
        "TextOverlayConverter": TextOverlayConverter,
        "ImageOverlayConverter": ImageOverlayConverter,
        "SplitConverter": SplitConverter,
        "AudioVisualizationConverter": AudioVisualizationConverter,
        "JoinConverter": JoinConverter,
        "VideoExportConverter": VideoExportConverter,
    }
    converter_class = converter_map.get(converter_type)
    if converter_class:
        return converter_class(directory, config)
    return None

if __name__ == "__main__":
    # Set base directory and configuration file path
    base_directory = '.'
    config_path = os.path.join(base_directory, 'config.yaml')

    # Load configuration
    try:
        config = load_config(config_path)
        tasks = config.get('tasks', [])
    except FileNotFoundError:
        console.print("[red]Configuration file not found. Please provide a valid config.yaml file.[/red]")
        exit(1)

    # Get directories to process
    clip_directories = get_clip_directories(base_directory)
    if not clip_directories:
        console.print("[yellow]No clip directories found.[/yellow]")
        exit(1)

    # Process each directory
    for directory in clip_directories:
        console.rule(f"Processing Directory: {directory}")
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