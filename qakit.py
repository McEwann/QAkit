#!/usr/bin/env python3
import os
import subprocess
import requests

# Define the current version
CURRENT_VERSION = "0.2.7"
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
            with open(__file__, "w") as script_file:
                script_file.write(response.text)
            print("Script updated successfully! Restarting...")
            
            # Restart the script
            python_executable = sys.executable  # Get the Python interpreter used to run the script
            os.execv(python_executable, [python_executable] + sys.argv)
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

def imagemagick_resize():
    """Resize an image."""
    input_file = input("Enter the input image file path: ").strip()
    output_file = input("Enter the output image file path: ").strip()
    dimensions = input("Enter the new dimensions (e.g., 800x600): ").strip()
    command = f"convert {input_file} -resize {dimensions} {output_file}"
    run_command(command)

def imagemagick_set_transparent_background():
    """Set an image's background to transparent."""
    input_file = input("Enter the input image file path: ").strip()
    output_file = input("Enter the output image file path: ").strip()
    color_to_make_transparent = input("Enter the background color to make transparent (e.g., white): ").strip()
    command = f"convert {input_file} -transparent {color_to_make_transparent} {output_file}"
    run_command(command)

def ffmpeg_compress_video():
    """Compress a video."""
    input_file = input("Enter the input video file path: ").strip()
    output_file = input("Enter the output video file path: ").strip()
    command = f"ffmpeg -i {input_file} -vcodec libx264 -crf 28 {output_file}"
    run_command(command)

def ffmpeg_convert_video():
    """Convert a video format."""
    input_file = input("Enter the input video file path: ").strip()
    output_format = input("Enter the desired output format (e.g., mp4, avi, mkv): ").strip()
    output_file = f"{os.path.splitext(input_file)[0]}.{output_format}"
    command = f"ffmpeg -i {input_file} {output_file}"
    run_command(command)

def ffmpeg_extract_audio():
    """Extract audio from a video."""
    input_file = input("Enter the input video file path: ").strip()
    output_file = input("Enter the output audio file path (e.g., audio.mp3): ").strip()
    command = f"ffmpeg -i {input_file} -q:a 0 -map a {output_file}"
    run_command(command)

def ffmpeg_set_green_background():
    """Set a video's background to green for chroma keying."""
    input_file = input("Enter the input video file path: ").strip()
    output_file = input("Enter the output video file path: ").strip()
    color_to_replace = input("Enter the color to replace (e.g., black): ").strip().lower()
    command = f"ffmpeg -i {input_file} -vf chromakey={color_to_replace}:similarity=0.2:blend=0.0,format=yuv420p {output_file}"
    run_command(command)

def list_multicast_addresses():
    """List visible multicast addresses."""
    command = "ip maddr show"
    run_command(command)

def nwtest_multicast():
    """Test multicast addresses using nwtest with detailed output."""
    multicast_address = input("Enter the multicast address to test: ").strip()
    duration = input("Enter the duration (in seconds) to run, or leave blank to run indefinitely: ").strip()
    verbose = input("Enable verbose output? (yes/no): ").strip().lower() == "yes"
    detailed_encryption_check = input("Enable detailed packet/encryption analysis? (yes/no): ").strip().lower() == "yes"

    duration_option = f"-n {duration}" if duration else ""
    verbose_option = "-v" if verbose else ""
    encryption_option = "-C UTF-8" if detailed_encryption_check else ""  # Adjust to the correct flag for encryption analysis

    # Construct the command
    command = f"nwtest -cs1 {multicast_address} {duration_option} {verbose_option} {encryption_option}".strip()
    print(f"Running: {command}")

    try:
        # Run the command and capture its real-time output
        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("\n--- nwtest Output ---")
        for line in process.stdout:
            print(line, end="")  # Display each line of output
        
        process.wait()  # Wait for the process to complete
        print("\n--- End of nwtest Output ---")
        
        if process.returncode == 0:
            print("nwtest completed successfully!")
        else:
            print(f"nwtest exited with errors (code: {process.returncode}).")
            error_output = process.stderr.read()
            if error_output:
                print("--- nwtest Errors ---")
                print(error_output)
            
    except Exception as e:
        print(f"Error running nwtest: {e}")


# Main menu
def main():
    display_intro()

    # Check dependencies
    dependencies = check_dependencies()

    # Check for updates
    update_available, latest_version = check_for_updates()

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
            if dependency and not dependencies[dependency]:
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
