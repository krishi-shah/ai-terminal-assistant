#!/usr/bin/env python3
"""
AI Terminal Assistant - Direct CLI Integration
Run natural language commands directly in your terminal

Installation:
1. Save this file as 'ai-terminal.py'
2. Install required packages: pip install anthropic openai
3. Set your API key (either one):
   export ANTHROPIC_API_KEY='your-claude-key'
   OR
   export OPENAI_API_KEY='your-openai-key'
4. Make executable: chmod +x ai-terminal.py
5. Run: ./ai-terminal.py

Usage:
- Interactive mode: ./ai-terminal.py
- Direct command: ./ai-terminal.py "find all large files"
- Auto-execute: ./ai-terminal.py --auto "list processes"
"""

import os
import sys
import json
import subprocess
import shutil
import platform

# Try importing both APIs
ANTHROPIC_AVAILABLE = False
OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    pass

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Package manager mappings for different distros
PACKAGE_MANAGERS = {
    'apt': {
        'check': 'dpkg -l',
        'install': 'sudo apt install -y',
        'distros': ['ubuntu', 'debian', 'mint', 'pop']
    },
    'dnf': {
        'check': 'rpm -qa',
        'install': 'sudo dnf install -y',
        'distros': ['fedora', 'rhel', 'centos']
    },
    'yum': {
        'check': 'rpm -qa',
        'install': 'sudo yum install -y',
        'distros': ['centos', 'rhel']
    },
    'pacman': {
        'check': 'pacman -Q',
        'install': 'sudo pacman -S --noconfirm',
        'distros': ['arch', 'manjaro']
    },
    'brew': {
        'check': 'brew list',
        'install': 'brew install',
        'distros': ['darwin']  # macOS
    },
    'zypper': {
        'check': 'rpm -qa',
        'install': 'sudo zypper install -y',
        'distros': ['opensuse', 'suse']
    }
}

# Common tool to package mappings
TOOL_PACKAGES = {
    'ffmpeg': 'ffmpeg',
    'convert': 'imagemagick',
    'git': 'git',
    'curl': 'curl',
    'wget': 'wget',
    'jq': 'jq',
    'tar': 'tar',
    'zip': 'zip',
    'unzip': 'unzip',
    'rsync': 'rsync',
    'htop': 'htop',
    'tree': 'tree',
    'xclip': 'xclip',
    'pbcopy': 'pbcopy',
    'docker': 'docker',
    'python3': 'python3',
    'pip': 'python3-pip',
    'node': 'nodejs',
    'npm': 'npm',
    'code': 'code',
    'vim': 'vim',
    'emacs': 'emacs',
    'nano': 'nano',
    'pandoc': 'pandoc',
    'youtube-dl': 'youtube-dl',
    'yt-dlp': 'yt-dlp',
    'neofetch': 'neofetch'
}

def print_colored(text, color, end='\n'):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.END}", end=end)

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║        AI Linux Terminal Assistant - CLI Mode         ║
    ║    Speak naturally, execute commands automatically    ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN)

def detect_os():
    """Detect the operating system and return OS info"""
    system = platform.system().lower()
    
    if system == 'darwin':
        return 'darwin', 'macOS'
    elif system == 'linux':
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                for distro in ['ubuntu', 'debian', 'fedora', 'arch', 'manjaro', 'centos', 'rhel', 'opensuse', 'mint', 'pop']:
                    if distro in os_info:
                        return distro, distro.capitalize()
        except:
            pass
        return 'linux', 'Linux'
    else:
        return system, system.capitalize()

def get_package_manager():
    """Detect and return the appropriate package manager"""
    os_type, os_name = detect_os()
    
    if os_type == 'darwin':
        if shutil.which('brew'):
            return 'brew'
        return None
    
    for pm, info in PACKAGE_MANAGERS.items():
        if os_type in info['distros']:
            if pm == 'apt' and shutil.which('apt'):
                return 'apt'
            elif pm == 'dnf' and shutil.which('dnf'):
                return 'dnf'
            elif pm == 'yum' and shutil.which('yum'):
                return 'yum'
            elif pm == 'pacman' and shutil.which('pacman'):
                return 'pacman'
            elif pm == 'zypper' and shutil.which('zypper'):
                return 'zypper'
    
    return None

def extract_tools_from_command(command):
    """Extract tool names from a command"""
    tools = []
    parts = command.replace('|', ' ').replace('&&', ' ').replace(';', ' ').replace('||', ' ').split()
    
    for part in parts:
        clean_part = part.strip().replace('sudo', '').strip()
        if clean_part.startswith('-'):
            continue
        if '/' in clean_part:
            clean_part = clean_part.split('/')[-1]
        
        if clean_part in TOOL_PACKAGES:
            tools.append(clean_part)
    
    return list(set(tools))

