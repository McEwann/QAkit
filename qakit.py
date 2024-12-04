#!/usr/bin/env python3
import os
import subprocess
import requests
import sys

# Define the current version
CURRENT_VERSION = "0.3.5"
GITHUB_REPO_URL = "https://raw.githubusercontent.com/McEwann/QAkit/main/qakit.py?nocache=1"

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

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
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:\n", result.stderr)
        if result.returncode == 0:
            print("Command executed successfully!")
        else:
            print("Command failed. Please check the errors above.")
        return result.returncode
    except Exception as e:
        print(f"Error executing command: {e}")
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
    return {
        "ImageMagick (convert)": is_tool_installed("convert"),
        "FFmpeg (ffmpeg)": is_tool_installed("ffmpeg"),
        "NWTest (nwtest)": is_tool_installed("nwtest"),
    }

def version_tuple(version):
    """Convert version string to tuple for comparison.""" 
    return tuple(map(int, version.split(".")))

def check_for_updates():
    """Check if a new version of the script is available on GitHub.""" 
    print("Checking for updates...")
    try:
        response = requests.get(GITHUB_REPO_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if "CURRENT_VERSION" in line:
                    latest_version = line.split('"')[1]
                    if version_tuple(latest_version) > version_tuple(CURRENT_VERSION):
                        print(f"A newer version ({latest_version}) is available!")
                        return True, latest_version
                    else:
                        print("You are using the latest version.")
                        return False, CURRENT_VERSION
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
    return False, CURRENT_VERSION

def update_script():
    """Update the script to the latest version from GitHub and restart."""
    print("Updating script...")
    try:
        response = requests.get(GITHUB_REPO_URL, timeout=10)
        if response.status_code == 200:
            updated_script = response.text

            # Ensure 'import sys' is included (or any necessary checks)
            if "import sys" not in updated_script:
                updated_script = "import sys\n" + updated_script

            # Only update the version part or specific parts that need updating
            updated_script_lines = updated_script.splitlines()

            # Check for lines that should be updated (like version information)
            for idx, line in enumerate(updated_script_lines):
                if line.startswith("CURRENT_VERSION"):
                    updated_script_lines[idx] = f'CURRENT_VERSION = "{CURRENT_VERSION}"'  # Preserve the current version

            # Now write back only specific changes
            with open(__file__, "w") as script_file:
                script_file.write("\n".join(updated_script_lines))
            print("Script updated successfully! Restarting...")

            # Restart the script
            python_executable = sys.executable  # Get the Python interpreter used to run the script
            os.execv(python_executable, [python_executable] + sys.argv)
        else:
            print(f"Failed to fetch the latest version. HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error updating script: {e}")

# Functions for individual features (image and video processing, etc.)

# Main menu
def main():
    display_intro()

    # Check dependencies
    dependencies = check_dependencies()

    # Check for updates
    update_available, latest_version = check_for_updates()

    # Define disabled options
    disabled_options = {} 
    awaiting_fix_label = "Awaiting fix"
    
    # Define menu options
    options = {
        "1": ("Convert an image using ImageMagick", imagemagick_convert, "ImageMagick (convert)"),
        "2": ("Resize an image using ImageMagick", imagemagick_resize, "ImageMagick (convert)"),
        "3": ("Set an image's background to transparent using ImageMagick", imagemagick_set_transparent_background, "ImageMagick (convert)"),
        "4": ("Compress a video using FFmpeg", ffmpeg_compress_video, "FFmpeg (ffmpeg)"),
        "5": ("Convert a video format using FFmpeg", ffmpeg_convert_video, "FFmpeg (ffmpeg)"),
        "6": ("Extract audio from a video using FFmpeg", ffmpeg_extract_audio, "FFmpeg (ffmpeg)"),
        "7": ("Set a video's background to green using FFmpeg", ffmpeg_set_green_background, "FFmpeg (ffmpeg)"),
        "8": ("List visible multicast addresses", list_multicast_addresses, None),
        "9": ("Test a multicast address with NWTest", nwtest_multicast, "NWTest (nwtest)"),
        "10": (
            "Update script" if update_available else "No updates available",
            update_script if update_available else None,
            None,
        ),
        "11": ("Exit", lambda: print("Exiting QA Toolkit. Goodbye!"), None),
    }

    while True:
        print("\nQA Toolkit - Choose an option:")
        for key, (description, action, dependency) in options.items():
            if key in disabled_options:
                color = RED
                dep_status = f" ({awaiting_fix_label})"
            elif dependency and not dependencies[dependency]:
                color = RED
                dep_status = " (Dependencies not met)"
            elif key == "10" and not update_available:
                color = RED
                dep_status = ""
            elif key == "10" and update_available:
                color = GREEN
                dep_status = f" (Update available: {latest_version})"
            else:
                color = GREEN
                dep_status = ""
            print(f"{color}{key}. {description}{dep_status}{RESET}")

        choice = input("Enter your choice: ").strip()

        if choice in options:
            description, action, dependency = options[choice]
            if dependency and not dependencies[dependency]:
                print(f"{RED}Cannot execute '{description}': Dependencies not met.{RESET}")
                continue
            if action:
                action()
            if choice == "11":
                break
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")

if __name__ == "__main__":
    main()
