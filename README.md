# AI Terminal Assistant

Convert natural language into terminal commands using AI. **Optimized for Linux** and also works on **macOS** and **Windows**.

Perfect for Linux power users who want to speed up their terminal workflow with natural language commands.

> 🐧 **Linux Users:** See [LINUX_SETUP.md](LINUX_SETUP.md) for a comprehensive Linux-specific guide!

## Quick Start

### Linux Quick Setup (One Command)

For Linux users, run this automated setup script:

```bash
bash setup.sh
```

This will:
- Check Python installation
- Install required packages
- Create secure .env file
- Make the script executable
- Give you alias suggestions

Then just edit the `.env` file with your API key and run `./ai-terminal.py`

### Manual Installation

#### 1. Install Python (Required)

**Python 3.7 or higher is required.** If you don't have Python installed:

| Platform | Installation Command |
|----------|---------------------|
| **Ubuntu/Debian** | `sudo apt install python3 python3-pip` |
| **Fedora/RHEL** | `sudo dnf install python3 python3-pip` |
| **Arch Linux** | `sudo pacman -S python python-pip` |
| **openSUSE** | `sudo zypper install python3 python3-pip` |
| **macOS** | `brew install python3` or https://www.python.org/downloads/macos/ |
| **Windows** | https://www.python.org/downloads/windows/ (check "Add to PATH") |

To verify Python is installed:
```bash
python3 --version
```

#### 2. Install Python Packages

**Linux/macOS (Recommended):**
```bash
pip3 install --user -r requirements.txt
```

Or install packages manually:
```bash
pip3 install --user openai python-dotenv colorama
```

**Windows:**
```bash
pip install -r requirements.txt
# Or: py -m pip install -r requirements.txt
```

#### 3. Setup API Key

**Option A: Using .env file (Recommended for Linux)**

Create a `.env` file in the same directory as ai-terminal.py:

```bash
# Copy the template
cp env.example .env

# Edit with your API key
nano .env

# Set secure permissions (Linux best practice)
chmod 600 .env
```

Your `.env` file should contain:
```
OPENAI_API_KEY=your-actual-key-here
```

**Option B: Set environment variable**

For bash/zsh (Linux/Mac):
```bash
export OPENAI_API_KEY='your-key-here'
python3 ai-terminal.py

# Or run inline:
OPENAI_API_KEY='your-key-here' python3 ai-terminal.py
```

For fish shell:
```bash
set -x OPENAI_API_KEY 'your-key-here'
python3 ai-terminal.py
```

For csh/tcsh:
```bash
setenv OPENAI_API_KEY your-key-here
python3 ai-terminal.py
```

For Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your-key-here"
python ai-terminal.py
```

**Option C: Enter when prompted**

Simply run the script and it will ask for your key.

#### 4. Run the Assistant

**Linux/macOS:**
```bash
# Make executable (first time only)
chmod +x ai-terminal.py

# Run it
./ai-terminal.py

# Or use python3
python3 ai-terminal.py
```

**Windows:**
```bash
python ai-terminal.py
```

**Pro Tip for Linux:** Add an alias to your `~/.bashrc` or `~/.zshrc`:
```bash
alias ai='python3 /path/to/ai-terminal.py'
```
Then reload your shell and use: `ai "your command"`

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

### Linux-Specific Example Commands

**File Operations:**
- "find all files larger than 100MB in my home directory"
- "find duplicate files in current directory"
- "search for TODO comments in all Python files"
- "compress all jpg files while preserving quality"
- "batch rename all files to lowercase"
- "find files modified in the last 24 hours"

**System Administration:**
- "list all running processes sorted by memory usage"
- "show disk usage for each directory"
- "find which process is using port 8080"
- "check system resource usage"
- "list all users logged into the system"
- "show largest log files in /var/log"

**Network Operations:**
- "test if port 443 is open on example.com"
- "show my public IP address"
- "list all listening network ports"
- "check DNS records for a domain"
- "monitor network traffic on eth0"

**Text Processing:**
- "count lines of code in all Python files"
- "find and replace text in all config files"
- "extract all email addresses from log files"
- "sort and deduplicate entries in a file"

**Package Management:**
- "list installed packages with 'python' in name" (apt/dnf)
- "check for available system updates"
- "find which package provides a command"

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

**For Linux Users:**
1. Set secure permissions on .env file: `chmod 600 .env`
2. Never commit .env file to version control (already in .gitignore)
3. Keep your API key private and never share it
4. Consider storing .env in your home directory outside the repo
5. Use `env.example` as a template (safe to share)
6. Review generated commands before executing (especially with sudo)

**General:**
- Always review commands before execution, especially destructive ones
- The assistant marks commands as safe/caution/danger
- You can edit commands before running them (press 'e')
- Start with safe operations while learning the tool

## File Structure

```
ai-terminal-assistant/
├── ai-terminal.py          Main script
├── .env                    Your API key (DO NOT COMMIT)
├── .env.example            Template file (safe to commit)
├── requirements.txt        Python dependencies
├── .gitignore              Git ignore rules
├── setup.sh                Setup script (Linux/macOS)
├── setup.ps1               Setup script (Windows PowerShell)
└── README.md               Documentation
```

## Troubleshooting

### "Python was not found" or "python is not recognized"

Python is not installed or not in your PATH:

1. Download Python from https://www.python.org/downloads/
2. **Windows:** Make sure to check ✅ "Add Python to PATH" during installation
3. **Restart your terminal** after installation
4. Try running `python --version` or `py --version` to verify

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
pip install openai python-dotenv colorama
```

### "Model not found"

Your API key may not have access to certain models. The script automatically detects available models and uses the cheapest one.

### Permission denied

Make the script executable:
```bash
chmod +x ai-terminal.py
```

## System Requirements

- **Python 3.7 or higher** - [Download here](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Internet connection**
- **OpenAI API key** - [Get one here](https://platform.openai.com/api-keys)

## Supported Shells

**Linux/Unix:**
- bash (most common, fully supported)
- zsh (macOS default, fully supported)
- fish (modern shell, fully supported)
- sh (POSIX compliant, fully supported)
- csh/tcsh (legacy, supported)

**Other Platforms:**
- Windows PowerShell
- Windows CMD

The script automatically detects your shell and generates optimized commands.

## License

MIT License

## Contributing

Contributions are welcome. Please submit pull requests or open issues on GitHub.
