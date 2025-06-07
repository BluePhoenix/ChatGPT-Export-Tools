# ChatGPT Export Tools

A collection of Python scripts to help manage and organize ChatGPT conversation exports from OpenAI. These tools help you clean, split, and index your ChatGPT conversations for better organization and searchability.

## Why This Exists

When you export your ChatGPT conversations from OpenAI, you get a single JSON file containing all your conversations. This project provides tools to:

1. Clean and analyze your conversations
2. Split them into individual markdown files for better readability
3. Create a searchable index of your conversations
4. Help you decide which conversations to keep or delete

## Features

- **Chat Cleaner** (`chat_cleaner.py`): Generates a CSV overview of all conversations with metadata and previews
- **Chat Splitter** (`split_chats.py`): Converts the JSON export into individual markdown files and optionally creates a searchable SQLite database

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd chatgpt-export-tools
```

2. Ensure you have Python 3.6+ installed

## Usage

### 1. Export Your ChatGPT Data

First, export your ChatGPT data from OpenAI:
1. Go to ChatGPT settings
2. Click "Export Data"
3. Download the export 
4. Extract the file sent over by OpenAI
5. In the extracted files you'll receive a `conversations.json` file which is used by this script.

### 2. Clean and Analyze Conversations

To get an overview of all your conversations:

```bash
python scripts/chat_cleaner.py conversations.json
```

This creates a `chats.csv` file that you can open in Excel/Google Sheets or import into Notion. The CSV includes:
- Conversation ID
- Title
- Creation time
- Last activity
- Number of messages
- Preview of the conversation

### 3. Split Conversations into Markdown Files

To split your conversations into individual markdown files:

```bash
python scripts/split_chats.py conversations.json
```

> **Experimental Feature**: Full-Text Search Database
> 
> You can optionally create a searchable SQLite database using the `--fts` flag:
> 
> ```bash
> python scripts/split_chats.py conversations.json --fts
> ```
> 
> This will create a `chats.db` file with a full-text search index. Note that this feature is currently experimental and hasn't been thoroughly tested. The core markdown file generation works independently of this feature.
> 
> If you use this feature and encounter any issues, please report them in the project's issue tracker.

Output:
- `out/` directory containing individual markdown files (named `YYYY-MM-DD_title-slug.md`)
- `chats.db` (if using `--fts`) - A SQLite database with full-text search capabilities (experimental)

## File Structure

```
.
├── scripts/
│   ├── chat_cleaner.py    # Generates CSV overview of conversations
│   └── split_chats.py     # Splits conversations into markdown files
├── exports/               # Place your OpenAI export here
└── out/                   # Generated markdown files
```

## Important Notice

This tool is provided as-is for processing your own ChatGPT conversation exports. Users are responsible for:
- Ensuring they have the right to export and process their ChatGPT conversations
- Complying with OpenAI's terms of service regarding their data
- Protecting their privacy and the privacy of others when processing conversations
- Using the tool responsibly and ethically

The MIT License below covers the code itself, but does not override or modify any terms of service or privacy requirements from OpenAI or other services.

## License

MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenAI for providing the ChatGPT export functionality
- The Python community for the excellent libraries used in this project 
