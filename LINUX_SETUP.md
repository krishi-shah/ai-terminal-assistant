# Linux Quick Setup Guide

This guide is specifically for Linux users who want to get started quickly with the AI Terminal Assistant.

## One-Line Installation

```bash
bash setup.sh
```

That's it! The script will:
- ✓ Detect your Linux distribution
- ✓ Check Python installation
- ✓ Install required packages
- ✓ Create a secure .env file
- ✓ Make the script executable
- ✓ Provide alias suggestions

## Manual Installation (Step by Step)

### 1. Install Python 3 (if not already installed)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install python3 python3-pip -y
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**openSUSE:**
```bash
sudo zypper install python3 python3-pip
```

### 2. Install Python Dependencies

```bash
pip3 install --user openai python-dotenv colorama
```

### 3. Setup Your API Key

```bash
# Copy the example file
cp env.example .env

# Edit with your preferred editor
nano .env    # or vim, gedit, etc.

# Set secure permissions (important!)
chmod 600 .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your key from: https://platform.openai.com/api-keys

### 4. Make Script Executable

```bash
chmod +x ai-terminal.py
```

### 5. Run It!

```bash
./ai-terminal.py
```

Or:
```bash
python3 ai-terminal.py
```

## Pro Tips for Linux Users

### Create a Global Alias

Add this to your `~/.bashrc` (or `~/.zshrc` if using zsh):

```bash
alias ai='python3 /full/path/to/ai-terminal.py'
```

Then reload your shell:
```bash
source ~/.bashrc
```

Now you can use it anywhere:
```bash
ai "find all log files larger than 100MB"
```

### Use with Direct Commands

```bash
./ai-terminal.py "list all running docker containers"
./ai-terminal.py "show disk usage"
./ai-terminal.py "find python files with TODO comments"
```

### Shell Detection

The tool automatically detects your shell:
- ✓ bash
- ✓ zsh
- ✓ fish
- ✓ csh/tcsh

Commands are optimized for your specific shell environment.

## Troubleshooting

### "pip3: command not found"

Install pip:
```bash
# Ubuntu/Debian
sudo apt install python3-pip

# Fedora/RHEL
sudo dnf install python3-pip

# Arch
sudo pacman -S python-pip
```

### "Permission denied" when running script

Make it executable:
```bash
chmod +x ai-terminal.py
```

### Import errors

Ensure packages are installed:
```bash
pip3 install --user openai python-dotenv colorama

# Or without --user flag
pip3 install openai python-dotenv colorama
```

### API key not found

Make sure your .env file:
1. Is in the same directory as ai-terminal.py
2. Has the correct format: `OPENAI_API_KEY=your-key`
3. Has secure permissions: `chmod 600 .env`

## Common Linux Use Cases

**System Administration:**
```bash
ai "show failed systemd services"
ai "list users logged in"
ai "check nginx service status"
```

**File Management:**
```bash
ai "find all files modified today"
ai "compress all logs older than 7 days"
ai "find duplicate files"
```

**Network Operations:**
```bash
ai "show which process is using port 3000"
ai "test connection to server on port 22"
ai "show my public IP"
```

**Development:**
```bash
ai "count lines of code in all python files"
ai "find TODO comments in source files"
ai "show git branches sorted by last commit date"
```

## Security Best Practices

1. **Secure your .env file:**
   ```bash
   chmod 600 .env
   ```

2. **Never commit .env to git** (already in .gitignore)

3. **Review commands before executing**, especially:
   - Commands with `sudo`
   - Commands with `rm -rf`
   - Commands modifying system files

4. **Start with safe commands** to get familiar with the tool

## System Requirements

- Linux (any distribution)
- Python 3.7 or higher
- Internet connection
- OpenAI API key

## Getting Help

- Check `README.md` for general documentation
- Check `EXAMPLES.md` for command examples
- Open an issue on GitHub for bugs or questions

---

**Enjoy your AI-powered Linux terminal! 🐧**

