# TeleGPT Converter

TeleGPT Converter is a Python utility that transforms Telegram chat JSON data into GPT-friendly formats. It helps prepare conversation data for easy processing by AI language models.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

## Features

- Convert Telegram JSON export to GPT-friendly formats
- Support for multiple output formats: Text, JSON, and CSV
- Command-line interface for easy integration with scripts
- Robust error handling and logging
- Type hints for improved code readability and maintainability

## Installation

1. Ensure you have Python 3.7 or higher installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/TheFoxKD/TeleGPT-Converter.git
   cd telegpt-converter
   ```

3. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

## Usage

Run the script from the command line with the following syntax:

```
python telegpt_converter.py input_file output_file [-f FORMAT]
```

- `input_file`: Path to the input Telegram JSON file
- `output_file`: Path where the output file will be saved
- `-f FORMAT` or `--format FORMAT`: (Optional) Output format. Choose from `text` (default), `json`, or `csv`

### Examples

1. Convert to text format (default):
   ```
   python telegpt_converter.py telegram_export.json gpt_friendly_chat.txt
   ```

2. Convert to JSON format:
   ```
   python telegpt_converter.py telegram_export.json gpt_friendly_chat.json -f json
   ```

3. Convert to CSV format:
   ```
   python telegpt_converter.py telegram_export.json gpt_friendly_chat.csv -f csv
   ```

## Input Format

The input should be a JSON file exported from Telegram, typically containing a structure like this:

```json
{
  "name": "Chat Name",
  "type": "personal_chat",
  "id": 1234567890,
  "messages": [
    {
      "id": 1,
      "type": "message",
      "date": "2023-01-01T12:00:00",
      "date_unixtime": "1672574400",
      "from": "User Name",
      "from_id": "user123456789",
      "text": "Hello, world!",
      "text_entities": [
        {
          "type": "plain",
          "text": "Hello, world!"
        }
      ]
    },
    // More messages...
  ]
}
```

## Output Formats

### Text Format (Default)
```
User Name, [01.01.2023 12:00]
Hello, world!

Another User, [01.01.2023 12:05]
Hi there!
```

### JSON Format
```json
[
  {
    "sender": "User Name",
    "content": "Hello, world!",
    "timestamp": "2023-01-01T12:00:00"
  },
  {
    "sender": "Another User",
    "content": "Hi there!",
    "timestamp": "2023-01-01T12:05:00"
  }
]
```

### CSV Format
```csv
sender,timestamp,content
"User Name","2023-01-01T12:00:00","Hello, world!"
"Another User","2023-01-01T12:05:00","Hi there!"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Telegram team for their chat export feature
- Inspired by the need for easy-to-process chat data for GPT models