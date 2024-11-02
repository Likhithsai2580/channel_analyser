# AI YouTube Content Analyzer

An AI-powered tool that analyzes YouTube videos for educational content using Groq's LLM and vision models. The analyzer provides comprehensive insights including transcription, visual analysis, and educational content summaries.

This tool is designed to help educators, content creators, and learners extract valuable information from YouTube videos. It automatically processes videos to identify key educational concepts, generate detailed summaries, and provide visual content analysis, making it easier to understand and utilize educational content on YouTube.

## Features

- Video download and frame extraction
- Speech-to-text transcription using Groq's Whisper integration
- Visual content analysis using Llama Vision models
- Educational content summarization
- Rate-limited API calls
- Automatic resource cleanup
- Detailed content analysis reports
- Support for multiple video formats
- Batch processing capabilities
- Custom output formatting options

## Prerequisites

- Python 3.9+
- Groq API key
- FFmpeg (for video processing)

## Installation

1. Clone the repository: `git clone https://github.com/Likhithsai2580/YT-VID-ANALYSER.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Set up the Groq API key by adding it to the `GROQ_API_KEY` environment variable.

## Usage

1. Run the script: `python main.py`
2. Follow the prompts to input the YouTube video URL and configure the analysis options.
3. The script will process the video, generate a detailed analysis report, and display the results.

## Customization

You can customize the analysis options and output format by modifying the `main.py` script. Refer to the Groq and Llama Vision documentation for more information on available models and parameters.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or suggestions, please contact semalalikithsai@gmail.com.

Enjoy using the AI YouTube Content Analyzer!