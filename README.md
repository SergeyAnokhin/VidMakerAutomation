# 🎥 Video Creation Pipeline 🚀

## ℹ️ About

This project is a Python 🐍-based video 🎞️ creation pipeline that processes media files 📂 from directories 📁 and automatically generates videos 📽️ by applying different tasks 📋 and effects ✨ in sequence. The application allows for the automation 🤖 of video production by combining audio 🎶 files, images 🖼️, and other visual elements 🌈 into complete videos 📹, with support for slideshows 🎠, text overlays ✍️, audio visualizations 📊, and much more.

The project aims to be highly configurable 🔧, with a YAML 📜-based configuration file that defines the sequence of tasks 📋 and settings ⚙️ for each video 🎥, making it versatile for various video production needs.

### Suggested Names for GitHub Repository
1. **VideoFlowPy**
2. **PyVideoPipeline**
3. **MediaMagic** ✨
4. **ClipForge** 🔨
5. **VidCraft** 🛠️
6. **AutoVidPy** 🤖
7. **VidTransformer** 🔄
8. **ClipSynth** 🎶
9. **PythonVideoFactory** 🏭🐍
10. **VidMakerAutomation** ⚙️

## 🌟 Features
- **Configurable Pipeline** 🔧: Set up your video production workflow via a YAML 📜 configuration file.
- **Automated Task Execution** 🤖: Perform various tasks in sequence, such as creating slideshows 🎠, adding text overlays ✍️, merging clips 🔗, and more.
- **Modular Converters** 🔄: Each task (like adding text ✍️, images 🖼️, or exporting a video 📤) is implemented as a converter, making it easy to extend or modify.
- **Multi-Format Support** 📽️🎵🖼️: Supports various formats for images 🖼️, audio 🎶, and video 🎥.
- **Rich Logging** 📝: Uses `Rich` 🌈 and `Icecream` 🍦 for informative console output 🖥️ and logging, making it easier to debug 🐞.

## 📦 Installation

Clone the repository 📂 and install the dependencies 📜:

```bash
git clone https://github.com/yourusername/VideoFlowPy.git
cd VideoFlowPy
pip install -r requirements.txt
```

## 🚀 Usage

Create a configuration file 📄 for your video pipeline in YAML format or modify the provided `config.yaml` example.

Run the main script to process the directories 📂 and generate videos 🎥:

```bash
python main.py
```

### ⚙️ Configuration
The main configuration is in the `config.yaml` file 📜. You can specify the directories 📁, tasks 📋, and the sequence of converters 🔄 to apply to each video project 🎥. Here is a basic overview of the configuration:

- **tasks** 📋: A list of tasks, each containing a set of converters applied in sequence.
- **converters** 🔄: Defines the converters (e.g., `AudioReaderConverter` 🎶, `SlideshowCreatorConverter` 🎠, etc.) and their settings ⚙️ for each task.

Refer to the example `config.yaml` for more detailed usage.

## 🔄 Converters Overview

- **AudioReaderConverter** 🎶: Reads audio from the directory 📂.
- **SlideshowCreatorConverter** 🎠: Creates a slideshow from a set of images 🖼️.
- **TextOverlayConverter** ✍️: Adds text with configurable position 📍, color 🎨, and font settings 🖋️.
- **ImageOverlayConverter** 🖼️: Adds static or animated images on top of the video 📽️.
- **SplitConverter** ✂️: Splits video into parts for parallel processing ⚡.
- **AudioVisualizationConverter** 📊: Adds audio visualizations to the video 🎶.
- **JoinConverter** 🔗: Joins multiple video parts together.
- **VideoExportConverter** 📤: Exports the final video 🎥 with configurable quality 🌟 and output settings ⚙️.

## 📜 Dependencies
- **MoviePy** 🎥: For video processing.
- **PyYAML** 📄: To handle the YAML configuration.
- **Rich** 🌈 and **Icecream** 🍦: For enhanced console logging 📝 and debugging 🐛.

Install these by running:

```bash
pip install -r requirements.txt
```

## 📄 Example Configuration
Here is an example configuration that you can use as a starting point. This file (`config.yaml`) contains the tasks 📋 and settings ⚙️ for creating a full-length video 🎥 and a short clip 📹.

```yaml
tasks:
  - name: "Create Full Length Video"
    converters:
      - type: "AudioReaderConverter"
        config:
          start_time: 0
          end_time: null  # End of the audio
      - type: "SlideshowCreatorConverter"
        config:
          slideshow:
            height: 720  # Height of the images to be unified
          transition:
            fade_in: 1.0  # Fade-in duration in seconds
            fade_out: 1.0  # Fade-out duration in seconds
      - type: "TextOverlayConverter"
        config:
          text: "Welcome to Our Video"
          position:
            x: "50%"  # Position in percentage for horizontal centering
            y: "90%"  # Position in percentage for vertical placement at the bottom
          font:
            name: "Arial"
            size: 24
            color: "white"
          contour:
            color: "black"
            size: 2
          transition:
            fade_in: 0.5
            fade_out: 0.5
      - type: "ImageOverlayConverter"
        config:
          image:
            path: "overlay.png"
            position:
              x: "10pt"  # Position in pixels (e.g., '10pt') or percentage (e.g., '10%')
              y: "20pt"  # Position in pixels (e.g., '20pt') or percentage (e.g., '20%')
          timing:
            start_time: 5  # Seconds from the start
            end_time: 10   # Seconds from the start
      - type: "SplitConverter"
        config:
          parts: 3
      - type: "AudioVisualizationConverter"
        config:
          visualization:
            bar_count: 30
            height: 150
            palette: "COLORMAP_MAGMA"  # OpenCV colormap naming convention
      - type: "JoinConverter"
      - type: "AudioReaderConverter"
        config:
          start_time: 0
          end_time: null  # End of the audio, searches for mp3 in directory
      - type: "VideoExportConverter"
        config:
          export:
            output_path: "output.mp4"
            fps: 24
            codec: "libx264"
            quality_preset: "medium"

  - name: "Create YouTube Short"
    converters:
      - type: "AudioReaderConverter"
        config:
          start_time: 30
          end_time: 60  # Duration of 30 seconds
      - type: "SlideshowCreatorConverter"
        config:
          slideshow:
            height: 1080  # Height for YouTube Short format
          transition:
            fade_in: 0.5
            fade_out: 0.5
      - type: "TextOverlayConverter"
        config:
          text: "Enjoy this Short Clip!"
          position:
            x: "50%"  # Position in percentage for horizontal centering
            y: "50%"  # Position in percentage for vertical centering
          font:
            name: "Arial"
            size: 32
            color: "yellow"
          contour:
            color: "black"
            size: 2
          transition:
            fade_in: 0.5
            fade_out: 0.5
      - type: "VideoExportConverter"
        config:
          export:
            output_path: "short_output.mp4"
            fps: 30
            codec: "libx264"
            quality_preset: "high"
```