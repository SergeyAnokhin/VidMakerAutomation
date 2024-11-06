from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from hierarchical_logger import HierarchicalLogger
from rich.console import Console
import time
from tool import transform_to_MMSS

class BaseConverter(ABC):
    config = {}
    
    def __init__(self, directory, config, logger: HierarchicalLogger):
        """
        Initialize the base converter with directory and configuration settings.
        :param directory: The directory where media files are located.
        :param config: Configuration settings for the converter.
        """
        self.directory = directory
        self.config = config or {}
        self.mylog = logger
        self.log = logger.sub_logger()

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

    def convert_async(self, clips, metadata, method):
        """
        Convert a single clip synchronously.
        """
        converter_name = self.__class__.__name__
        with ThreadPoolExecutor() as executor:
            self.mylog.log(f"{converter_name}: [blue]Multiple clips detected, processing in parallel[/blue]")
            self.log_clip_conversion(converter_name)
            results = list(executor.map(lambda clip: method(clip, metadata), clips))
        return results

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
            return self.convert_async(clips, metadata, self.convert)
        else:
            self.mylog.log(f"{converter_name}: [blue]Single clip detected, processing sequentially[/blue]")
            self.log_clip_conversion(converter_name)
            first_clip = clips[0] if len(clips) > 0 else None
            results = [self.convert(first_clip, metadata)]

        self.log_execution_time(start_time)
        return results

    def log_execution_time(self, start_time):
        """
        Logs the time taken for an operation in minutes and seconds.
        :param start_time: The starting time of the operation.
        :param message_prefix: Prefix message to display before the elapsed time.
        """
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.mylog.log(f"[green]-.-.-.-.- ✅Processing completed in {transform_to_MMSS(elapsed_time)} -.-.-.-.-[/green]")

    def log_clip_conversion(self, converter_name):
        """
        Logs that a clip is being converted by the specified converter.
        :param converter_name: The name of the converter.
        """
        self.mylog.log(f"[green]-.-.-.-.- ⏩Converting clip using {converter_name}... -.-.-.-.-[/green]")
