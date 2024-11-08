class AudioPart:
    start_time: float
    end_time: float
    audio_file: str
    sample_rate: int

    def __init__(self, start_time, end_time, audio_file, sample_rate=48000):
        self.start_time = start_time
        self.end_time = end_time
        self.audio_file = audio_file
        self.sample_rate = sample_rate

        self.offset = start_time

        if end_time is not None:
            self.duration = end_time - start_time
        else:
            self.duration = None
