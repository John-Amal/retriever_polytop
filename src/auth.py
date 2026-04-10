import subprocess
import sys

def authenticate(script_path, username, password):
    """
    Runs the authentication script safely using subprocess.
    """
    print("--- Authentication ---")
    if not password:
        raise ValueError("Password missing. Set DESP_PASSWORD in .env file.")

    try:
        # Arguments passed as a list to avoid shell injection issues with special chars
        subprocess.run(
            [sys.executable, script_path, "-u", username, "-p", password],
            check=True,
            capture_output=True,
            text=True
        )
        print("Authentication successful.")
    except subprocess.CalledProcessError as e:
        print(f"Authentication failed.\nSTDERR: {e.stderr}")
        sys.exit(1)
