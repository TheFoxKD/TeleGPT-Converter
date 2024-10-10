import json
import logging
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum, auto
import argparse
import sys


class LogLevel(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class Message:
    sender: str
    content: str
    timestamp: datetime


class OutputFormat(Enum):
    TEXT = "text"
    JSON = "json"
    CSV = "csv"


class TelegramToGPTConverter:
    def __init__(self, input_file: str, output_file: str, output_format: OutputFormat):
        self.input_file = input_file
        self.output_file = output_file
        self.output_format = output_format
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger("TelegramToGPTConverter")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        if level == LogLevel.INFO:
            self.logger.info(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.ERROR:
            self.logger.error(message)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(message)

    def _load_json(self) -> Dict[str, Any]:
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            self._log("Invalid JSON format in input file", LogLevel.ERROR)
            raise
        except FileNotFoundError:
            self._log(f"Input file not found: {self.input_file}", LogLevel.ERROR)
            raise

    def _parse_messages(self, data: Dict[str, Any]) -> List[Message]:
        messages = []
        for msg in data.get('messages', []):
            try:
                sender = msg['from']
                content = msg['text']
                timestamp = datetime.fromtimestamp(int(msg['date_unixtime']))
                messages.append(Message(sender, content, timestamp))
            except KeyError as e:
                self._log(f"Missing key in message: {e}", LogLevel.WARNING)
        return messages

    def _format_for_text(self, messages: List[Message]) -> str:
        formatted_messages = []
        for msg in messages:
            formatted_msg = f"{msg.sender}, [{msg.timestamp.strftime('%d.%m.%Y %H:%M')}]\n{msg.content}"
            formatted_messages.append(formatted_msg)
        return "\n\n".join(formatted_messages)

    def _format_for_json(self, messages: List[Message]) -> str:
        json_messages = [
            {
                "sender": msg.sender,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
        return json.dumps(json_messages, ensure_ascii=False, indent=2)

    def _format_for_csv(self, messages: List[Message]) -> str:
        csv_lines = ["sender,timestamp,content"]
        for msg in messages:
            csv_line = f'"{msg.sender}","{msg.timestamp.isoformat()}","{msg.content.replace('"', '""')}"'
            csv_lines.append(csv_line)
        return "\n".join(csv_lines)

    def convert(self) -> None:
        try:
            self._log("Starting conversion process")
            data = self._load_json()
            messages = self._parse_messages(data)

            if self.output_format == OutputFormat.TEXT:
                output = self._format_for_text(messages)
            elif self.output_format == OutputFormat.JSON:
                output = self._format_for_json(messages)
            elif self.output_format == OutputFormat.CSV:
                output = self._format_for_csv(messages)
            else:
                raise ValueError(f"Unsupported output format: {self.output_format}")

            with open(self.output_file, 'w', encoding='utf-8') as file:
                file.write(output)

            self._log(f"Conversion completed. Output saved to {self.output_file}")
        except Exception as e:
            self._log(f"An error occurred during conversion: {str(e)}", LogLevel.ERROR)
            raise


def main():
    parser = argparse.ArgumentParser(description="Convert Telegram JSON to GPT-friendly format")
    parser.add_argument("input", help="Path to input JSON file")
    parser.add_argument("output", help="Path to output file")
    parser.add_argument("-f", "--format", choices=[e.value for e in OutputFormat], default=OutputFormat.TEXT.value,
                        help="Output format (default: text)")

    args = parser.parse_args()

    try:
        output_format = OutputFormat(args.format)
        converter = TelegramToGPTConverter(args.input, args.output, output_format)
        converter.convert()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()