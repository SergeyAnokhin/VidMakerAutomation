import numpy as np
import cv2
from moviepy.editor import AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from .base_converter import BaseConverter

class ChannelBarsVisualizer(BaseConverter):  # Assuming BasicConvert is your provided base class

    def __init__(self, config):
        self.config = config
        self.num_bars_per_channel = 4  # four bars for each channel
        self.font = ImageFont.load_default()  # Font for bar height labels

    def convert(self, clip):
        # Extract audio data from the video clip
        audio = clip.audio
        audio_data = self.extract_audio_data(audio)
        
        # Configuration parameters
        fps = self.config.get('visualization', {}).get('fps', 60)
        colormap_name = self.config.get('visualization', {}).get('colormap', 'COLORMAP_JET')
        bar_height_scale = self.config.get('visualization', {}).get('bar_height_scale', 0.8)
        
        # Visualization image size
        image_width = self.config.get('visualization', {}).get('image_width', 800)
        image_height = self.config.get('visualization', {}).get('image_height', 600)
        bar_width = self.config.get('visualization', {}).get('bar_width', 20)
        spacing = self.config.get('visualization', {}).get('spacing', 10)

        # Color map from OpenCV
        colormap = getattr(cv2, colormap_name)
        
        # Define frequency bands for each bar (frequency ranges)
        frequency_bands = self.config.get('frequency_bands', [60, 250, 500, 2000])

        # Create an image to draw the visualization on
        image = Image.new("RGB", (image_width, image_height), "black")
        draw = ImageDraw.Draw(image)
        
        # Split audio data into left and right channels
        left_channel, right_channel = np.split(audio_data, 2)
        
        # Calculate amplitude for each bar based on frequency bands
        left_bars = self.calculate_frequency_bounce(left_channel, frequency_bands, bar_height_scale)
        right_bars = self.calculate_frequency_bounce(right_channel, frequency_bands, bar_height_scale)
        
        # Draw bars for both channels
        self.draw_bars(draw, left_bars, side="left", colormap=colormap)
        self.draw_bars(draw, right_bars, side="right", colormap=colormap)
        
        return image

    def extract_audio_data(self, audio):
        """ Extract audio data from MoviePy AudioFileClip """
        audio_data = np.array(list(audio.iter_frames(fps=audio.fps)))[:, 0]  # Only keep one channel
        return audio_data
    
    def calculate_frequency_bounce(self, channel_data, frequency_bands, scale):
        """ Calculate amplitude for each frequency band (Frequency Bounce) """
        amplitudes = []
        
        for band in frequency_bands:
            # Filter data by frequency
            band_data = channel_data[::band]  # Approximate filter, can be refined for accuracy
            amplitude = np.mean(np.abs(band_data)) * scale
            amplitudes.append(amplitude)
        
        return amplitudes

    def draw_bars(self, draw, amplitudes, side="left", colormap=cv2.COLORMAP_JET):
        """ Draw bars on the image using OpenCV ColorMap """
        for idx, amplitude in enumerate(amplitudes):
            # Determine color for each bar based on amplitude
            color_value = int((amplitude / max(amplitudes)) * 255)
            color = cv2.applyColorMap(np.array([[color_value]], dtype=np.uint8), colormap)[0][0]
            color_tuple = (int(color[0]), int(color[1]), int(color[2]))

            # Define the x-position for each bar
            if side == "left":
                x_pos = idx * (self.config['visualization']['bar_width'] + self.config['visualization']['spacing'])
            else:
                x_pos = self.config['visualization']['image_width'] - (idx + 1) * (self.config['visualization']['bar_width'] + self.config['visualization']['spacing'])

            y_top = self.config['visualization']['image_height'] - amplitude
            y_bottom = self.config['visualization']['image_height']

            # Draw the rectangle for each bar
            draw.rectangle([x_pos, y_top, x_pos + self.config['visualization']['bar_width'], y_bottom], fill=color_tuple)

            # Add height label below each bar
            text_position = (x_pos, y_bottom + 5)
            draw.text(text_position, f"{int(amplitude)}", fill="white", font=self.font)
