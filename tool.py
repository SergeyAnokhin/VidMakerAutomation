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
