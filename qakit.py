#!/usr/bin/env python3
import os
import subprocess
import requests
import sys
import platform

# Define the current version
CURRENT_VERSION = "1.0"
GITHUB_REPO_URL = "https://raw.githubusercontent.com/McEwann/QAkit/main/qakit.py?nocache=1"

# ANSI color codes (conditionally enabled)
if platform.system() == "Windows":
    GREEN = RED = RESET = ""
else:
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

def alias_exists():
    """Check if the alias for qakit already exists in the shell configuration file."""
    shell = os.getenv("SHELL")
    if "bash" in shell:
        config_file = os.path.expanduser("~/.bashrc")
    elif "zsh" in shell:
        config_file = os.path.expanduser("~/.zshrc")
    else:
        return False

    try:
        with open(config_file, "r") as f:
            content = f.read()
            return "alias qakit=" in content
    except Exception as e:
        print(f"{RED}Error checking for alias in config file: {e}{RESET}")
        return False

def create_alias():
    """Create an alias for qakit based on the current working directory."""
    if alias_exists():
        print(f"{RED}Alias already exists. Skipping alias creation.{RESET}")
        return

    current_directory = os.getcwd()
    alias_command = f"alias qakit='python3 {current_directory}/qakit.py'"

    shell = os.getenv("SHELL")
    if "bash" in shell:
        config_file = os.path.expanduser("~/.bashrc")
    elif "zsh" in shell:
        config_file = os.path.expanduser("~/.zshrc")
    else:
        print(f"{RED}Unsupported shell: {shell}. Alias not created.{RESET}")
        return

    try:
        with open(config_file, "a") as f:
         f.write(f"\n{alias_command}\n")

        print(f"{GREEN}Alias created successfully! To use it, please restart your shell or run 'source {config_file}'.{RESET}")
    except Exception as e:
        print(f"{RED}Error creating alias: {e}{RESET}")

def display_intro():
    print(f"""
Craig's QA Kit - Version {CURRENT_VERSION}

This toolkit is designed to assist QA engineers with:
- Streamlining test preparation.
- Simplifying troubleshooting steps.
- Performing common multimedia and network tasks.

Important:
These tools are NOT a replacement for proper testing procedures.
Always ensure thorough and appropriate testing for your use case.
""")

