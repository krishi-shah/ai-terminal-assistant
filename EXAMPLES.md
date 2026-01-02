# AI Terminal Assistant - Example Commands

This document contains real-world examples of what you can do with the AI Terminal Assistant.

**Note:** These examples are optimized for Linux systems. The tool automatically adapts to your shell (bash, zsh, fish, etc.) and operating system.

## File Management

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

## System Information

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

## Text Search

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

## Compression & Archives

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

## Network Operations

**Natural Language:**
> "Check if google.com is reachable"

**Generated Command:**
```bash
ping -c 4 google.com
```

---

**Natural Language:**
> "Show which process is using port 8080"

**Generated Command:**
```bash
sudo lsof -i :8080
```

---

**Natural Language:**
> "List all open network connections"

**Generated Command:**
```bash
ss -tuln
```

---

**Natural Language:**
> "Show my public IP address"

**Generated Command:**
```bash
curl -s ifconfig.me
```

---

**Natural Language:**
> "Download this file from a URL"

**Generated Command:**
```bash
wget [URL]
```

---

**Natural Language:**
> "Check DNS records for a domain"

**Generated Command:**
```bash
dig example.com
```

## Cleanup Operations

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

## Log Analysis

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

## Permissions & Ownership

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

## Image/Video Processing

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

## Data Processing

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

## Batch Operations

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

## Linux Package Management

**Natural Language (Ubuntu/Debian):**
> "List all installed packages with python in the name"

**Generated Command:**
```bash
dpkg -l | grep python
```

---

**Natural Language (Fedora/RHEL):**
> "Check for available system updates"

**Generated Command:**
```bash
sudo dnf check-update
```

---

**Natural Language:**
> "Find which package provides the netstat command"

**Generated Command:**
```bash
# Ubuntu/Debian
apt-file search bin/netstat

# Fedora/RHEL
dnf provides netstat
```

## Linux System Administration

**Natural Language:**
> "Show logged in users and their activity"

**Generated Command:**
```bash
w
```

---

**Natural Language:**
> "List all systemd services that failed"

**Generated Command:**
```bash
systemctl --failed
```

---

**Natural Language:**
> "Check the status of the nginx service"

**Generated Command:**
```bash
systemctl status nginx
```

---

**Natural Language:**
> "Show system boot time and uptime"

**Generated Command:**
```bash
uptime -s && uptime
```

---

**Natural Language:**
> "Display kernel version and system information"

**Generated Command:**
```bash
uname -a
```

---

**Natural Language:**
> "Show memory usage in human readable format"

**Generated Command:**
```bash
free -h
```

## Linux File System

**Natural Language:**
> "Find broken symbolic links in current directory"

**Generated Command:**
```bash
find . -xtype l
```

---

**Natural Language:**
> "Show inode usage for all mounted filesystems"

**Generated Command:**
```bash
df -i
```

---

**Natural Language:**
> "List files opened by a specific process"

**Generated Command:**
```bash
lsof -p [PID]
```

---

**Natural Language:**
> "Find files with setuid bit set"

**Generated Command:**
```bash
find / -perm -4000 -type f 2>/dev/null
```

## Linux Performance Monitoring

**Natural Language:**
> "Monitor CPU usage in real time"

**Generated Command:**
```bash
top -o %CPU
```

---

**Natural Language:**
> "Show I/O statistics for all disks"

**Generated Command:**
```bash
iostat -x 1
```

---

**Natural Language:**
> "List processes sorted by memory usage"

**Generated Command:**
```bash
ps aux --sort=-%mem | head -20
```

---

**Natural Language:**
> "Show network bandwidth usage by process"

**Generated Command:**
```bash
sudo nethogs
```

## Shell-Specific Features

### Bash/Zsh Tips

The assistant understands shell-specific features:

**Natural Language:**
> "Create a timestamped backup of a directory"

**Generated Command:**
```bash
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz /path/to/directory
```

---

**Natural Language:**
> "Process all files in parallel using 4 cores"

**Generated Command:**
```bash
find . -name "*.txt" | xargs -P 4 -I {} process_command {}
```

## Pro Tips

1. **Be specific**: The more details you provide, the better the command
2. **Mention file types**: Specify extensions like .pdf, .jpg, .log
3. **Include locations**: Mention folders like "in my Documents" or "in /var/log"
4. **State the action**: Use verbs like find, move, delete, compress, list
5. **Add constraints**: Mention size, date, or other filters
6. **Linux-specific**: Mention package managers (apt, dnf, pacman) or system tools (systemctl, journalctl)
7. **Shell awareness**: The tool detects your shell (bash/zsh/fish) and adapts commands

## Safety Reminders

- Always review generated commands before executing
- Commands marked as DANGEROUS require extra caution
- Use the 'c' option to copy and review complex commands
- Test on sample data first for destructive operations
- Keep backups of important data
- Be especially careful with `sudo`, `rm -rf`, and other destructive operations
- The tool will warn you about dangerous commands with a safety indicator

## Linux-Specific Safety

- Commands requiring `sudo` will be marked appropriately
- File deletion commands are marked as high-risk
- System modification commands include warnings
- Always verify paths before running destructive operations on Linux systems

---

**Want to add your own examples?** Submit a PR to this file!
