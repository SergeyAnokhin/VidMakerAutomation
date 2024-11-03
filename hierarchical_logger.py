from rich.console import Console
from rich.text import Text

# Инициализация консоли
console = Console()

class HierarchicalLogger:
    def __init__(self, indent_level=0, indent_step=2, prefix=""):
        self.indent_level = indent_level  # Текущий уровень отступа
        self.indent_step = indent_step    # Количество пробелов для одного уровня
        self.prefix = prefix

    def print(self, message):
        console.print(message)

    def log(self, message):
        # Создаем текст с отступом
        text = self.prefix + " " * self.indent_level + message
        console.print(text)

    def error(self, text):
        message = self.prefix + " " * self.indent_level + f"[red]❌ {message}[/red]"
        console.print(message)

    def warn(self, text):
        message = self.prefix + " " * self.indent_level + f"[yellow]⚠️ {text}[/yellow]"
        console.print(message)

    def sub_logger(self, prefix=""):
        # Создаем новый логгер с увеличенным уровнем отступа
        return HierarchicalLogger(self.indent_level + self.indent_step, prefix)

# # Основной логгер
# logger = HierarchicalLogger()

# # Логируем основной компонент
# logger.log("Main component")

# # Под-компонент с увеличенным уровнем отступа
# sub_logger = logger.sub_logger()
# sub_logger.log("Sub component")

# # Под-под-компонент
# sub_sub_logger = sub_logger.sub_logger()
# sub_sub_logger.log("Sub-sub component")