def check_tool_installed(tool):
    """Check if a tool is installed"""
    return shutil.which(tool) is not None

def get_install_command(tool, package_manager):
    """Get the installation command for a tool"""
    if not package_manager or package_manager not in PACKAGE_MANAGERS:
        return None
    
    package_name = TOOL_PACKAGES.get(tool, tool)
    install_cmd = PACKAGE_MANAGERS[package_manager]['install']
    
    return f"{install_cmd} {package_name}"

def check_missing_tools(command):
    """Check for missing tools and return installation suggestions"""
    tools = extract_tools_from_command(command)
    missing_tools = []
    
    for tool in tools:
        if not check_tool_installed(tool):
            missing_tools.append(tool)
    
    return missing_tools

def generate_command_anthropic(client, user_input):
    """Generate command using Anthropic Claude API"""
    prompt = f"""You are a Linux command expert. Convert the following natural language request into a safe, executable Linux command.

User request: "{user_input}"

Provide your response in the following JSON format only, with no additional text or markdown:
{{
  "command": "the actual Linux command",
  "explanation": "brief explanation of what the command does",
  "safety_level": "safe|caution|dangerous",
  "warnings": ["list any potential risks or important notes"]
}}

Rules:
- Generate only safe, non-destructive commands when possible
- For potentially destructive operations, add confirmation flags or suggest safer alternatives
- Include proper error handling where appropriate
- Use standard Linux utilities available on most systems
- Mark commands as "dangerous" if they could cause data loss or system changes
- Mark as "caution" if they require careful use
- Mark as "safe" for read-only or low-risk operations
- Ensure commands are compatible with bash/zsh shells"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text.strip()
    response_text = response_text.replace('```json', '').replace('```', '').strip()
    
    return json.loads(response_text)

def generate_command_openai(client, user_input):
    """Generate command using OpenAI GPT API"""
    prompt = f"""You are a Linux command expert. Convert the following natural language request into a safe, executable Linux command.

User request: "{user_input}"

Provide your response in the following JSON format only, with no additional text or markdown:
{{
  "command": "the actual Linux command",
  "explanation": "brief explanation of what the command does",
  "safety_level": "safe|caution|dangerous",
  "warnings": ["list any potential risks or important notes"]
}}

Rules:
- Generate only safe, non-destructive commands when possible
- For potentially destructive operations, add confirmation flags or suggest safer alternatives
- Include proper error handling where appropriate
- Use standard Linux utilities available on most systems
- Mark commands as "dangerous" if they could cause data loss or system changes
- Mark as "caution" if they require careful use
- Mark as "safe" for read-only or low-risk operations
- Ensure commands are compatible with bash/zsh shells"""

    response = client.chat.completions.create(
        model="gpt-4",  # You can also use "gpt-3.5-turbo" for cheaper option
        messages=[
            {"role": "system", "content": "You are a Linux command expert. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    
    response_text = response.choices[0].message.content.strip()
    response_text = response_text.replace('```json', '').replace('```', '').strip()
    
    return json.loads(response_text)

def suggest_alternatives(client, ai_provider, original_command, missing_tool):
    """Ask AI for alternative commands that don't require the missing tool"""
    try:
        prompt = f"""A user wants to run this command but the tool '{missing_tool}' is not installed:

Command: {original_command}

Please suggest an alternative command that achieves the same goal using commonly available tools (like find, grep, awk, sed, cat, etc.) that are typically pre-installed on most Linux systems.

Respond in JSON format:
{{
  "alternative_command": "the alternative command",
  "explanation": "brief explanation of the alternative"
}}"""

        if ai_provider == 'anthropic':
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = message.content[0].text.strip()
        else:  # openai
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Linux expert. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            response_text = response.choices[0].message.content.strip()
        
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        return json.loads(response_text)
    except:
        return None

def generate_command(client, ai_provider, user_input):
    """Generate Linux command from natural language using available AI API"""
    try:
        if ai_provider == 'anthropic':
            return generate_command_anthropic(client, user_input)
        else:  # openai
            return generate_command_openai(client, user_input)
    except Exception as e:
        print_colored(f"Error generating command: {str(e)}", Colors.RED)
        return None

