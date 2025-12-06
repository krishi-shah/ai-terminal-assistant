#!/usr/bin/env python3
"""
AI Linux Terminal Assistant - Professional Edition
Works with any OpenAI model on any Linux system

Installation:
1. pip install openai python-dotenv
2. Create .env file with: OPENAI_API_KEY=your-key-here
3. python3 ai-terminal.py

Or run without .env and enter key when prompted
"""

import os
import sys
import json
import subprocess
import getpass

# Check if OpenAI is installed
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: OpenAI library not installed")
    print("Install it with: pip install openai python-dotenv")
    print("Or try: pip3 install --user openai python-dotenv")
    sys.exit(1)

# Try to load .env file (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Simple color codes
class C:
    B = '\033[94m'   # Blue
    G = '\033[92m'   # Green
    Y = '\033[93m'   # Yellow
    R = '\033[91m'   # Red
    C = '\033[96m'   # Cyan
    E = '\033[0m'    # End
    BOLD = '\033[1m'

def print_banner():
    """Welcome message"""
    print(f"\n{C.C}{'='*60}")
    print(f"  AI Linux Terminal Assistant")
    print(f"  Natural Language to Linux Commands")
    print(f"{'='*60}{C.E}\n")

def get_api_key():
    """Get OpenAI API key from .env file, environment, or prompt"""
    key = os.environ.get('OPENAI_API_KEY')
    if key:
        print(f"{C.G}[SUCCESS] API key found{C.E}")
        return key
    
    print(f"{C.Y}[INFO] No API key found{C.E}")
    print(f"{C.C}Get your API key from: https://platform.openai.com/api-keys{C.E}")
    print(f"\n{C.B}TIP: Create a .env file in this directory with:{C.E}")
    print(f"{C.B}     OPENAI_API_KEY=your-key-here{C.E}\n")
    
    try:
        key = getpass.getpass(f"{C.BOLD}Enter your OpenAI API key: {C.E}")
    except:
        key = input(f"{C.BOLD}Enter your OpenAI API key: {C.E}")
    
    return key.strip()

def get_available_model(client):
    """Auto-detect which OpenAI model the user has access to"""
    models_to_try = [
        "gpt-3.5-turbo",
        "gpt-4o-mini",
        "gpt-4",
        "gpt-4-turbo"
    ]
    
    for model in models_to_try:
        try:
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            print(f"{C.G}[SUCCESS] Using model: {model}{C.E}\n")
            return model
        except Exception as e:
            if "does not exist" in str(e) or "model_not_found" in str(e):
                continue
            else:
                print(f"{C.R}[ERROR] {str(e)}{C.E}")
                return None
    
    print(f"{C.R}[ERROR] No accessible models found. Check your API key.{C.E}")
    return None

def generate_command(client, model, user_input):
    """Generate Linux command from natural language"""
    prompt = f"""Convert this request into a Linux command. Respond ONLY with valid JSON, no markdown:

Request: "{user_input}"

{{
  "command": "the bash command",
  "explanation": "what it does (1 sentence)",
  "safety": "safe|caution|danger"
}}

Rules: Use common Linux tools. Make it safe. One line command."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Linux expert. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        text = response.choices[0].message.content.strip()
        text = text.replace('```json', '').replace('```', '').strip()
        
        return json.loads(text)
    
    except json.JSONDecodeError:
        print(f"{C.R}[ERROR] Failed to parse AI response{C.E}")
        print(f"Raw response: {text}")
        return None
    except Exception as e:
        print(f"{C.R}[ERROR] {str(e)}{C.E}")
        return None

def execute_command(cmd):
    """Run the command and show output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.stdout:
            print(f"\n{C.G}[OUTPUT]{C.E}")
            print(result.stdout)
        
        if result.stderr:
            print(f"{C.Y}[WARNING]{C.E}")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"{C.G}[SUCCESS] Command completed{C.E}")
        else:
            print(f"{C.R}[ERROR] Command failed (exit code {result.returncode}){C.E}")
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"{C.R}[ERROR] Command timeout (exceeded 60 seconds){C.E}")
        return False
    except Exception as e:
        print(f"{C.R}[ERROR] {str(e)}{C.E}")
        return False

def get_safety_color(level):
    """Get color for safety level"""
    return {
        'safe': C.G,
        'caution': C.Y,
        'danger': C.R
    }.get(level, C.B)

def process_command(client, model, user_input):
    """Main logic: generate and optionally execute command"""
    print(f"\n{C.C}[INFO] Generating command...{C.E}")
    
    result = generate_command(client, model, user_input)
    
    if not result:
        return
    
    # Display command
    print(f"\n{C.BOLD}Generated Command:{C.E}")
    print(f"  {result['command']}")
    
    print(f"\n{C.B}Explanation:{C.E}")
    print(f"  {result['explanation']}")
    
    # Safety indicator
    safety = result.get('safety', 'caution')
    color = get_safety_color(safety)
    print(f"\n{color}[SAFETY] {safety.upper()}{C.E}")
    
    # Ask to execute
    print(f"\n{C.BOLD}Execute command? [y/n/c=copy/e=edit]: {C.E}", end='')
    choice = input().strip().lower()
    
    if choice == 'y':
        print(f"\n{C.G}[INFO] Executing command...{C.E}")
        execute_command(result['command'])
    
    elif choice == 'c':
        print(f"\n{C.G}Command to copy:{C.E}")
        print(result['command'])
    
    elif choice == 'e':
        print(f"\n{C.BOLD}Enter modified command: {C.E}")
        edited = input().strip()
        if edited:
            print(f"\n{C.G}[INFO] Executing edited command...{C.E}")
            execute_command(edited)
    
    else:
        print(f"{C.Y}[INFO] Execution cancelled{C.E}")

def main():
    """Main program"""
    print_banner()
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        print(f"{C.R}[ERROR] No API key provided{C.E}")
        sys.exit(1)
    
    # Initialize client
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"{C.R}[ERROR] Failed to initialize: {str(e)}{C.E}")
        sys.exit(1)
    
    # Find available model
    print(f"{C.C}[INFO] Checking available models...{C.E}")
    model = get_available_model(client)
    
    if not model:
        print(f"\n{C.R}[ERROR] Cannot find an accessible OpenAI model.{C.E}")
        print(f"{C.Y}[INFO] Make sure your API key is valid and has credits.{C.E}")
        sys.exit(1)
    
    # Check if single command mode
    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
        process_command(client, model, user_input)
        sys.exit(0)
    
    # Interactive mode
    print(f"{C.G}[READY] Type your commands in plain English{C.E}")
    print(f"{C.Y}[INFO] Type 'quit' or press Ctrl+C to exit{C.E}\n")
    
    while True:
        try:
            print(f"{C.BOLD}{C.G}{'─'*60}")
            print(f"What would you like to do? {C.E}", end='')
            user_input = input().strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n{C.C}Session ended{C.E}\n")
                break
            
            process_command(client, model, user_input)
        
        except KeyboardInterrupt:
            print(f"\n\n{C.C}Session ended{C.E}\n")
            break
        except Exception as e:
            print(f"\n{C.R}[ERROR] {str(e)}{C.E}\n")

if __name__ == "__main__":
    main()
