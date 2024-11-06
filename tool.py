import time
import cv2
import numpy as np
from moviepy.editor import VideoClip
import librosa  


def transform_to_MMSS(seconds: int) -> str:
    return time.strftime('%M:%S', time.gmtime(seconds))

# def transform_to_MMSS(seconds: int) -> str:
#     return f"{int(seconds // 60)}:{int(seconds % 60):02d}"

# Dictionary to map colormap codes to their names
colormap_names = {
    0: "COLORMAP_AUTUMN",
    1: "COLORMAP_BONE",
    2: "COLORMAP_JET",
    3: "COLORMAP_WINTER",
    4: "COLORMAP_RAINBOW",
    5: "COLORMAP_OCEAN",
    6: "COLORMAP_SUMMER",
    7: "COLORMAP_SPRING",
    8: "COLORMAP_COOL",
    9: "COLORMAP_HSV",
    10: "COLORMAP_PINK",
    11: "COLORMAP_HOT",
    12: "COLORMAP_PARULA",
}

def get_colormap_name(code):
    return colormap_names.get(code, "Unknown colormap")

def inspect_clip(name, clip, log, debug=False):
    if not debug:
        return

    # Get the size (resolution) of the clip
    log.log(f"[bold blue]===== Inspect clip: {name} ========[/bold blue]")
    size = clip.size
    log.log(f"📐 Size (width, height): {size}")

    # Get the duration of the clip
    duration = clip.duration
    log.log(f"⏱️ Duration: {duration} seconds")

    # Check if the clip has an alpha mask (transparency)
    has_transparency = clip.mask is not None
    log.log(f"🎨 Has transparency (alpha channel): {has_transparency}")

    # Get the number of color channels by inspecting a frame
    frame = clip.get_frame(0)  # Get the first frame of the clip
    num_channels = (
        frame.shape[2] if len(frame.shape) == 3 else 1
    )  # Check if the frame has color channels
    log.log(f"📊 Number of color channels: {num_channels} (ℹ: 3 for RGB, 4 for RGBA)")

    # Print if the clip has transparency based on number of channels
    if num_channels == 4:
        log.log("🎨 This clip is RGBA (has transparency).")
    else:
        log.log("🎨 This clip is RGB (no transparency).")
    log.log("[bold blue]==============================[/bold blue]")

def load_audio_from_videoclip(clip: VideoClip, log, fps=24, type="moviepy", metadata=None, sample_rate=None):
    """
    Extracts audio from a VideoFileClip, returning it in a format similar to `librosa.load`.

    Parameters:
        video_clip (VideoFileClip): The MoviePy VideoFileClip object.
        sr (int or None): Desired sample rate. If None, uses the original sample rate of the video.
        mono (bool): If True, converts the audio to mono. If False, keeps stereo (if available).

    Returns:
        y (np.ndarray): Audio data as a NumPy array. 1D if mono, 2D if stereo.
        sr (int): The sample rate of the audio data.
    """
        
    if clip.audio is None or clip.audio.duration is None:
        log.log("Audio duration is missing or the audio track is not present.")
    else:
        log.log(f"Audio duration: {transform_to_MMSS(clip.audio.duration)}")        
    
    log.log(f"[grey]🎵 Using [bold]{type}[/bold] type to load audio[/grey]")
    if type == "moviepy":
        # Use specified sample rate or default to 44100 Hz

        # Extract audio as a NumPy array with the specified sample rate
        # audio_data = clip.audio.to_soundarray(fps=sample_rate)
        log.log(f"[grey]🎵 Loaded audio with sample rate: [bold]{sample_rate}[/bold] Hz[/grey]")
        
        # Extract the audio as a list of samples
        audio_samples = list(clip.audio.iter_frames(fps=sample_rate))
        # self.log.log(f"[grey]🎵 Setting audio sample rate: {sample_rate} Hz. 📊 Got {len(audio_samples)} audio samples[/grey]")

        # Convert the list of samples to a NumPy array
        audio_data = np.array(audio_samples)
        return audio_data.T, sample_rate    
    else:
        # TODO: fix duration of audio
        log.log(f"[grey]🎵 Loading audio from file: [bold]{metadata['audio_file']}[/bold][/grey]")
        y, sr = librosa.load(metadata["audio_file"], sr=None, mono=False)
        log.log(f"[grey]🎵 Loaded audio with sample rate: [bold]{sr}[/bold] Hz[/grey]")
        log.log(f"[grey]🔢 Первые 50 значений аудио:[/grey]")
        log.log(f"[grey]{y[:50]}[/grey]")
        return y, sr

    # self.log.log(f"[grey]🔊 Converting audio samples to NumPy array with shape {audio_data.shape}[/grey]")
    # print(audio_data)
    # print(audio_data.shape)
    
    # print("----------------")
    # y, sr = librosa.load("Clip1/The Laughing Heart #6.mp3", sr=None, mono=False)
    # print(y)
    # print(sr)
    # print(y.shape)
    
    # raise ValueError("STOP!")
    
    # return y, sr