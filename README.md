# Subtitle Translator 🎬

A streamlined web application for translating subtitle files (.srt) to various languages using OpenAI's language models.

## Overview

Subtitle Translator is a Streamlit-based application that allows users to easily translate subtitle files (.srt) into multiple languages. The application leverages OpenAI's powerful language models to provide high-quality translations while maintaining the original subtitle timing and formatting.

## Features

- **Multiple Language Support**: Translate subtitles to French, English, Spanish, German, Italian, Portuguese, Polish, Japanese, Chinese, and Korean
- **SRT File Processing**: Handles .srt files with proper formatting preservation
- **Batch Processing**: Efficiently processes subtitles in chunks to optimize translation quality and API usage
- **Error Handling**: Robust error handling with detailed logging for troubleshooting
- **Debug Information**: Provides debug information and logs for transparency
- **Download Options**: Download translated subtitles as .srt files
- **Multiple Encoding Support**: Handles various file encodings (UTF-8, CP1251, ISO-8859-5, UTF-16)

## Requirements

- Python 3.12+
- OpenAI API key
- Required Python packages (see `requirements.txt`):
  - streamlit==1.32.0
  - langchain-openai==0.0.8
  - langchain==0.1.11
  - langchain-core==0.1.31

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

## Usage

1. Enter your OpenAI API key in the sidebar
2. Upload your .srt subtitle file
3. Select the target language for translation
4. Click "Translate"
5. Wait for the translation process to complete
6. Download the translated subtitle file

## Utilities

### SRT Normalization

The project includes a utility script (`normalize_srt.py`) for normalizing SRT files before translation:

```
python normalize_srt.py path/to/subtitles.srt -o path/to/output.srt
```

This helps ensure proper formatting and compatibility with the translator.

## Logging

The application includes comprehensive logging capabilities that can be enabled by setting `logging_enabled = True` in the `app.py` file. Logs are stored in the `logs` directory.

## License

This project is open source and available for personal and commercial use.

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://www.langchain.com/) and [OpenAI](https://openai.com/)