def run_command(command):
    """Runs a shell command and prints its output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            env={**os.environ, "LD_LIBRARY_PATH": "/usr/local/triplecms/lib"}
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"{RED}Errors:\n{result.stderr}{RESET}")
        if result.returncode == 0:
            print(f"{GREEN}Command executed successfully!{RESET}")
        else:
            print(f"{RED}Command failed. Please check the errors above.{RESET}")
        return result.returncode
    except Exception as e:
        print(f"{RED}Error executing command: {e}{RESET}")
        return None

def is_tool_installed(tool):
    """Check if a specific tool is installed on the system."""
    try:
        subprocess.run([tool, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def check_dependencies():
    """Check for required tools and their availability."""
    tools = {
        "ImageMagick (convert)": "convert",
        "FFmpeg (ffmpeg)": "ffmpeg",
        "NWTest (nwtest)": "nwtest"
    }
    return {name: is_tool_installed(command) for name, command in tools.items()}

def display_dependencies():
    """Display the status of tool dependencies."""
    print("\nChecking dependencies...")
    statuses = check_dependencies()
    for name, status in statuses.items():
        color = GREEN if status else RED
        print(f"{color}{name}: {'Installed' if status else 'Not Installed'}{RESET}")

def imagemagick_convert():
    input_file = input("Enter the input image file path: ").strip()
    output_format = input("Enter the desired output format (e.g., png, jpg): ").strip()
    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
    run_command(f"convert {input_file} {output_file}")

def ffmpeg_compress_video():
    input_file = input("Enter the input video file path: ").strip()
    output_file = input("Enter the output video file path: ").strip()
    run_command(f"ffmpeg -i {input_file} -vcodec libx264 -crf 28 {output_file}")

def imagemagick_resize():
    input_file = input("Enter the input image file path: ").strip()
    dimensions = input("Enter the dimensions (e.g., 800x600): ").strip()
    output_file = input("Enter the output file path: ").strip()
    run_command(f"convert {input_file} -resize {dimensions} {output_file}")

def imagemagick_rotate():
    input_file = input("Enter the input image file path: ").strip()
    angle = input("Enter the rotation angle (e.g., 90): ").strip()
    output_file = input("Enter the output file path: ").strip()
    run_command(f"convert {input_file} -rotate {angle} {output_file}")

def ffmpeg_resize_video():
    input_file = input("Enter the input video file path: ").strip()
    dimensions = input("Enter the dimensions (e.g., 1280x720): ").strip()
    output_file = input("Enter the output file path: ").strip()
    run_command(f"ffmpeg -i {input_file} -vf scale={dimensions} {output_file}")

def ffmpeg_extract_audio():
    input_file = input("Enter the input video file path: ").strip()
    output_file = input("Enter the output audio file path: ").strip()
    run_command(f"ffmpeg -i {input_file} -q:a 0 -map a {output_file}")

def ffmpeg_set_green_background():
    input_file = input("Enter the input video file path: ").strip()
    color = input("Enter the color to replace (e.g., black): ").strip()
    output_file = input("Enter the output video file path: ").strip()
    run_command(f"ffmpeg -i {input_file} -vf chromakey={color}:similarity=0.2:blend=0.0 {output_file}")

def nwtest_multicast():
    address = input("Enter the multicast address to test: ").strip()
    duration = input("Enter the duration for the test (seconds): ").strip()
    run_command(f"nwtest -cs1 {address} -n {duration}")

def check_connection():
    target = input("Enter the IP or domain to ping: ").strip()
    run_command(f"ping -c 4 {target}")

def download_file():
    url = input("Enter the file URL: ").strip()
    output_path = input("Enter the output file path: ").strip()
    run_command(f"wget -O {output_path} {url}")


def list_multicast_addresses():
    run_command("ip maddr show")

def main_menu():
    def image_tools_menu():
        options = {
            "1": ("Convert an image", imagemagick_convert),
            "2": ("Resize an image", imagemagick_resize),
            "3": ("Rotate an image", imagemagick_rotate),
            "4": ("Back to Main Menu", None),
        }
        handle_menu("Image Tools", options)

    def video_tools_menu():
        options = {
            "1": ("Compress a video", ffmpeg_compress_video),
            "2": ("Resize a video", ffmpeg_resize_video),
            "3": ("Extract audio from a video", ffmpeg_extract_audio),
            "4": ("Set a video's background to green", ffmpeg_set_green_background),
            "5": ("Back to Main Menu", None),
        }
        handle_menu("Video Tools", options)

    def network_tools_menu():
        options = {
            "1": ("List multicast addresses", list_multicast_addresses),
            "2": ("Test a multicast address", nwtest_multicast),
            "3": ("Ping a specific IP or domain", check_connection),
            "4": ("Download a file", download_file),
            "5": ("Back to Main Menu", None),
        }
        handle_menu("Network Tools", options)

    options = {
        "1": ("Image Tools", image_tools_menu),
        "2": ("Video Tools", video_tools_menu),
        "3": ("Network Tools", network_tools_menu),
        "4": ("Check for Updates", lambda: update_script() if check_for_updates() else None),
        "5": ("Create Alias for qakit", create_alias),
        "6": ("Display Dependencies", display_dependencies),
        "7": ("Exit", None),
    }
    handle_menu("Main Menu", options)


def handle_menu(title, options):
    while True:
        print(f"\n--- {title} ---")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")
        choice = input("Enter your choice: ").strip()
        if choice in options:
            _, action = options[choice]
            if action:
                action()
            else:
                break

def version_tuple(version):
    return tuple(map(int, version.split(".")))

def check_for_updates():
    print("Checking for updates...")
    try:
        response = requests.get(GITHUB_REPO_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if "CURRENT_VERSION" in line:
                    latest_version = line.split('"')[1]
                    if version_tuple(latest_version) > version_tuple(CURRENT_VERSION):
                        print(f"{GREEN}A newer version ({latest_version}) is available!{RESET}")
                        return True
                    else:
                        print(f"{GREEN}You are using the latest version.{RESET}")
                        return False
    except Exception as e:
        print(f"{RED}Error checking for updates: {e}{RESET}")
    return False

def update_script():
    print("Updating script...")
    try:
        response = requests.get(GITHUB_REPO_URL, timeout=10)
        if response.status_code == 200:
            updated_script = response.text
            try:
                with open(__file__, "w") as script_file:
                    script_file.write(updated_script)
                print(f"{GREEN}Script updated successfully! Please restart.{RESET}")
                sys.exit()
            except PermissionError:
                print(f"{RED}Permission denied. Please run the script with sudo privileges to update.{RESET}")
        else:
            print(f"{RED}Failed to fetch the update. HTTP Status: {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}Error updating script: {e}{RESET}")

if __name__ == "__main__":
    try:
        display_intro()
        display_dependencies()
        main_menu()
    except KeyboardInterrupt:
        print(f"{RED}Program interrupted by user..{RESET}")
        sys.exit(0)

