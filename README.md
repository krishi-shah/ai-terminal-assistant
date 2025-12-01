# 🤖 AI Linux Terminal Assistant

Transform natural language into powerful Linux commands instantly! No more memorizing complex syntax or searching through man pages.

## ✨ Features

- 🗣️ **Natural Language**: Describe what you want in plain English
- ⚡ **Instant Commands**: AI generates optimized Linux commands
- 🛡️ **Safety First**: Color-coded warnings for dangerous operations
- 📝 **Learn as You Go**: Every command comes with detailed explanations
- 🎨 **Beautiful Interface**: Clean, terminal-inspired design
- 🔄 **Multiple Modes**: Interactive, direct command, or auto-execute

## 🎥 Demo

```bash
➜ What would you like to do? find all video files larger than 500MB in my Videos folder

🤖 Processing: find all video files larger than 500MB in my Videos folder
⏳ Generating command...

╔═══ Generated Command ═══╗
  find ~/Videos -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mkv" \) -size +500M
╚═════════════════════════╝

📝 Explanation:
  Searches the Videos directory for MP4, AVI, and MKV files larger than 500MB

✅ Safety Level: SAFE
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- **Anthropic API Key** (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/krishi-shah/ai-terminal-assistant.git
   cd ai-terminal-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### API Key Options

This tool supports **two AI providers** - use whichever you prefer:

**Option 1: Anthropic Claude (Recommended)**
- More accurate for Linux commands
- Better at following JSON format
- Cost: ~$0.001-0.003 per command
- Get key: [https://console.anthropic.com/](https://console.anthropic.com/)
```bash
export ANTHROPIC_API_KEY='your-claude-key'
```

**Option 2: OpenAI GPT-4**
- Widely available
- Good alternative
- Cost: ~$0.003-0.01 per command (GPT-4)
- Get key: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
```bash
export OPENAI_API_KEY='your-openai-key'
```

**Note:** If both keys are set, Claude will be used by default. To use GPT-3.5-turbo (cheaper), edit line 286 in `ai-terminal.py` and change `model="gpt-4"` to `model="gpt-3.5-turbo"`.
```

---

### 3. **.env.example** - UPDATE THIS

**Old version:**
```
ANTHROPIC_API_KEY=your_api_key_here
```

**New version:**
```
# AI Provider API Keys (set at least one)
# Option 1: Anthropic Claude (Recommended)
ANTHROPIC_API_KEY=your_claude_key_here

# Option 2: OpenAI GPT
OPENAI_API_KEY=your_openai_key_here

# Note: If both are set, Claude will be used by default
   
   **Option C - .env file**
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   ```

5. **Make the script executable**
   ```bash
   chmod +x ai-terminal.py
   ```

6. **Run it!**
   ```bash
   ./ai-terminal.py
   ```

### Optional: Install Globally

To use `ai-terminal` from anywhere:

```bash
sudo cp ai-terminal.py /usr/local/bin/ai-terminal
sudo chmod +x /usr/local/bin/ai-terminal

# Now you can use it anywhere:
ai-terminal "find large files"
```

## 📖 Usage

### Interactive Mode (Recommended for Beginners)

```bash
./ai-terminal.py
```

Then type commands in plain English:
- "find all PDF files in my Documents folder"
- "show me the 10 largest files"
- "compress all images in the current directory"
- "list all running Python processes"

### Direct Command Mode

Execute a single command:

```bash
./ai-terminal.py "find all files modified today"
./ai-terminal.py "create a backup of my config files"
```

### Auto-Execute Mode

Automatically run safe commands without confirmation:

```bash
./ai-terminal.py --auto "show disk usage"
./ai-terminal.py --auto "list directory contents sorted by size"
```

⚠️ **Note**: Auto-execute only works for commands marked as "safe". Dangerous commands still require confirmation.

## 🎯 Example Commands

| What You Say | Generated Command |
|--------------|-------------------|
| "Find all log files older than 30 days" | `find /var/log -name "*.log" -mtime +30` |
| "Show me memory usage" | `free -h` |
| "List the 5 largest directories" | `du -h --max-depth=1 \| sort -hr \| head -n 5` |
| "Find all Python files containing 'import pandas'" | `grep -r "import pandas" --include="*.py"` |
| "Compress all PDFs in Documents" | `tar -czf pdfs.tar.gz ~/Documents/*.pdf` |

## 🛡️ Safety Features

The AI Assistant includes multiple safety mechanisms:

### Safety Levels

- 🟢 **SAFE**: Read-only operations, no system changes
- 🟡 **CAUTION**: Requires attention, might modify files
- 🔴 **DANGEROUS**: Could cause data loss or system changes

### Execution Options

When a command is generated, you can:
- **y** - Execute the command
- **n** - Cancel execution
- **c** - Copy to clipboard
- **e** - Edit before executing

### Built-in Protections

- ✅ Timeout protection (5 minutes max)
- ✅ Detailed warnings for risky operations
- ✅ Command explanations before execution
- ✅ Error capture and display

## 💰 Pricing & Cost

### API Costs (as of 2025)

- **Model Used**: Claude Sonnet 4
- **Average Cost**: $0.001-0.003 per command
- **Free Tier**: $5 in credits (≈1,500-5,000 commands)

### Cost Examples

- Generate 100 commands: ~$0.10-0.30
- Daily use (10 commands/day) for a month: ~$0.30-0.90
- Power user (50 commands/day) for a month: ~$1.50-4.50

**Most users stay within the free tier!** 🎉

## 🔧 Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` - Your API key (required)

### Advanced Options

Edit the script to customize:
- Command timeout duration
- Safety level thresholds
- Default execution behavior
- Color scheme

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Ideas for Contributions

- Add support for more shells (fish, PowerShell, etc.)
- Implement command history with SQLite
- Add command templates/favorites
- Create a configuration file system
- Improve error handling
- Add unit tests

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set" Error

Make sure you've exported your API key:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### Command Not Found

Ensure the script is executable:
```bash
chmod +x ai-terminal.py
```

### Python Import Errors

Install dependencies:
```bash
pip install -r requirements.txt
```

### Clipboard Not Working

Install clipboard utilities:
- **Ubuntu/Debian**: `sudo apt install xclip`
- **Fedora**: `sudo dnf install xclip`
- **macOS**: Built-in (pbcopy)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by [Anthropic's Claude AI](https://www.anthropic.com/)
- Inspired by the need to make Linux more accessible
- Built with ❤️ for the open-source community

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-terminal-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-terminal-assistant/discussions)

## ⭐ Show Your Support

If this project helps you, please give it a ⭐ on GitHub!

---

**Made with 🤖 AI and ❤️ by the community**