def execute_command(command):
    """Execute the generated command in the shell"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.stdout:
            print_colored("\n Output:", Colors.GREEN)
            print(result.stdout)
        
        if result.stderr:
            print_colored("\n  Errors/Warnings:", Colors.YELLOW)
            print(result.stderr)
        
        if result.returncode == 0:
            print_colored("\n Command completed successfully", Colors.GREEN)
        else:
            print_colored(f"\n Command failed with exit code {result.returncode}", Colors.RED)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print_colored("\n  Command timed out (exceeded 5 minutes)", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"\n Execution error: {str(e)}", Colors.RED)
        return False

def get_safety_color(level):
    """Get color for safety level"""
    return {
        'safe': Colors.GREEN,
        'caution': Colors.YELLOW,
        'dangerous': Colors.RED
    }.get(level, Colors.BLUE)

def process_request(client, ai_provider, user_input, auto_execute=False):
    """Process a user request and optionally execute it"""
    print_colored(f"\n Processing: {user_input}", Colors.BLUE)
    print_colored(" Generating command...\n", Colors.CYAN)
    
    result = generate_command(client, ai_provider, user_input)
    
    if not result:
        return False
    
    print_colored("╔═══ Generated Command ═══╗", Colors.CYAN)
    print_colored(f"  {result['command']}", Colors.BOLD)
    print_colored("╚═════════════════════════╝\n", Colors.CYAN)
    
    # Check for missing tools
    missing_tools = check_missing_tools(result['command'])
    package_manager = get_package_manager()
    
    if missing_tools:
        print_colored("  Missing Tools Detected!", Colors.YELLOW)
        print_colored("─" * 60, Colors.YELLOW)
        
        for tool in missing_tools:
            print_colored(f"\n Tool '{tool}' is not installed", Colors.RED)
            
            if package_manager:
                install_cmd = get_install_command(tool, package_manager)
                print_colored(f"   Install with: {install_cmd}", Colors.GREEN)
            else:
                print_colored(f"   Please install '{tool}' manually", Colors.YELLOW)
        
        print()
        print_colored("Options:", Colors.CYAN)
        print_colored("  [i] Install missing tools automatically", Colors.BLUE)
        print_colored("  [a] Suggest alternative command (without these tools)", Colors.BLUE)
        print_colored("  [c] Continue anyway (command may fail)", Colors.BLUE)
        print_colored("  [n] Cancel", Colors.BLUE)
        
        print_colored("\nYour choice [i/a/c/N]: ", Colors.BOLD, end='')
        choice = input().strip().lower()
        
        if choice == 'i' and package_manager:
            print_colored("\n Installing missing tools...\n", Colors.GREEN)
            for tool in missing_tools:
                install_cmd = get_install_command(tool, package_manager)
                print_colored(f"Running: {install_cmd}", Colors.CYAN)
                os.system(install_cmd)
            print_colored("\n Installation complete!\n", Colors.GREEN)
        
        elif choice == 'a':
            print_colored("\n Finding alternative command...\n", Colors.CYAN)
            alternative = suggest_alternatives(client, ai_provider, result['command'], missing_tools[0])
            if alternative:
                print_colored("╔═══ Alternative Command ═══╗", Colors.CYAN)
                print_colored(f"  {alternative['alternative_command']}", Colors.BOLD)
                print_colored("╚═══════════════════════════╝\n", Colors.CYAN)
                print_colored(f" {alternative['explanation']}\n", Colors.BLUE)
                
                print_colored("Use this alternative? [y/N]: ", Colors.BOLD, end='')
                if input().strip().lower() == 'y':
                    result['command'] = alternative['alternative_command']
                else:
                    print_colored(" Cancelled", Colors.YELLOW)
                    return False
            else:
                print_colored(" Could not find alternative command", Colors.RED)
                return False
        
        elif choice == 'c':
            print_colored("  Continuing anyway (command may fail)...\n", Colors.YELLOW)
        
        else:
            print_colored(" Cancelled", Colors.YELLOW)
            return False
    
    print_colored(" Explanation:", Colors.BLUE)
    print(f"  {result['explanation']}\n")
    
    safety_symbol = {
        'safe': '✅',
        'caution': '⚠️',
        'dangerous': '🚨'
    }.get(result['safety_level'], '❓')
    
    safety_color = get_safety_color(result['safety_level'])
    print_colored(f"{safety_symbol} Safety Level: {result['safety_level'].upper()}", safety_color)
    
    if result.get('warnings'):
        print_colored("\n  Important Warnings:", Colors.YELLOW)
        for warning in result['warnings']:
            print(f"  • {warning}")
    
    print()
    
    if auto_execute and result['safety_level'] == 'safe':
        print_colored(" Auto-executing (safe command)...\n", Colors.GREEN)
        execute_command(result['command'])
    else:
        print_colored("Execute this command? [y/N/c(copy)/e(edit)]: ", Colors.BOLD, end='')
        choice = input().strip().lower()
        
        if choice == 'y':
            print_colored("\n Executing...\n", Colors.GREEN)
            execute_command(result['command'])
        elif choice == 'c':
            try:
                if os.system('which xclip > /dev/null 2>&1') == 0:
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                 input=result['command'].encode(), check=True)
                    print_colored(" Command copied to clipboard!", Colors.GREEN)
                elif os.system('which pbcopy > /dev/null 2>&1') == 0:
                    subprocess.run(['pbcopy'], input=result['command'].encode(), check=True)
                    print_colored(" Command copied to clipboard!", Colors.GREEN)
                else:
                    print_colored(" Clipboard utility not found. Command:", Colors.YELLOW)
                    print(result['command'])
            except Exception as e:
                print_colored(f" Could not copy to clipboard: {e}", Colors.YELLOW)
                print(f"Command: {result['command']}")
        elif choice == 'e':
            print_colored("Enter modified command: ", Colors.BOLD, end='')
            edited_command = input().strip()
            if edited_command:
                print_colored("\n Executing edited command...\n", Colors.GREEN)
                execute_command(edited_command)
        else:
            print_colored(" Execution cancelled", Colors.YELLOW)
    
    return True

def interactive_mode(client, ai_provider):
    """Run in interactive mode"""
    print_banner()
    
    os_type, os_name = detect_os()
    package_manager = get_package_manager()
    
    # Display AI provider
    ai_name = "Claude (Anthropic)" if ai_provider == 'anthropic' else "GPT-4 (OpenAI)"
    print_colored(f" AI Provider: {ai_name}", Colors.CYAN)
    print_colored(f"  Detected OS: {os_name}", Colors.CYAN)
    if package_manager:
        print_colored(f" Package Manager: {package_manager}", Colors.CYAN)
    else:
        print_colored("  No package manager detected", Colors.YELLOW)
    
    print_colored("\n Type your commands in plain English (or 'quit' to exit)", Colors.CYAN)
    print_colored(" Press Ctrl+C to cancel at any time\n", Colors.CYAN)
    
    while True:
        try:
            print_colored("─" * 60, Colors.BLUE)
            user_input = input(f"{Colors.BOLD}{Colors.GREEN}➜ What would you like to do? {Colors.END}").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print_colored("\n Goodbye!", Colors.CYAN)
                break
            
            process_request(client, ai_provider, user_input)
            
        except KeyboardInterrupt:
            print_colored("\n\n Goodbye!", Colors.CYAN)
            break
        except Exception as e:
            print_colored(f"\n Error: {str(e)}", Colors.RED)

def main():
    """Main entry point"""
    # Check for API keys and determine which provider to use
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')
    
    client = None
    ai_provider = None
    
    # Prioritize Anthropic if both are available
    if anthropic_key and ANTHROPIC_AVAILABLE:
        client = Anthropic(api_key=anthropic_key)
        ai_provider = 'anthropic'
    elif openai_key and OPENAI_AVAILABLE:
        client = OpenAI(api_key=openai_key)
        ai_provider = 'openai'
    else:
        # No valid API key found
        print_colored(" Error: No API key found", Colors.RED)
        print_colored("\nPlease set one of the following:", Colors.YELLOW)
        
        if not anthropic_key:
            print_colored("  export ANTHROPIC_API_KEY='your-claude-key'", Colors.CYAN)
            print_colored("  Get it from: https://console.anthropic.com/", Colors.BLUE)
        
        if not openai_key:
            print_colored("  export OPENAI_API_KEY='your-openai-key'", Colors.CYAN)
            print_colored("  Get it from: https://platform.openai.com/api-keys", Colors.BLUE)
        
        # Check if libraries are missing
        if not ANTHROPIC_AVAILABLE and not OPENAI_AVAILABLE:
            print_colored("\n  Missing required libraries!", Colors.RED)
            print_colored("Install with: pip install anthropic openai", Colors.YELLOW)
        elif not ANTHROPIC_AVAILABLE:
            print_colored("\n Install Anthropic library: pip install anthropic", Colors.YELLOW)
        elif not OPENAI_AVAILABLE:
            print_colored("\n Install OpenAI library: pip install openai", Colors.YELLOW)
        
        sys.exit(1)
    
    # Parse command line arguments
    auto_execute = '--auto' in sys.argv
    if auto_execute:
        sys.argv.remove('--auto')
    
    # Check if command provided as argument
    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
        process_request(client, ai_provider, user_input, auto_execute)
    else:
        interactive_mode(client, ai_provider)

if __name__ == "__main__":
    main()
