import tool
from .base_converter import BaseConverter
from moviepy.editor import AudioFileClip, ColorClip
from rich.console import Console
import os
import librosa
import numpy as np
from rich.table import Table
console = Console()

class AudioReaderConverter(BaseConverter):
    def convert(self, clip, metadata):
        """
        Reads an audio file from the directory and adds it to the clip.
        If no clip is provided, creates a new audio clip from the audio file.
        """
        self.log.log("[bold blue]🎵 Starting Audio Reading...[/bold blue]")
        audio_files = [
            os.path.join(self.directory, f) for f in os.listdir(self.directory)
            if f.lower().endswith(('.mp3', '.wav', '.aac'))
        ]

        if not audio_files:
            self.log.error(f"No audio files found in directory: {self.directory}")
            raise FileNotFoundError(f"No audio files found in directory: {self.directory}")

        if len(audio_files) > 1:
            self.log.warn(f"Multiple audio files found in directory: {self.directory}. Using the first one found.")

        audio_file = audio_files[0]

        start_time = self.config.get('start_time', 0)
        end_time = self.config.get('end_time', None)

        # Load audio with start and end times if specified
        if start_time != 0 or end_time is not None:
            self.log.log(f"[cyan]✂️ Cropping audio from {start_time} to {end_time} seconds[/cyan]")
            audio_clip = AudioFileClip(audio_file).subclip(start_time, end_time)
            metadata["start_time"] = start_time
            metadata["end_time"] = end_time
        else:
            audio_clip = AudioFileClip(audio_file)

        self.log.log(f"[cyan]🔊 Audio file loaded: {audio_file} with duration {tool.transform_to_MMSS(audio_clip.duration)} seconds[/cyan]")

        if clip is None:
            self.log.warn("No existing video clip provided. Returning audio as new clip.")
            clip = ColorClip(size=(1024, 1024), color=(0, 0, 0), duration=audio_clip.duration)
            self.suggest_frequency_bands(audio_file)    
        else:
            self.log.log("[green]🛠️ Adding audio to existing video clip.[/green]")

        clip = clip.set_audio(audio_clip)
        metadata["audio_file"] = audio_file

        return clip


    def suggest_frequency_bands(self, 
        audio_file, num_bands=4, sr=None, n_fft=2048, hop_length=None
    ):
        # Загружаем аудио файл
        y, sr = librosa.load(audio_file, sr=sr, mono=True)

        if hop_length is None:
            hop_length = n_fft // 4

        # Вычисляем спектрограмму
        S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))

        # Получаем частотные значения
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        # Вычисляем изменение амплитуды по времени для каждой частоты (спектральный флюкс)
        spectral_flux = np.var(S, axis=1)

        # Разбиваем частотный спектр на равные интервалы
        num_freqs = len(frequencies)
        freq_bins = np.linspace(frequencies[0], frequencies[-1], num=500)

        # Суммируем спектральный флюкс в каждом частотном диапазоне
        flux_per_band = []
        for i in range(len(freq_bins) - 1):
            freq_mask = (frequencies >= freq_bins[i]) & (frequencies < freq_bins[i + 1])
            if np.any(freq_mask):
                flux = np.sum(spectral_flux[freq_mask])
                flux_per_band.append((flux, freq_bins[i], freq_bins[i + 1]))

        # Сортируем диапазоны по величине спектрального флюкса (изменчивости)
        flux_per_band.sort(reverse=True, key=lambda x: x[0])

        # Выбираем топ `num_bands` диапазонов
        top_bands = flux_per_band[:num_bands]

        # Сортируем выбранные диапазоны по возрастанию частоты
        top_bands.sort(key=lambda x: x[1])

        # Формируем список диапазонов
        suggested_bands = [(round(band[1]), round(band[2])) for band in top_bands]

        table = Table(title="🎵 Предлагаемые частотные диапазоны")
        table.add_column("№", justify="right")
        table.add_column("Диапазон", justify="left")
        for idx, band in enumerate(suggested_bands):
            table.add_row(str(idx+1), f"{band[0]} - {band[1]} Гц")
        self.log.print(table)

        return suggested_bands
