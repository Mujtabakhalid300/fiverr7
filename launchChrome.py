import subprocess

def launch_chrome():
    # Command to launch Google Chrome with the desired flags
    command = [
        "google-chrome",
        "--remote-debugging-port=9222",
        "--user-data-dir=~/.config/google-chrome/default"
        
    ]

    try:
        # Use subprocess to run the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Google Chrome launched with remote debugging enabled.")
    except FileNotFoundError:
        print("Google Chrome is not installed or not in PATH. Please check your installation.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    launch_chrome()
