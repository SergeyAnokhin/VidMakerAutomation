from rich.console import Console
import time

console = Console()

def log_execution_time(start_time, message_prefix="Processing completed in"):
    """
    Logs the time taken for an operation in minutes and seconds.
    :param start_time: The starting time of the operation.
    :param message_prefix: Prefix message to display before the elapsed time.
    """
    end_time = time.time()
    elapsed_time = end_time - start_time
    console.print(f"[green]{message_prefix} {transform_to_MMSS(elapsed_time)}[/green]")

def log_clip_conversion(converter_name):
    """
    Logs that a clip is being converted by the specified converter.
    :param converter_name: The name of the converter.
    """
    console.print(f"[cyan]Converting clip using {converter_name}...[/cyan]")




def transform_to_MMSS(seconds: int) -> str:
    return time.strftime('%M:%S', time.gmtime(seconds))

# def transform_to_MMSS(seconds: int) -> str:
#     return f"{int(seconds // 60)}:{int(seconds % 60):02d}"