import tool
from .base_converter import BaseConverter
from moviepy.editor import *
from rich.console import Console
from rich.table import Table
import numpy as np
import cv2
import librosa

console = Console()

class TwoSpotsVisualizationConverter(BaseConverter):
    def convert(self, clip: VideoClip, metadata, index: int):
        """
        Adds an audio visualization overlay to each video clip in the list.
        If no clips are provided, raises an error.
        """
        if not clip:
            self.log.error(f"No existing clips found. Cannot add audio visualization without clips.")
            raise ValueError("No existing clips found to add audio visualization.")

        self.log.log(f"[bold blue]Processing Audio Visualization:[/bold blue] Adding two spots visualization")

        # audio_path = self.config.get('audio', {}).get('path')
        # if not audio_path or not os.path.exists(audio_path):
        #     self.log.log(f"[red]Audio file not found or path not specified: {audio_path}[/red]")
        #     raise FileNotFoundError("Audio file not found or path not specified.")

        # bar_count = self.config.get('visualization', {}).get('bar_count', 30)  # Default bar count to 30
        # height = self.config.get('visualization', {}).get('height', 150)  # Default visualization height to 150
        fps = self.config.get('visualization', {}).get('fps', 60) 
        colormap_name = self.config.get('visualization', {}).get('colormap', 'COLORMAP_JET')  # Default palette to 'COLORMAP_MAGMA'
        colormap = getattr(cv2, colormap_name, cv2.COLORMAP_JET)

        # # Create an audio clip
        # audio_clip = AudioFileClip(audio_path)

        # # Placeholder for visualization (needs actual implementation for creating visual bars)
        # visualization_clip = colorx(audio_clip.to_ImageClip(), 0.5).set_duration(audio_clip.duration)

        # updated_clips = []
        # for clip in clips:
        #     self.log.log(f"[green]Adding audio visualization to clip with duration {clip.duration} seconds.[/green]")
        #     updated_clips.append(CompositeVideoClip([clip, visualization_clip.set_duration(clip.duration)]))
        # return updated_clips
        
        tool.inspect_clip("clip", clip, self.log)

        # all color maps : https://learnopencv.com/applycolormap-for-pseudocoloring-in-opencv-c-python/
        equalizer_clip = self.create_equalizer_clip(clip, size=clip.size, index=index,
                            colormap=colormap, debug_mode=False, fps=fps, metadata=metadata)        
        tool.inspect_clip("equalizer_clip", equalizer_clip, self.log)

        # Делаем фон прозрачным (удаляем определенный цвет)
        equalizer_clip = equalizer_clip.fx(vfx.mask_color, color=[0, 0, 0], thr=100, s=5) # thr=100, s=5
        tool.inspect_clip("equalizer_clip", equalizer_clip, self.log)
        # equalizer_clip = equalizer_clip.mask_color(color=[0, 0, 0], thr=100, s=5) # thr=100, s=5
        equalizer_clip = equalizer_clip.set_opacity(0.2)  # Опционально: установить прозрачность
        tool.inspect_clip("equalizer_clip", equalizer_clip, self.log)

        composite_clip = CompositeVideoClip([clip, equalizer_clip])
        tool.inspect_clip("composite_clip", composite_clip, self.log)

        return composite_clip
    
    # @retry(stop_max_attempt_number=5, wait_fixed=5000)
    def load_audio(self, clip, audio_part, sample_rate):
        # try:
            return tool.load_audio_from_videoclip(clip, self.log, audio_part=audio_part, sample_rate=sample_rate)
        # except Exception as e:
        #     self.log.warn(f"[yellow]Error loading audio from {clip.filename} : {e}. Trying again...[/yellow]")
        #     raise e
        
    # all color maps : https://learnopencv.com/wp-content/uploads/2015/07/colormap_opencv_example.jpg
    def create_equalizer_clip(self, clip: VideoClip, fps, size, index, colormap=cv2.COLORMAP_JET,
                            debug_mode=False, metadata=None):
        
        # circle_radius=300,
        # center_dot_size=15, edge_dot_size=5,
        # num_dots=10,
        # circle_vertical_position_percent=10,
        # amplitude_threshold=0.05,
        # frequency_bands=None,

        resize_factor = size[1] / 1024
        duration = clip.duration   
        size = clip.size
        # Radius of the visualization circle, set to 25% of video height
        # Example for 1080p video:
        #  ___________1920px____________
        # |                             |
        # |          ○ <-270px radius   | 1080px 
        # |         /|\                 |
        # |                             |
        # |_____________________________|
        circle_radius = size[1] * 0.3 * resize_factor

        # Positions for color transitions in the colormap (0.0=start color, 1.0=end color)
        # Example:
        # [0.0]    [0.33]    [0.66]    [1.0]
        #  blue -> yellow -> orange ->  red
        colormap_positions=[0.0, 0.33, 0.66, 1.0]

        # Size in pixels of the center dot that shows the main beat
        # Example:
        #    ___35px___
        #   /     ○    \  <- Center dot expands/contracts with beat
        #  |   ●●●●●●   | 
        #   \__________/
        center_dot_size=20 * resize_factor

        # Size in pixels of the smaller dots around the circle edge
        # Example:
        #      ○        
        #   •       •    <- 5px dots
        #      ○
        edge_dot_size=5 * resize_factor

        # Number of dots to display around the circle
        # Example:
        #      • • •      
        #    •       •    <- 30 dots total
        #  •           •
        #    •       •
        #      • • •
        num_dots=round(30 * resize_factor)

        # Vertical position of circle center as percentage from top of frame
        # Example for 7%:
        # ___________________
        #      ○  <- 7% from top
        # |           |
        # |           |
        # |___________|
        circle_vertical_position_percent=7
        # Threshold for audio amplitude to trigger visualization (0.0-1.0)
        amplitude_threshold=0.6

        # Log visualization parameters
        table = Table(title="🎨 Visualization Parameters")
        table.add_column("📊 Parameter", justify="right")
        table.add_column("Value", justify="left") 
        table.add_column("📊 Parameter", justify="right")
        table.add_column("Value", justify="left")
        params = [
            ("⏱️ Duration", f"{duration:.2f} s", "🎯 Circle Radius", f"{circle_radius:.0f} px"),
            ("📐 Size", f"↔{size[0]} ↕{size[1]} px", "🎨 Colormap", tool.get_colormap_name(colormap)),
            ("⚪ Center Dot", str(center_dot_size), "⭕ Edge Dot", str(edge_dot_size)),
            ("🔢 Num Dots", str(num_dots), "📍 Circle Y Pos", f"{circle_vertical_position_percent}%"),
            ("📊 Amplitude", str(amplitude_threshold), "🎞️ FPS", str(fps)),
            ("🎨 Colors", str(colormap_positions), "", "")
        ]
        for row_params in params:
            table.add_row(*row_params)
        self.log.print(table)

        # Создаем эквалайзерный клип
        # Настройка диапазонов частот для каждой из четырех суб-точек с усилением
        frequency_bands = [
            {'band': (20, 80), 'amplification': 0.2}, # blue
            {'band': (80, 255), 'amplification': 1.0}, # light blue # humain voice band 
            {'band': (255, 500), 'amplification': 1.0}, # yellow
            {'band': (500, 8000), 'amplification': 4.00}, # red
        ]
        # Load audio file
        # y, sr = librosa.load(audio_file, sr=None, mono=False)
        sample_rate = self.config.get('audio', {}).get('sample_rate', 48000)

        # try:
        audio_part = metadata["audio_parts"][index]
        y, sr = self.load_audio(clip, audio_part, sample_rate)
        # except Exception as e:
        #     self.log.warn(f"[yellow]Error loading audio from {clip.filename} : {e}. Trying to load from file...[/yellow]")
        #     time.sleep(10)
        #     try:    
        #         y, sr = tool.load_audio_from_videoclip(clip, self.log, fps, metadata=metadata, sample_rate=sample_rate)
        #     except Exception as e:
        #         self.log.error(f"[red]Error loading audio from {clip.filename} : {e}[/red]")
        #         return clip

        self.log.log(f"[grey]🎨Used colormap: {tool.get_colormap_name(colormap)}[/grey]")        

        # Ensure audio is stereo
        if y.ndim == 1:
            y = np.array([y, y])

        # Parameters for audio processing
        hop_length = int(sr / fps)
        n_fft = 2048

        # Get spectrograms for left and right channels
        S_left = np.abs(librosa.stft(y[0], n_fft=n_fft, hop_length=hop_length))
        S_right = np.abs(librosa.stft(y[1], n_fft=n_fft, hop_length=hop_length))

        # Frequency scale
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        # Function to aggregate spectrogram over frequency bands
        def aggregate_band_amplitude(S, band):
            freq_mask = (frequencies >= band[0]) & (frequencies < band[1])
            if np.any(freq_mask):
                return np.mean(S[freq_mask, :], axis=0)
            else:
                return np.zeros(S.shape[1])

        # Extract amplitudes for each frequency band with amplification
        band_amplitudes_left = []
        band_amplitudes_right = []
        table = Table()
        table.add_column("↔Range", justify="center")
        table.add_column("⏫Amplification", justify="center")
        table.add_column("Max Left", justify="center")
        table.add_column("Median Left", justify="center")
        table.add_column("Max Right", justify="center")
        table.add_column("Median Right", justify="center")
        table.add_column("Normalized Weight", justify="center")

        total_max_left = 0
        total_max_right = 0

        band_data = []

        for band_info in frequency_bands:
            band = band_info['band']
            amplification = band_info.get('amplification', 1.0)
            amp_left = aggregate_band_amplitude(S_left, band) * amplification
            amp_right = aggregate_band_amplitude(S_right, band) * amplification
            band_amplitudes_left.append(amp_left)
            band_amplitudes_right.append(amp_right)
            
            # Calculate max and median values
            max_left = np.max(amp_left)
            median_left = np.median(amp_left)
            max_right = np.max(amp_right)
            median_right = np.median(amp_right)
            
            # Summarize max values
            total_max_left += max_left
            total_max_right += max_right

            # Store data in array
            band_data.append({
                "band": f"{band[0]}-{band[1]} Hz",
                "amplification": str(amplification),
                "max_left": f"{max_left:.2f}",
                "median_left": f"{median_left:.2f}",
                "max_right": f"{max_right:.2f}",
                "median_right": f"{median_right:.2f}",
                "normalized_weight": ""  # Placeholder for normalized weight
            })
        
        # Normalize and update the table with weights
        for i, band_info in enumerate(frequency_bands):
            max_left = np.max(band_amplitudes_left[i])
            max_right = np.max(band_amplitudes_right[i])
            normalized_weight = ((max_left / total_max_left) + (max_right / total_max_right)) / 2
            band_data[i]["normalized_weight"] = f"{normalized_weight:.2f}"

            # Add row to the table
            table.add_row(
                band_data[i]["band"],
                band_data[i]["amplification"],
                band_data[i]["max_left"],
                band_data[i]["median_left"],
                band_data[i]["max_right"],
                band_data[i]["median_right"],
                band_data[i]["normalized_weight"]
            )

        self.log.print(table)

        # Normalize amplitudes
        max_amp = max([band.max() for band in band_amplitudes_left + band_amplitudes_right])
        if max_amp == 0:
            max_amp = 1e-6  # Avoid division by zero
        band_amplitudes_left = [band / max_amp for band in band_amplitudes_left]
        band_amplitudes_right = [band / max_amp for band in band_amplitudes_right]

        # Clip amplitudes to [0, 1]
        band_amplitudes_left = [np.clip(band, 0, 1) for band in band_amplitudes_left]
        band_amplitudes_right = [np.clip(band, 0, 1) for band in band_amplitudes_right]

        # Ensure number of frames matches duration and fps
        num_frames = int(duration * fps)
        interpolated_bands_left = [np.interp(np.linspace(0, len(band) - 1, num_frames),
                                            np.arange(len(band)), band)
                                for band in band_amplitudes_left]
        interpolated_bands_right = [np.interp(np.linspace(0, len(band) - 1, num_frames),
                                            np.arange(len(band)), band)
                                    for band in band_amplitudes_right]

        # Compute dot positions within circle
        def compute_dot_positions(center):
            positions = []
            for i in range(num_dots):
                for j in range(num_dots):
                    # Normalized positions between -1 and 1
                    x_norm = -1 + 2 * i / (num_dots - 1)
                    y_norm = -1 + 2 * j / (num_dots - 1)
                    # Check if point is inside circle
                    if x_norm**2 + y_norm**2 <= 1:
                        x = center[0] + x_norm * circle_radius
                        y = center[1] + y_norm * circle_radius
                        positions.append((int(x), int(y), x_norm, y_norm))
            return positions

        # Circle positions
        vertical_pos = size[1] * (circle_vertical_position_percent / 100)

        left_center = (int(size[0] * 0.1), int(vertical_pos))   # Left speaker
        right_center = (int(size[0] * 0.9), int(vertical_pos))  # Right speaker

        left_positions = compute_dot_positions(left_center)
        right_positions = compute_dot_positions(right_center)

        # Generate colors from colormap at specified positions
        colormap_colors = [cv2.applyColorMap(
            np.array([[int(pos * 255)]], dtype=np.uint8), colormap)[0][0]
            for pos in colormap_positions]
        # Convert BGR to RGB
        colormap_colors = [(int(c[2]), int(c[1]), int(c[0])) for c in colormap_colors]

        # For debugging, we will store dot sizes
        debug_info = []

        def make_frame(t):
            # Get the current frame index
            frame_idx = int(t * fps)
            if frame_idx >= num_frames:
                frame_idx = num_frames - 1

            # Create an empty frame
            frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)

            # Clear debug_info for this frame
            if debug_mode:
                debug_info.clear()

            # Function to draw dots
            def draw_dots(positions, band_amplitudes, channel_name):
                # For debugging information
                frame_debug_info = []

                for x, y, x_norm, y_norm in positions:
                    # Calculate base dot size based on position
                    distance = np.sqrt(x_norm**2 + y_norm**2)
                    dot_size = edge_dot_size + (center_dot_size - edge_dot_size) * (1 - distance)

                    # List to store current_dot_size for each band
                    current_dot_sizes = []

                    # Draw four mini-dots with different colors
                    for idx, color in enumerate(colormap_colors):
                        amp = band_amplitudes[idx][frame_idx]  # Amplitude from corresponding frequency band
                        # Increase the range of size variation
                        current_dot_size = dot_size * (0.0 + 2.0 * amp)  # Adjust size based on amplitude
                        current_dot_size = max(1, int(current_dot_size))

                        current_dot_sizes.append(current_dot_size // 2)

                        offset = (idx - 1.5) * current_dot_size / 3  # Position mini-dots around the main point
                        xi = int(x + offset)
                        yi = int(y + offset)
                        if 0 <= xi < size[0] and 0 <= yi < size[1]:
                            cv2.circle(frame, (xi, yi), current_dot_size // 2, color, -1)

                    # Save debugging information only for the Left channel
                    if channel_name == 'Left' and debug_mode:
                        frame_debug_info.append({
                            'position': (x, y),
                            'distance': distance,
                            'dot_size': dot_size,
                            'amplitudes': [band[frame_idx] for band in band_amplitudes],
                            'current_dot_sizes': current_dot_sizes  # List of current_dot_size for each band
                        })

                if channel_name == 'Left' and debug_mode:
                    debug_info.extend(frame_debug_info)

            # Draw dots for Left channel
            draw_dots(left_positions, interpolated_bands_left, 'Left')
            # Draw dots for Right channel (can skip if only interested in Left)
            draw_dots(right_positions, interpolated_bands_right, 'Right')

            # If debug mode is on, display information
            if debug_mode:
                # Sum current_dot_sizes over all points
                num_points = len(debug_info)
                total_current_dot_sizes = [0] * len(frequency_bands)

                for point_info in debug_info:
                    for idx, current_dot_size in enumerate(point_info['current_dot_sizes']):
                        total_current_dot_sizes[idx] += current_dot_size

                # Compute average current_dot_size for each band
                if num_points > 0:
                    avg_current_dot_sizes = [total_current_dot_sizes[idx] / num_points for idx in range(len(frequency_bands))]
                else:
                    avg_current_dot_sizes = [0] * len(frequency_bands)

                # Display text information on the frame
                debug_texts = []
                message = ""
                for idx, band_info in enumerate(frequency_bands):
                    freq_range = f"{band_info['band'][0]:6.0f}-{band_info['band'][1]:6.0f} Hz"
                    amplitude = interpolated_bands_left[idx][frame_idx]
                    amplitude_percent = f"{amplitude * 100:6.0f}%"
                    dot_size = avg_current_dot_sizes[idx]
                    debug_texts.append(f"Band {idx+1} ({freq_range}): {amplitude_percent} Size: {dot_size:5.2f}")
                    message += f"{amplitude_percent} Size: {dot_size:5.2f} |"
                print(f"Band Amplitudes: {message}")

                # Position for displaying the text
                text_x = size[0] // 2 - 200
                text_y = int(vertical_pos)

                # Font options
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                color = (255, 255, 255)
                thickness = 2

                # Draw rectangle behind text for contrast
                rect_width = 400
                rect_height = 30 * len(debug_texts)
                overlay = frame.copy()
                cv2.rectangle(overlay, (text_x - 10, text_y - 30),
                            (text_x + rect_width, text_y + rect_height),
                            (0, 0, 0), -1)
                alpha = 0.5  # Transparency
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

                # Display text information
                for i, text in enumerate(debug_texts):
                    y_position = text_y + i * 30
                    cv2.putText(frame, text, (text_x, y_position), font,
                                font_scale, color, thickness, cv2.LINE_AA)

            # Check amplitude threshold
            if all(band[frame_idx] < amplitude_threshold for band in interpolated_bands_left):
                # Return an empty transparent frame
                return frame

            return frame

        # Create video clip for the frame
        equalizer_clip = VideoClip(make_frame, duration=duration).set_fps(fps)

        # get_max_dot_sizes_per_band(debug_info, len(frequency_bands))

        return equalizer_clip


    def get_max_dot_sizes_per_band(debug_info, num_bands=4):
        # Инициализируем список для хранения максимальных размеров по каждому диапазону
        max_dot_sizes_per_band = [0] * num_bands

        # Проходим по кадрам
        for frame_debug in debug_info:
            # Проходим по точкам в кадре
            current_dot_sizes = frame_debug['current_dot_sizes']
            # Проходим по диапазонам частот
            for idx in range(num_bands):
                size = current_dot_sizes[idx]
                if size > max_dot_sizes_per_band[idx]:
                    max_dot_sizes_per_band[idx] = size

        # Выводим максимальные размеры точек по каждому диапазону
        for idx, max_size in enumerate(max_dot_sizes_per_band):
            print(f"Максимальный размер точки для диапазона {idx+1}: {max_size}")

        return max_dot_sizes_per_band


    def create_equalizer_clip_bars_upper(audio_file, duration, fps=24, size=(1280, 720),
                            colormap=cv2.COLORMAP_JET, equalizer_width_percent=10,
                            max_bar_height_percent=90, num_bars=60):
        # Загружаем аудио файл
        y, sr = librosa.load(audio_file, sr=None, mono=False)

        # Убедимя, что аудио стерео
        if y.ndim == 1:
            y = np.array([y, y])

        # Параметры для обработки аудио
        hop_length = int(sr / fps)
        n_fft = 4096  # Увеличиваем FFT для лучшего разрешения по частоте

        # Получаем спектрограммы для лево��о и правого каналов
        S_left = np.abs(librosa.stft(y[0], n_fft=n_fft, hop_length=hop_length))
        S_right = np.abs(librosa.stft(y[1], n_fft=n_fft, hop_length=hop_length))

        # Частотная шкала
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        # Определяем границы частот для каждого столбика (логарифмическая шкала)
        freq_bins = np.logspace(np.log10(frequencies[1]), np.log10(frequencies[-1]), num=num_bars+1)

        # Функция для агрегирования спектрограммы по частотным диапазонам
        def aggregate_spectrum(S, freq_bins):
            spectrum_bars = np.zeros((len(S[0]), num_bars))
            for i in range(num_bars):
                freq_mask = (frequencies >= freq_bins[i]) & (frequencies < freq_bins[i+1])
                if np.any(freq_mask):
                    spectrum_bars[:, i] = S[freq_mask, :].mean(axis=0)
            return spectrum_bars

        # Агрегируем спектры по частотным диапазонам
        left_bars = aggregate_spectrum(S_left, freq_bins)
        right_bars = aggregate_spectrum(S_right, freq_bins)

        # Нормализуем амплитуды
        max_amp = max(left_bars.max(), right_bars.max())
        left_bars /= max_amp
        right_bars /= max_amp

        # Убеждаемся, что количество кадров соответствует длительности и fps
        num_frames = int(duration * fps)
        times = np.linspace(0, left_bars.shape[0]-1, num_frames).astype(int)
        left_bars = left_bars[times, :]
        right_bars = right_bars[times, :]

        # Вычисляем параметры один раз перед циклом
        equalizer_width = int(size[0] * (equalizer_width_percent / 100))  # Ширина каждого эквалайзера
        bar_width = equalizer_width // num_bars  # Ширина одного столбика

        # Мксимальная высота столбика в пикселях
        max_bar_height = int(size[1] * (max_bar_height_percent / 100))

        # Начальные позиции для левого и правого эквалайзеров
        left_start_x = 0  # Левый эквалайзер прижат к левому краю
        right_start_x = size[0] - equalizer_width  # Правый эквалайзер прижат к правому краю

        def make_frame(t):
            # Создаем пустой кадр RGB
            frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
            # Создаем маску (одноканальный кадр)
            mask = np.zeros((size[1], size[0]), dtype=np.uint8)

            frame_idx = int(t * fps)
            if frame_idx >= num_frames:
                frame_idx = num_frames - 1

            # Рисуем столбики для левого канала (низкие частоты по краям)
            for i in range(num_bars):
                amplitude = left_bars[frame_idx, num_bars - i - 1]  # Инвертируем индекс для частот
                bar_height = int(amplitude * max_bar_height)
                x = left_start_x + i * bar_width
                y = 0  # Начало от верхнего края
                color_intensity = int(amplitude * 255)
                color_bgr = cv2.applyColorMap(
                    np.array([[color_intensity]], dtype=np.uint8), colormap)[0][0]
                color_rgb = (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0]))  # Конвертация BGR в RGB
                # Рисуем столбик на кадре
                cv2.rectangle(frame, (x, y), (x + bar_width - 2, y + bar_height), color_rgb, -1)
                # Рисуем столбик на маске (белый цвет - непрозрачный)
                cv2.rectangle(mask, (x, y), (x + bar_width - 2, y + bar_height), 255, -1)

            # Рисуем столбики для правого канала (столбики идут от правого края к центру)
            for i in range(num_bars):
                amplitude = right_bars[frame_idx, i]
                bar_height = int(amplitude * max_bar_height)
                x = right_start_x + (num_bars - i - 1) * bar_width
                y = 0
                color_intensity = int(amplitude * 255)
                color_bgr = cv2.applyColorMap(
                    np.array([[color_intensity]], dtype=np.uint8), colormap)[0][0]
                color_rgb = (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0]))  # Конвертация BGR в RGB
                # Рисуем столбик на кадре
                cv2.rectangle(frame, (x, y), (x + bar_width - 2, y + bar_height), color_rgb, -1)
                # Рисуем столбик на маске
                cv2.rectangle(mask, (x, y), (x + bar_width - 2, y + bar_height), 255, -1)

            return frame, mask / 255.0  # Возвращаем кадр и маску (маска должна быть от 0 до 1)

        # Создаем VideoClip для кадра и маски
        def make_frame_rgb(t):
            frame, _ = make_frame(t)
            return frame

        def make_frame_mask(t):
            _, mask = make_frame(t)
            return mask

        # Создаем видео клип для кадра
        equalizer_clip = VideoClip(make_frame_rgb, duration=duration).set_fps(fps)
        # Создаем маску
        mask_clip = VideoClip(make_frame_mask, ismask=True, duration=duration).set_fps(fps)
        # Устанавливаем маску для клипа
        equalizer_clip = equalizer_clip.set_mask(mask_clip)

        return equalizer_clip

