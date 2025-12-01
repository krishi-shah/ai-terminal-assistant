# 📚 AI Terminal Assistant - Example Commands

This document contains real-world examples of what you can do with the AI Terminal Assistant.

## 🗂️ File Management

### Find Files

**Natural Language:**
> "Find all PDF files in my Documents folder"

**Generated Command:**
```bash
find ~/Documents -type f -name "*.pdf"
```

---

**Natural Language:**
> "Find all files larger than 100MB modified in the last week"

**Generated Command:**
```bash
find ~ -type f -size +100M -mtime -7
```

### Organize Files

**Natural Language:**
> "Move all images from Downloads to Pictures folder"

**Generated Command:**
```bash
find ~/Downloads -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.jpeg" \) -exec mv {} ~/Pictures/ \;
```

---

**Natural Language:**
> "Create a backup of all my config files"

**Generated Command:**
```bash
tar -czf ~/backup-configs-$(date +%Y%m%d).tar.gz ~/.bashrc ~/.zshrc ~/.vimrc ~/.gitconfig
```

## 📊 System Information

**Natural Language:**
> "Show me the top 10 processes using the most memory"

**Generated Command:**
```bash
ps aux --sort=-%mem | head -n 11
```

---

**Natural Language:**
> "What's my current disk usage?"

**Generated Command:**
```bash
df -h
```

---

**Natural Language:**
> "Show me the 5 largest directories in my home folder"

**Generated Command:**
```bash
du -h ~/ --max-depth=1 | sort -hr | head -n 6
```

## 🔍 Text Search

**Natural Language:**
> "Find all Python files that import pandas"

**Generated Command:**
```bash
grep -r "import pandas" --include="*.py"
```

---

**Natural Language:**
> "Search for the word 'TODO' in all JavaScript files"

**Generated Command:**
```bash
grep -rn "TODO" --include="*.js"
```

## 📦 Compression & Archives

**Natural Language:**
> "Compress all video files larger than 500MB"

**Generated Command:**
```bash
find . -type f \( -iname "*.mp4" -o -iname "*.avi" -o -iname "*.mkv" \) -size +500M -print0 | tar -czf large-videos.tar.gz --null -T -
```

---

**Natural Language:**
> "Extract all zip files in the current directory"

**Generated Command:**
```bash
for file in *.zip; do unzip "$file" -d "${file%.zip}"; done
```

## 🌐 Network Operations

**Natural Language:**
> "Check if google.com is reachable"

**Generated Command:**
```bash
ping -c 4 google.com
```

---

**Natural Language:**
> "Download this file from a URL"

**Generated Command:**
```bash
wget [URL]
```

## 🗑️ Cleanup Operations

**Natural Language:**
> "Delete all log files older than 30 days"

**Generated Command:**
```bash
find /var/log -name "*.log" -type f -mtime +30 -delete
```

---

**Natural Language:**
> "Remove all empty directories in the current folder"

**Generated Command:**
```bash
find . -type d -empty -delete
```

## 📝 Log Analysis

**Natural Language:**
> "Show me the last 50 lines of the system log"

**Generated Command:**
```bash
tail -n 50 /var/log/syslog
```

---

**Natural Language:**
> "Count how many errors are in the application log"

**Generated Command:**
```bash
grep -c "ERROR" /var/log/application.log
```

## 🔐 Permissions & Ownership

**Natural Language:**
> "Make all shell scripts in this directory executable"

**Generated Command:**
```bash
find . -name "*.sh" -type f -exec chmod +x {} \;
```

---

**Natural Language:**
> "Change ownership of all files in /var/www to www-data"

**Generated Command:**
```bash
sudo chown -R www-data:www-data /var/www
```

## 🎨 Image/Video Processing

**Natural Language:**
> "Convert all PNG images to JPEG"

**Generated Command:**
```bash
for img in *.png; do convert "$img" "${img%.png}.jpg"; done
```

---

**Natural Language:**
> "Reduce video file size using ffmpeg"

**Generated Command:**
```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
```

## 📊 Data Processing

**Natural Language:**
> "Count the number of lines in all CSV files"

**Generated Command:**
```bash
wc -l *.csv
```

---

**Natural Language:**
> "Extract the first column from a CSV file"

**Generated Command:**
```bash
cut -d',' -f1 data.csv
```

## 🔄 Batch Operations

**Natural Language:**
> "Rename all .txt files to .md"

**Generated Command:**
```bash
for file in *.txt; do mv "$file" "${file%.txt}.md"; done
```

---

**Natural Language:**
> "Copy all configuration files to a backup folder"

**Generated Command:**
```bash
mkdir -p ~/config-backup && cp ~/.{bashrc,vimrc,zshrc,gitconfig} ~/config-backup/
```

## 💡 Pro Tips

1. **Be specific**: The more details you provide, the better the command
2. **Mention file types**: Specify extensions like .pdf, .jpg, .log
3. **Include locations**: Mention folders like "in my Documents" or "in /var/log"
4. **State the action**: Use verbs like find, move, delete, compress, list
5. **Add constraints**: Mention size, date, or other filters

## 🚨 Safety Reminders

- Always review generated commands before executing
- Commands marked as DANGEROUS require extra caution
- Use the 'c' option to copy and review complex commands
- Test on sample data first for destructive operations
- Keep backups of important data

---

**Want to add your own examples?** Submit a PR to this file!