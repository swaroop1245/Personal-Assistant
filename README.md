# Personal Assistant

A conversational AI assistant built with Gradio and OpenAI that acts as a personal representative, answering questions about career, background, skills, and experience. The assistant uses PDF documents (resume and profile) to provide accurate information about the person it represents.

## Features

- 🤖 **AI-Powered Chat Interface**: Interactive chat interface built with Gradio
- 📄 **Document Integration**: Automatically extracts and uses information from PDF resumes and profiles
- 🔔 **Notification System**: Integrates with Pushover for recording user interactions and unanswered questions
- 🎨 **Modern UI**: Beautiful, responsive web interface with custom styling
- 🔧 **Function Calling**: Uses OpenAI function calling to record user details and track unknown questions

## Project Structure

```
Personal-Assistant/
├── app.py              # Main Gradio application
├── main.py             # Entry point
├── me/                 # Personal documents folder
│   ├── Profile.pdf     # LinkedIn profile (ignored by git)
│   ├── Swaroop_resume (1).pdf  # Resume (ignored by git)
│   └── summary.txt     # Summary text file
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

**Note**: `large_folder.py` (deployment script) and `uv.lock` are excluded from version control. Personal PDFs in the `me/` folder are also ignored for privacy.

## Prerequisites

- Python 3.12 or higher
- OpenAI API key
- Pushover account (optional, for notifications)
- Hugging Face account (optional, for deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Personal-Assistant
```

2. Install dependencies:

Using pip:
```bash
pip install -r requirements.txt
```

Or using uv (recommended):
```bash
uv sync
```

**Note**: If using `uv`, the `uv.lock` file will be generated but is excluded from version control.

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
PUSHOVER_TOKEN=your_pushover_token_here
PUSHOVER_USER=your_pushover_user_here
HF_TOKEN=your_huggingface_token_here  # Optional, for deployment
PORT=7860  # Optional, default port for Gradio
GRADIO_SHARE=false  # Optional, set to true for public sharing
```

4. Add your personal documents:
   - Place your profile PDF in `me/Profile.pdf`
   - Place your resume PDF in `me/Swaroop_resume (1).pdf`
   - Add a summary text file in `me/summary.txt`

## Usage

### Running Locally

Run the main application:
```bash
python app.py
```

The Gradio interface will be available at `http://localhost:7860` (or the port specified in your `.env` file).

### Deployment to Hugging Face Spaces

For deployment to Hugging Face Spaces, you'll need to create a deployment script (similar to `large_folder.py`). The script should:

1. Create or update a Hugging Face Space repository
2. Upload the necessary files while excluding sensitive data
3. Configure the space with Gradio SDK

Make sure to set the `HF_TOKEN` environment variable before running any deployment script.

**Note**: Deployment scripts are excluded from version control for security reasons.

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required. Your OpenAI API key for GPT-4o-mini model
- `PUSHOVER_TOKEN`: Optional. Pushover API token for notifications
- `PUSHOVER_USER`: Optional. Pushover user key for notifications
- `HF_TOKEN`: Optional. Hugging Face token for deployment
- `PORT`: Optional. Port number for Gradio server (default: 7860)
- `GRADIO_SHARE`: Optional. Set to "true" to enable public sharing link

### Customization

To customize the assistant for a different person:
1. Update the `name` variable in the `Me` class in `app.py`
2. Replace the PDF files in the `me/` folder
3. Update the `summary.txt` file with relevant information
4. Modify the system prompt in the `system_prompt()` method if needed

## Dependencies

- `gradio>=5.49.1` - Web interface framework
- `openai>=2.8.0` - OpenAI API client
- `pypdf>=6.2.0` - PDF text extraction
- `python-dotenv>=1.2.1` - Environment variable management
- `requests>=2.32.5` - HTTP requests for Pushover API
- `huggingface_hub` - For Hugging Face deployment (optional)

## Features in Detail

### Function Calling
The assistant uses OpenAI function calling to:
- **Record user details**: Captures email addresses and names of interested users
- **Track unknown questions**: Records questions that couldn't be answered for later review

### Document Processing
- Automatically extracts text from PDF resumes and profiles
- Combines information from multiple sources to provide comprehensive answers
- Uses a summary file for quick reference

## License

This project is for personal use.

## Security & Privacy

- Personal documents (PDFs) in the `me/` folder are excluded from version control
- Environment variables (`.env`) are never committed to the repository
- Deployment scripts and certificates are excluded from version control
- The assistant never shares personal phone numbers with users

## Notes

- The assistant is designed to represent a specific person (currently Swaroop Talakwar)
- All user interactions and unanswered questions are logged via Pushover (if configured)
- The assistant encourages users to provide their email for follow-up contact
- The project uses `uv.lock` for dependency locking, which is excluded from version control
