import subprocess
import json
import time
import sys
import re
from pathlib import Path
import shutil
import datetime

# --- Configuration is the same ---
PROJECT_ROOT = Path(__file__).parent.parent
SCLAUDE_PATH = PROJECT_ROOT / "scripts" / "sclaude.bat"
INSTRUCTIONS_FILE = PROJECT_ROOT / "update_instructions.txt"
SNAPSHOT_SCRIPT = PROJECT_ROOT / "scripts" / "generate_code_snapshot.py"
ARCHIVE_DIR = PROJECT_ROOT / "docs" / "PastUpdates"

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    if total == 0: total = 1
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def run_claude_and_show_progress():
    print("  -> Tasking Claude Code for automated execution...")
    print("  -> All verbose output is being processed in the background.")

    cmd = [
        str(SCLAUDE_PATH),
        "Carefully read the file 'update_instructions.txt' and execute ALL the actions it describes, in order, ensuring the final state matches the requirements."
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='ignore',
        # ** THE DEFINITIVE FIX IS HERE: Force line-buffering **
        bufsize=1
    )

    total_steps = 1
    current_step = 0
    print_progress_bar(0, total_steps, prefix="Progress:", suffix="Initializing...")

    # The character-by-character parser is still correct, it just wasn't getting any data.
    buffer = ""
    while True:
        char = process.stdout.read(1)
        if not char:
            break
        
        buffer += char
        
        if char == '}':
            try:
                data = json.loads(buffer)
                text_content = ""
                if (message := data.get("message")) and \
                   (content := message.get("content")) and \
                   isinstance(content, list) and len(content) > 0 and \
                   (text_content := content[0].get("text")):

                    match = re.search(r"Starting action (\d+) of (\d+)", text_content, re.IGNORECASE)
                    if match:
                        current_step = int(match.group(1))
                        total_steps = int(match.group(2))
                        print_progress_bar(current_step - 1, total_steps, prefix="Progress:", suffix=f"Starting Step {current_step}...")
                        sys.stdout.write(f"\n  -> {text_content.strip()}\n")
                        sys.stdout.flush()
                    
                    elif "completed action" in text_content.lower():
                        print_progress_bar(current_step, total_steps, prefix="Progress:", suffix="Done.")
                        sys.stdout.write(f"\n  -> {text_content.strip()}\n")
                        sys.stdout.flush()

                buffer = ""

            except json.JSONDecodeError:
                continue

    process.wait()
    print_progress_bar(total_steps, total_steps, prefix="Progress:", suffix="Complete.")
    return process.returncode

# The rest of the script remains identical.
def main():
    print_header("Symposium Knowledge Base Update Orchestrator")
    if not INSTRUCTIONS_FILE.exists():
        print("[ERROR] 'update_instructions.txt' not found.")
        sys.exit(1)
    print("[PREP] Instructions file found. The update process will now begin.\n")
    print_step(1, 3, "EXECUTING INSTRUCTIONS")
    return_code = run_claude_and_show_progress()
    if return_code != 0:
        print("\n\n[FATAL ERROR] AI agent reported an error during execution.")
        sys.exit(1)
    print("\n\n  -> Claude Code task complete.")
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

if __name__ == "__main__":
    main()