import sys
from pathlib import Path
import shutil
import datetime
import subprocess

# --- Agent-Specific Configuration ---
AGENTS = {
    'c': {'name': 'Claude', 'command': 'claude'},
    'g': {'name': 'Gemini', 'command': 'gemini'}
}

# --- Global Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
INSTRUCTIONS_FILE = PROJECT_ROOT / "update_instructions.txt"
SNAPSHOT_SCRIPT = PROJECT_ROOT / "scripts/generate_code_snapshot.py"
ARCHIVE_DIR = PROJECT_ROOT / "docs/PastUpdates"

def run_agent_in_new_window(agent_config):
    """
    Launches the selected agent in a NEW, separate command window,
    which is the only robust way to handle fully interactive CLIs.
    """
    agent_name = agent_config['name']
    agent_command = agent_config['command']

    print(f"  -> Launching {agent_name} in a new window.")
    print(f"  -> Please follow the prompts in the new window.")
    print(f"  -> This script will resume after you close the {agent_name} window.")
    print("-----------------------------------------------------------------")
    
    executable_path = shutil.which(agent_command)
    if not executable_path:
        print(f"\n[FATAL ERROR] Could not find '{agent_command}' in your PATH.")
        return 1

    prompt = f"Carefully read the file '{INSTRUCTIONS_FILE.name}' and execute ALL the actions it describes, in order."
    
    # We must build the command as a single string for this method
    full_command = f'"{executable_path}" "{prompt}"'

    # --- THE DEFINITIVE FIX: CREATE_NEW_CONSOLE ---
    # This tells Windows to spawn the process in its own, fully interactive terminal window.
    # The 'P_WAIT' flag makes our script pause until that new window is closed.
    return_code = os.spawnv(os.P_WAIT, executable_path, [executable_path, prompt])
    
    return return_code

# --- Main script logic ---
def main():
    if len(sys.argv) < 2 or sys.argv[1] not in AGENTS:
        print(f"Usage: {PROJECT_ROOT.name}\\upp.bat [c|g]")
        sys.exit(1)
        
    agent_key = sys.argv[1]
    agent_config = AGENTS[agent_key]
    
    print_header(f"Symposium Knowledge Base Updater ({agent_config['name']})")
    
    if not INSTRUCTIONS_FILE.exists():
        print("[ERROR] 'update_instructions.txt' not found.")
        sys.exit(1)
    print("[PREP] Instructions file found. The update process will now begin.\n")
    
    print_step(1, 3, "EXECUTING INSTRUCTIONS")
    return_code = run_agent_in_new_window(agent_config)
    
    if return_code != 0:
        print("\n\n[FATAL ERROR] AI agent process exited with a non-zero status code.")
        sys.exit(1)
        
    print("\n-----------------------------------------------------------------")
    print("\n  -> Agent task complete.")
    print_step_complete(1, 3)
    
    print_step(2, 3, "GENERATING CODE SNAPSHOT")
    result = subprocess.run([sys.executable, str(SNAPSHOT_SCRIPT)], capture_output=True, text=True, check=True, encoding='utf-8')
    summary_line = result.stdout.strip().split('\n')[-1]
    print(f"  -> {summary_line}")
    print_step_complete(2, 3)
    
    print_step(3, 3, "ARCHIVING LOG FILE")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_filename = f"{timestamp}_update_executed.txt"
    archive_path = ARCHIVE_DIR / archive_filename
    
    print(f"  -> Archiving instructions as: {archive_filename}")
    
    ARCHIVE_DIR.mkdir(exist_ok=True)
    shutil.move(str(INSTRUCTIONS_FILE), str(archive_path))
    print("  -> Instruction file successfully archived.")
    print_step_complete(3, 3)
    
    print_footer("PROJECT KNOWLEDGE BASE IS NOW SYNCED")


def print_header(title):
    print(f"   +{'-' * (len(title) + 4)}+")
    print(f"   |  {title}  |")
    print(f"   +{'-' * (len(title) + 4)}+\n")

def print_footer(title):
    print(f"\n   +{'=' * (len(title) + 4)}+")
    print(f"   |  {title}  |")
    print(f"   +{'=' * (len(title) + 4)}+\n")

def print_step(current, total, title):
    print(f"[STEP {current}/{total}] {title}")
    print("-----------------------------------------------------------------")

def print_step_complete(current, total):
    print(f"[STEP {current}/{total}] COMPLETE\n")

# Need to import os for os.spawnv
import os
if __name__ == "__main__":
    main()