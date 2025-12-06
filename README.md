# AI Linux Terminal Assistant

Convert natural language into Linux commands using AI.

## Quick Start

### 1. Install Dependencies

```bash
pip3 install openai python-dotenv
```

Or use pip install if pip3 is not available:

```bash
pip install openai python-dotenv
```

For user-level installation:

```bash
pip3 install --user openai python-dotenv
```

### 2. Setup API Key

**Option A: Using .env file (Recommended)**

Create a file named .env in the same directory as ai-terminal.py:

```
OPENAI_API_KEY=your-actual-key-here
```

**Option B: Set environment variable**

For bash/zsh (Linux/Mac):
```bash
OPENAI_API_KEY='your-key-here' python3 ai-terminal.py
```

For csh/tcsh:
```bash
setenv OPENAI_API_KEY your-key-here
python3 ai-terminal.py
```

For Windows CMD:
```cmd
set OPENAI_API_KEY=your-key-here
python ai-terminal.py
```

For Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your-key-here"
python ai-terminal.py
```

**Option C: Enter when prompted**

Simply run the script and it will ask for your key.

### 3. Run the Assistant

```bash
python3 ai-terminal.py
```

## Usage Examples

### Interactive Mode

```bash
python3 ai-terminal.py

What would you like to do? find all PDF files in Documents folder
```

### Direct Command Mode

```bash
python3 ai-terminal.py "list all large files"
```

### Example Commands

- "find all files larger than 100MB"
- "list all running processes"
- "show disk usage"
- "search for text in all Python files"
- "compress all images in current directory"
- "find duplicate files"

## Getting Your API Key

1. Visit https://platform.openai.com/api-keys
2. Sign up for an account (free tier available)
3. Create a new API key
4. Copy the key to your .env file

## Cost Information

- Free tier includes credits for testing
- Average cost: $0.0002 - $0.001 per command
- Uses the cheapest available model automatically
- Typical usage: thousands of commands on free tier

## Security Best Practices

1. Never commit .env file to version control
2. Add .env to .gitignore
3. Keep your API key private
4. Set file permissions: chmod 600 .env
5. Use .env.example as a template (safe to share)

## File Structure

```
ai-terminal-assistant/
├── ai-terminal.py          Main script
├── .env                    Your API key (DO NOT COMMIT)
├── .env.example            Template file (safe to commit)
├── requirements.txt        Python dependencies
├── .gitignore             Git ignore rules
└── README.md              Documentation
```

## Troubleshooting

### "export: Command not found"

Your shell may not support export. Use one of these alternatives:

For csh/tcsh:
```bash
setenv OPENAI_API_KEY your-key-here
```

Or use .env file (recommended):
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

Or run with inline environment variable:
```bash
OPENAI_API_KEY='your-key' python3 ai-terminal.py
```

### "No module named 'openai'"

Install the required packages:
```bash
pip3 install --user openai python-dotenv
```

### "Model not found"

Your API key may not have access to certain models. The script automatically detects available models and uses the cheapest one.

### Permission denied

Make the script executable:
```bash
chmod +x ai-terminal.py
```

## System Requirements

- Python 3.7 or higher
- pip or pip3
- Internet connection
- Valid OpenAI API key

## Supported Shells

- bash
- zsh
- sh
- csh
- tcsh
- fish
- Windows CMD
- Windows PowerShell

## License

MIT License

## Contributing

Contributions are welcome. Please submit pull requests or open issues on GitHub.
