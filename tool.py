import time
import cv2

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

def inspect_clip(name, clip, log, debug=True):
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
