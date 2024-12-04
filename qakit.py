#!/usr/bin/env python3
import os
import subprocess
import requests

# Define the current version
CURRENT_VERSION = "0.2.1"
GITHUB_REPO_URL = "https://raw.githubusercontent.com/McEwann/QAkit/main/qakit.py"

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

def check_for_updates():
    """Check if a new version of the script is available on GitHub."""
    print("Checking for updates...")
    try:
        response = requests.get(GITHUB_REPO_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if "CURRENT_VERSION" in line:
                    latest_version = line.split('"')[1]
                    if latest_version > CURRENT_VERSION:
                        print(f"A newer version ({latest_version}) is available!")
                        return True
                    else:
                        print("You are using the latest version.")
                        return False
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
    return False

def update_script():
    """Update the script to the latest version from GitHub."""
    print("Updating script...")
    try:
        response = requests.get(GITHUB_REPO_URL, timeout=10)
        if response.status_code == 200:
            with open(__file__, "w") as script_file:
                script_file.write(response.text)
            print("Script updated successfully! Please restart it to apply changes.")
        else:
            print(f"Failed to fetch the latest version. HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error updating script: {e}")

# Functions for individual features
def imagemagick_convert():
    """Convert an image to another format."""
    input_file = input("Enter the input image file path: ").strip()
    output_format = input("Enter the desired output format (e.g., png, jpg, gif): ").strip()
    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
    command = f"convert {input_file} {output_file}"
    run_command(command)

def ffmpeg_compress_video():
    """Compress a video."""
    input_file = input("Enter the input video file path: ").strip()
    output_file = input("Enter the output video file path: ").strip()
    command = f"ffmpeg -i {input_file} -vcodec libx264 -crf 28 {output_file}"
    run_command(command)

def list_multicast_addresses():
    """List visible multicast addresses."""
    command = "ip maddr show"
    run_command(command)

# Main menu
def main():
    display_intro()

    # Check dependencies
    dependencies = check_dependencies()

    # Define menu options
    options = {
        "1": ("Convert an image using ImageMagick", imagemagick_convert, "ImageMagick (convert)"),
        "2": ("Compress a video using FFmpeg", ffmpeg_compress_video, "FFmpeg (ffmpeg)"),
        "3": ("List visible multicast addresses", list_multicast_addresses, "NWTest (nwtest)"),
        "4": ("Check for updates", check_for_updates, None),
        "5": ("Update script", update_script, None),
        "6": ("Exit", lambda: print("Exiting QA Toolkit. Goodbye!"), None),
    }

    while True:
        print("\nQA Toolkit - Choose an option:")
        for key, (description, _, dependency) in options.items():
            dep_status = ""
            if dependency and not dependencies[dependency]:
                dep_status = " (Dependencies not met)"
            print(f"{key}. {description}{dep_status}")

        choice = input("Enter your choice: ").strip()

        if choice in options:
            description, action, dependency = options[choice]
            if dependency and not dependencies[dependency]:
                print(f"Cannot execute '{description}': Dependencies not met.")
                continue
            if choice == "4":
                # Check for updates
                if check_for_updates():
                    print("Run the 'Update script' option to update.")
            elif choice == "5":
                # Update script
                update_script()
                break
            elif choice == "6":
                # Exit
                action()
                break
            else:
                # Run the selected action
                action()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
