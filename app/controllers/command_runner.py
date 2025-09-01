import subprocess
import shlex

# A simple whitelist of allowed commands for security
# This is a critical security feature. For a real app, this would be a much more extensive list or a more advanced filter.
ALLOWED_COMMANDS = ["ls", "dir", "pwd", "date", "whoami", "echo", "cal"]

def run_secure_command(command: str) -> str:
    """
    Runs a shell command in a secure, non-privileged way.
    It checks against a whitelist of allowed commands.
    """
    # Using shlex to safely split the command string
    args = shlex.split(command)
    
    if not args or args[0] not in ALLOWED_COMMANDS:
        raise ValueError(f"Command '{args[0] if args else 'None'}' is not allowed for security reasons.")
    
    try:
        # Popen is a good choice for asynchronous execution
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=5)  # Add a timeout
        
        if process.returncode != 0:
            raise RuntimeError(f"Command failed with error: {stderr}")
            
        return stdout
        
    except subprocess.TimeoutExpired:
        process.kill()
        raise RuntimeError("Command execution timed out.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the command: {e}")