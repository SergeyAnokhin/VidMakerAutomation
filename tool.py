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
    Extracts audio from a video clip and returns it in a format compatible with librosa.load or moviepy output.

    Parameters:
        clip (VideoClip): MoviePy VideoClip object containing video with audio
        log (HierarchicalLogger): Logger for outputting process information
        fps (int): Frame rate for audio extraction (default 24)
        type (str): Audio extraction type - "moviepy" or "librosa"
        metadata (dict): Metadata containing audio file path for librosa
        sample_rate (int): Desired audio sampling rate in Hz

    Returns:
        tuple:
            - np.ndarray: Audio data as NumPy array
              For mono: 1D array of values [-1, 1]
              For stereo: 2D array [left_channel, right_channel] with values [-1, 1]
            - int: Audio sampling rate in Hz
    """
        
    if clip.audio is None or clip.audio.duration is None:
        log.log("Audio duration is missing or the audio track is not present.")
    else:
        log.log(f"Audio duration: {transform_to_MMSS(clip.audio.duration)}")        
    
    log.log(f"[grey]🎵 Using [bold]{type}[/bold] type to load audio[/grey]")
    if type == "moviepy":
        # Extract audio as a NumPy array with the specified sample rate
        log.log(f"[grey]🎵 Loaded audio with sample rate: [bold]{sample_rate}[/bold] Hz.  [bold]{clip.audio.duration}[/bold] seconds. Filename: [bold]{clip.filename}[/bold][/grey]")
        
        # Get audio samples as a list of frames, where each frame is a numpy array
        # For mono audio: each frame is a single float value between -1 and 1
        # For stereo: each frame is [left_channel, right_channel] with values between -1 and 1
        # fps parameter determines how many frames per second are sampled
        audio_samples = list(clip.audio.iter_frames(fps=sample_rate))

        # Convert the list of samples to a NumPy array
        audio_data = np.array(audio_samples)
        return audio_data.T, sample_rate    
    else:
        # TODO: fix duration of audio
        log.log(f"[grey]🎵 Loading audio from file: [bold]{metadata['audio_file']}[/bold][/grey]")
        
        # Load audio file using librosa
        # y: numpy array of shape (n_channels, n_samples)
        #    - For stereo: y[0] is left channel, y[1] is right channel
        #    - Values are normalized to [-1, 1] range
        # sr: integer sample rate in Hz (e.g. 44100, 48000)
        y, sr = librosa.load(metadata["audio_file"], sr=None, mono=False)
        log.log(f"[grey]🎵 Loaded audio with sample rate: [bold]{sr}[/bold] Hz[/grey]")
        log.log(f"[grey]🔢 Первые 50 значений аудио:[/grey]")
        log.log(f"[grey]{y[:50]}[/grey]")
        return y, sr

def get_segment_duration(total_duration, segment_number, total_segments):
    # Вычисляем длительность одного сегмента
    segment_length = total_duration // total_segments

    # Определяем начало и конец сегмента
    start_time = segment_number * segment_length
    end_time = start_time + segment_length

    # Если это последний сегмент, корректируем конечное время
    if segment_number == total_segments + 1:
        end_time = total_duration - 1

    return start_time, end_time