from abc import ABC, abstractmethod

class BaseConverter(ABC):
    def __init__(self, directory, config):
        """
        Initialize the base converter with directory and configuration settings.
        :param directory: The directory where media files are located.
        :param config: Configuration settings for the converter.
        """
        self.directory = directory
        self.config = config

    @abstractmethod
    def convert(self, clips, metadata):
        """
        Abstract method that all derived converters must implement.
        This method processes the given clips and returns a list of processed clips.
        :param clips: List of video/audio clips to process.
        :param metadata: Common metadata shared between converters.
        :return: List of processed clips.
        """
        pass


# # Add import path fix to ensure that base_converter is importable from submodules
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))