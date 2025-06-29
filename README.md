# YouTube Shorts Automation

## Description
A command-line tool to automate the creation and upload of YouTube Shorts, combining Google Data API for media management and OpenAI ChatGPT API for script generation.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- Automates YouTube Shorts upload via Google Data API (OAuth2)
- Generates video scripts and dialogues using OpenAI ChatGPT API
- Supports scheduling and state management for batch uploads
- Integrated with Google Cloud Storage for media retrieval

## Prerequisites
- Python 3.8 or higher
- `git` command-line tool
- Google Cloud project with YouTube Data API enabled
- OpenAI API key
- OAuth2 client credentials JSON for YouTube API

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/gurdahari/YouTubeShortsAutomation.git
   cd YouTubeShortsAutomation
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Copy the example config file and update placeholders:
   ```bash
   cp config_example.py config.py
   ```
2. Set environment variables or edit `config.py` to include:
   ```python
   # config.py
   PROJECT_ID = "<YOUR_GCP_PROJECT_ID>"
   GCS_BUCKET_NAME = "<YOUR_BUCKET_NAME>"
   OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
   YOUTUBE_CREDENTIALS_FILE = os.environ.get("YOUTUBE_CLIENT_SECRETS")
   ```
3. Ensure your OAuth2 credentials JSON and GCS key files are accessible and ignored by Git:
   ```bash
   # .gitignore
   *.json
   .env
   ```

## Usage
Run the main script to start an upload session or schedule batch jobs:
```bash
python main_youtube.py --upload --file <SHORT_VIDEO_FILE>
```
For detailed options, see:
```bash
python main_youtube.py --help
```

## Project Structure
```
├── config.py            # Project configuration (env variables)
├── gcs_handler.py       # Google Cloud Storage utilities
├── oauth_youtube.py     # OAuth2 setup for YouTube Data API
├── youtube_handler.py   # YouTube API wrapper functions
├── openai_handler.py    # OpenAI ChatGPT integration
├── main_youtube.py      # Orchestration of workflow
└── requirements.txt     # Python dependencies
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request and describe your changes

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
