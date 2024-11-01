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
          end_time: null
      - type: "SlideshowCreatorConverter"
        config:
          slideshow:
            height: 720
          transition:
            fade_in: 1.0
            fade_out: 1.0
      - type: "TextOverlayCo