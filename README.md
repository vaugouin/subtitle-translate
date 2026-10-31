# Subtitle Translator 🎬

A streamlined web application for translating subtitle files (.srt) to various languages using OpenAI's language models with optimized batch processing.

## Overview

Subtitle Translator is a Streamlit-based application that allows users to easily translate subtitle files (.srt) into multiple languages. The application leverages OpenAI's powerful language models to provide high-quality translations while maintaining the original subtitle timing and formatting.

## Features

- **Extensive Language Support**: Translate subtitles to 21 languages including French, English, Spanish, German, Italian, Portuguese, Polish, Japanese, Chinese, Korean, Arabic, Hindi, Russian, Bengali, Indonesian, Malay, Turkish, Vietnamese, Thai, Urdu, and Swahili
- **Optimized Batch Processing**: Groups multiple subtitle chunks into a single API call, significantly reducing API costs and improving performance
- **Configurable Group Size**: Adjust the number of chunks processed per API call via the user interface
- **SRT File Processing**: Handles .srt files with proper formatting preservation
- **Error Handling**: Robust error handling with detailed logging for troubleshooting
- **Debug Information**: Provides debug information and logs for transparency
- **Download Options**: Download translated subtitles as .srt files
- **Multiple Encoding Support**: Handles various file encodings (UTF-8, CP1251, ISO-8859-5, UTF-16)

## Requirements

- Python 3.12+
- OpenAI API key
- Required Python packages (see `requirements.txt`):
  - streamlit==1.32.0
  - openai>=1.55,<2
  - python-dotenv>=1.0.0

The translation model defaults to `gpt-6-sol` (OpenAI SDK, low reasoning effort); set the `OPENAI_MODEL` environment variable to override it.

## Installation

### Local Installation

1. Clone the repository or download the source code
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```
4. Open your browser and navigate to `http://localhost:8501`

### Docker Installation

The application can also be run using Docker:

1. Build the Docker image:
   ```
   docker build -t subtitle-translator .
   ```
2. Run the container:
   ```
   docker run -p 8501:8501 subtitle-translator
   ```
3. Access the application at `http://localhost:8501`

Alternatively, use docker-compose:
```
docker-compose up
```

In production the app runs in Docker through `subtitle-translate.sh` (`docker compose up -d --build`).

## Usage

1. Enter your OpenAI API key in the sidebar
2. Upload your .srt subtitle file
3. Select the target language for translation
4. Adjust the group size in the sidebar settings (optional)
5. Click "Translate"
6. Wait for the translation process to complete
7. Download the translated subtitle file

## Logging

The application includes comprehensive logging capabilities that can be enabled by setting `logging_enabled = True` in the `app.py` file. Logs are stored in the `logs` directory.

## Tests

`normalize_srt.py` holds the SRT cue splitter (`f_split_srt_blocks`) used by `app.py`, plus a normalization CLI. `test-srt-blocks.py` checks the splitter offline (no Streamlit, no API key): `uv run --no-project python -B test-srt-blocks.py`.

## License

MIT License, see [LICENSE](LICENSE).

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)

## Recent Improvements

### June 2025 Updates

- **Optimized Translation Processing**: Implemented a grouping mechanism that combines multiple subtitle chunks into a single API call, significantly reducing the number of API calls and improving performance
- **Configurable Group Size**: Added a slider in the sidebar to let users adjust how many chunks are processed in a single API call (1-10)
- **Expanded Language Support**: Added support for 11 additional languages with large global audiences:
  - Arabic
  - Hindi
  - Russian
  - Bengali
  - Indonesian
  - Malay
  - Turkish
  - Vietnamese
  - Thai
  - Urdu
  - Swahili
