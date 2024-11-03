from rich.console import Console
from rich.text import Text
from rich.table import Table
import re
from datetime import datetime
from pathlib import Path

# Инициализация консоли
console = Console()

class HierarchicalLogger:
    def __init__(self, indent_level=0, indent_step=2, prefix="", directory="./logs"):
        self.indent_level = indent_level  # Текущий уровень отступа
        self.indent_step = indent_step    # Количество пробелов для одного уровня
        self.prefix = prefix
        
        # Используем переданную директорию вместо фиксированной
        self.log_dir = Path(directory)
        
        # Создаем новый файл с текущей датой и временем
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"log_{timestamp}.md"
        
    def _convert_rich_to_markdown(self, message):

        # Если это таблица, обрабатываем особым образом
        if isinstance(message, Table):
            markdown_table = self._convert_table_to_markdown(message)
            return "\n" + markdown_table
                
        """Конвертирует форматирование Rich в Markdown с учетом иерархии"""
        # Сначала конвертируем Rich теги
        conversions = {
            r'\[red\](.*?)\[\/red\]': r'**❌ <span style="color:red">\1</span>**',
            r'\[yellow\](.*?)\[\/yellow\]': r'**⚠️ <span style="color:yellow">\1</span>**', 
            r'\[green\](.*?)\[\/green\]': r'**✅ <span style="color:green">\1</span>**',
            r'\[blue\](.*?)\[\/blue\]': r'*<span style="color:blue">\1</span>*',
            r'\[bold blue\](.*?)\[\/bold blue\]': r'**<span style="color:blue">\1</span>**',
            r'\[cyan\](.*?)\[\/cyan\]': r'<span style="color:cyan">\1</span>',
            r'\[grey\](.*?)\[\/grey\]': r'<span style="color:grey">\1</span>',
        }
        
        for pattern, replacement in conversions.items():
            message = re.sub(pattern, replacement, message)

        # Определяем уровень отступа для Markdown (2 пробела = 1 уровень)
        indent_level = self.indent_level // 2
        
        # Создаем маркер списка в зависимости от уровня отступа
        if indent_level == 0:
            prefix = "- "
        else:
            prefix = "  " * (indent_level - 1) + "  - "
        
        # Добавляем маркер списка и обрабатываем многострочные сообщения
        return "\n" + prefix + message

    def _convert_table_to_markdown(self, table: Table) -> str:
        headers = [col.header for col in table.columns]
        markdown = "| " + " | ".join(headers) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        # Determine the number of rows
        num_rows = len(table.columns[0]._cells) if table.columns else 0
        
        # Extract the rows
        for i in range(num_rows):
            row_data = [str(table.columns[j]._cells[i]) for j in range(len(headers))]
            markdown += "| " + " | ".join(row_data) + " |\n"
        
        return markdown

    def _write_to_file(self, message):
        """Записывает сообщение в файл с учетом иерархии"""
        try:
            md_message = self._convert_rich_to_markdown(message)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(md_message + "\n")
        except Exception as e:
            console.print(f"[red]Error writing to log file: {str(e)}[/red]")

    def print(self, message):
        console.print(message)
        self._write_to_file(message)

    def log(self, message):
        text = self.prefix + " " * self.indent_level + str(message)
        console.print(text)
        self._write_to_file(text)

    def error(self, text):
        message = self.prefix + " " * self.indent_level + f"[red]❌ {text}[/red]"
        console.print(message)
        self._write_to_file(message)

    def warn(self, text):
        message = self.prefix + " " * self.indent_level + f"[yellow]⚠️ {text}[/yellow]"
        console.print(message)
        self._write_to_file(message)

    def sub_logger(self, prefix=""):
        # Передаем ту же директорию в под-логгер
        logger = HierarchicalLogger(
            self.indent_level + self.indent_step, 
            self.indent_step, 
            prefix,
            directory=self.log_dir
        )
        logger.log_file = self.log_file
        return logger

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
