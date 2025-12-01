#!/usr/bin/env python3
"""
AI Terminal Assistant - Direct CLI Integration
Run natural language commands directly in your terminal

Installation:
1. Save this file as 'ai-terminal.py'
2. Install required package: pip install anthropic
3. Set your API key: export ANTHROPIC_API_KEY='your-api-key'
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
from anthropic import Anthropic

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

def generate_command(client, user_input):
    """Generate Linux command from natural language using Claude API"""
    try:
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
        
        # Extract and parse response
        response_text = message.content[0].text.strip()
        # Remove markdown code blocks if present
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        return json.loads(response_text)
    
    except Exception as e:
        print_colored(f"Error generating command: {str(e)}", Colors.RED)
        return None

def execute_command(command):
    """Execute the generated command in the shell"""
    try:
        # Execute command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Display output
        if result.stdout:
            print_colored("\n📤 Output:", Colors.GREEN)
            print(result.stdout)
        
        if result.stderr:
            print_colored("\n⚠️  Errors/Warnings:", Colors.YELLOW)
            print(result.stderr)
        
        if result.returncode == 0:
            print_colored("\n✅ Command completed successfully", Colors.GREEN)
        else:
            print_colored(f"\n❌ Command failed with exit code {result.returncode}", Colors.RED)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print_colored("\n⏱️  Command timed out (exceeded 5 minutes)", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"\n❌ Execution error: {str(e)}", Colors.RED)
        return False

def get_safety_color(level):
    """Get color for safety level"""
    return {
        'safe': Colors.GREEN,
        'caution': Colors.YELLOW,
        'dangerous': Colors.RED
    }.get(level, Colors.BLUE)

def process_request(client, user_input, auto_execute=False):
    """Process a user request and optionally execute it"""
    print_colored(f"\n🤖 Processing: {user_input}", Colors.BLUE)
    print_colored("⏳ Generating command...\n", Colors.CYAN)
    
    # Generate command
    result = generate_command(client, user_input)
    
    if not result:
        return False
    
    # Display generated command
    print_colored("╔═══ Generated Command ═══╗", Colors.CYAN)
    print_colored(f"  {result['command']}", Colors.BOLD)
    print_colored("╚═════════════════════════╝\n", Colors.CYAN)
    
    # Display explanation
    print_colored("📝 Explanation:", Colors.BLUE)
    print(f"  {result['explanation']}\n")
    
    # Display safety level
    safety_symbol = {
        'safe': '✅',
        'caution': '⚠️',
        'dangerous': '🚨'
    }.get(result['safety_level'], '❓')
    
    safety_color = get_safety_color(result['safety_level'])
    print_colored(f"{safety_symbol} Safety Level: {result['safety_level'].upper()}", safety_color)
    
    # Display warnings if any
    if result.get('warnings'):
        print_colored("\n⚠️  Important Warnings:", Colors.YELLOW)
        for warning in result['warnings']:
            print(f"  • {warning}")
    
    print()  # Empty line
    
    # Execute or ask for confirmation
    if auto_execute and result['safety_level'] == 'safe':
        print_colored("🚀 Auto-executing (safe command)...\n", Colors.GREEN)
        execute_command(result['command'])
    else:
        # Ask for confirmation
        print_colored("Execute this command? [y/N/c(copy)/e(edit)]: ", Colors.BOLD, end='')
        choice = input().strip().lower()
        
        if choice == 'y':
            print_colored("\n🚀 Executing...\n", Colors.GREEN)
            execute_command(result['command'])
        elif choice == 'c':
            # Copy to clipboard (works on most Linux systems)
            try:
                if os.system('which xclip > /dev/null 2>&1') == 0:
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                 input=result['command'].encode(), check=True)
                    print_colored("✅ Command copied to clipboard!", Colors.GREEN)
                elif os.system('which pbcopy > /dev/null 2>&1') == 0:  # macOS
                    subprocess.run(['pbcopy'], input=result['command'].encode(), check=True)
                    print_colored("✅ Command copied to clipboard!", Colors.GREEN)
                else:
                    print_colored("⚠️  Clipboard utility not found. Command:", Colors.YELLOW)
                    print(result['command'])
            except Exception as e:
                print_colored(f"⚠️  Could not copy to clipboard: {e}", Colors.YELLOW)
                print(f"Command: {result['command']}")
        elif choice == 'e':
            print_colored("Enter modified command: ", Colors.BOLD, end='')
            edited_command = input().strip()
            if edited_command:
                print_colored("\n🚀 Executing edited command...\n", Colors.GREEN)
                execute_command(edited_command)
        else:
            print_colored("❌ Execution cancelled", Colors.YELLOW)
    
    return True

def interactive_mode(client):
    """Run in interactive mode"""
    print_banner()
    print_colored("💡 Type your commands in plain English (or 'quit' to exit)", Colors.CYAN)
    print_colored("💡 Press Ctrl+C to cancel at any time\n", Colors.CYAN)
    
    while True:
        try:
            print_colored("─" * 60, Colors.BLUE)
            user_input = input(f"{Colors.BOLD}{Colors.GREEN}➜ What would you like to do? {Colors.END}").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print_colored("\n👋 Goodbye!", Colors.CYAN)
                break
            
            process_request(client, user_input)
            
        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye!", Colors.CYAN)
            break
        except Exception as e:
            print_colored(f"\n❌ Error: {str(e)}", Colors.RED)

def main():
    """Main entry point"""
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print_colored("❌ Error: ANTHROPIC_API_KEY environment variable not set", Colors.RED)
        print_colored("\nSet it with: export ANTHROPIC_API_KEY='your-api-key'", Colors.YELLOW)
        print_colored("Get your API key from: https://console.anthropic.com/", Colors.CYAN)
        sys.exit(1)
    
    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)
    
    # Parse command line arguments
    auto_execute = '--auto' in sys.argv
    if auto_execute:
        sys.argv.remove('--auto')
    
    # Check if command provided as argument
    if len(sys.argv) > 1:
        # Direct command mode
        user_input = ' '.join(sys.argv[1:])
        process_request(client, user_input, auto_execute)
    else:
        # Interactive mode
        interactive_mode(client)

if __name__ == "__main__":
    main()
