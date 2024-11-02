from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from tool import log_execution_time, log_clip_conversion
from rich.console import Console
import time
console = Console()

class BaseConverter(ABC):
    config = {}
    
    def __init__(self, directory, config):
        """
        Initialize the base converter with directory and configuration settings.
        :param directory: The directory where media files are located.
        :param config: Configuration settings for the converter.
        """
        self.directory = directory
        self.config = config or {}

    @abstractmethod
    def convert(self, clip, metadata):
        """
        Abstract method that all derived converters must implement.
        This method processes the given clip or list of clips and returns a processed clip or list of clips.
        :param clip: Video/audio clip or list of clips to process.
        :param metadata: Common metadata shared between converters.
        :return: Processed clip or list of processed clips.
        """
        pass

    def process(self, clips, metadata):
        """
        Manages single or multi-clip processing.
        If more than one clip is provided, runs the processing in parallel.
        :param clips: List of clips to process.
        :param metadata: Metadata shared across converters.
        :return: List of processed clips.
        """
        start_time = time.time()
        converter_name = self.__class__.__name__

        if len(clips) > 1:
            with ThreadPoolExecutor() as executor:
                console.print(f"{converter_name}: [blue]Multiple clips detected, processing in parallel[/blue]")
                log_clip_conversion(converter_name)
                results = list(executor.map(lambda clip: self.convert(clip, metadata), clips))
        else:
            console.print(f"{converter_name}: [blue]Single clip detected, processing sequentially[/blue]")
            log_clip_conversion(converter_name)
            first_clip = clips[0] if len(clips) > 0 else None
            results = [self.convert(first_clip, metadata)]

        log_execution_time(start_time)
        return results

