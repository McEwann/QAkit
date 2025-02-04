#!/usr/bin/env python3
import os
import subprocess
import requests
import sys
import platform

# Define the current version
CURRENT_VERSION = "1.5.1"
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
    if shell and "bash" in shell:
        config_file = os.path.expanduser("~/.bashrc")
    elif shell and "zsh" in shell:
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
    if shell and "bash" in shell:
        config_file = os.path.expanduser("~/.bashrc")
    elif shell and "zsh" in shell:
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
        "NWTest (nwtest)": "nwtest",
		"Stress (stress)": "stress",
		"Stress-ng (stress-ng)": "stress-ng"
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

def stress_test():
    """Perform an enhanced stress test with a guided interface.
    
    Offers:
      - Simple Mode: Predefined test profiles (Light, Moderate, Heavy)
      - Advanced Mode: Custom settings for CPU, Memory, and I/O stress
    """
    import time  # Ensure time is imported
    print("\n--- Enhanced Stress Testing ---")
    
    # Determine which stress tool is available.
    stress_tool = None
    if is_tool_installed("stress-ng"):
        print(f"{GREEN}Using stress-ng for testing.{RESET}")
        stress_tool = "stress-ng"
    elif is_tool_installed("stress"):
        print(f"{GREEN}Using stress for testing.{RESET}")
        stress_tool = "stress"
    else:
        print(f"{RED}No stress tool found. Please install stress or stress-ng via your package manager.{RESET}")
        return

    # Attempt to import psutil for monitoring.
    try:
        import psutil
    except ImportError:
        print(f"{RED}psutil module not installed. For monitoring, install it via 'pip install psutil'.{RESET}")
        psutil = None

    # Ask if the user wants to use advanced options.
    print("\nFor most users, we recommend using the Simple Mode which uses predefined test profiles.")
    print("If you are familiar with CPU and Memory settings and want to customize them, choose Advanced Mode.")
    adv_choice = input("Do you want to use advanced options? (y/n): ").strip().lower()
    if adv_choice not in ("y", "n"):
        print("Invalid choice, defaulting to Simple Mode.")
        adv_choice = "n"

    # Initialize parameters.
    cpu_workers = 0
    vm_workers = 0
    vm_bytes = ""
    io_workers = 0
    duration = 0

    if adv_choice == "y":
        # Advanced Mode: present detailed options.
        print("\nSelect the type of stress test you want to run:")
        print(" 1. CPU Stress only")
        print(" 2. Memory Stress only")
        print(" 3. I/O Stress only")
        print(" 4. Combined Stress (CPU + Memory + I/O)")
        
        while True:
            test_type = input("Enter your choice (1-4): ").strip()
            if test_type in ("1", "2", "3", "4"):
                break
            print("Invalid choice. Please enter a number between 1 and 4.")

        def get_int_input(prompt):
            while True:
                value = input(prompt).strip()
                try:
                    return int(value)
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

        if test_type == "1":
            print("\n--- CPU Stress ---")
            cpu_workers = get_int_input("Enter the number of CPU workers (e.g., 4): ")
            duration = get_int_input("Enter the test duration in seconds (e.g., 60): ")
        elif test_type == "2":
            print("\n--- Memory Stress ---")
            print("Memory stress simulates heavy memory usage by launching processes (called 'workers') that allocate memory.")
            print("For most systems, 1 or 2 workers is sufficient. If you're unsure, use a low number.")
            vm_workers = get_int_input("Enter the number of memory workers (try 1 or 2): ")
            vm_bytes = input("Enter the memory allocation per worker (e.g., 256M for 256 MB or 1G for 1 GB): ").strip()
            duration = get_int_input("Enter the test duration in seconds (e.g., 60): ")
        elif test_type == "3":
            print("\n--- I/O Stress ---")
            io_workers = get_int_input("Enter the number of I/O workers (e.g., 1 or 2): ")
            duration = get_int_input("Enter the test duration in seconds (e.g., 60): ")
        elif test_type == "4":
            print("\n--- Combined Stress (CPU + Memory + I/O) ---")
            cpu_workers = get_int_input("Enter the number of CPU workers (e.g., 2): ")
            print("Memory stress: A 'worker' allocates memory. Usually 1 or 2 is enough.")
            vm_workers = get_int_input("Enter the number of memory workers (e.g., 1 or 2): ")
            vm_bytes = input("Enter the memory allocation per worker (e.g., 256M): ").strip()
            io_workers = get_int_input("Enter the number of I/O workers (e.g., 1 or 2): ")
            duration = get_int_input("Enter the test duration in seconds (e.g., 60): ")
    else:
        # Simple Mode: Predefined Profiles.
        print("\n--- Simple Mode: Predefined Test Profiles ---")
        print("Choose a stress test intensity:")
        print(" 1. Light    - Basic test with low load")
        print(" 2. Moderate - Standard test with moderate load")
        print(" 3. Heavy    - Maximum load for intensive testing")
        while True:
            profile = input("Enter your choice (1-3): ").strip()
            if profile in ("1", "2", "3"):
                break
            print("Invalid choice. Please enter 1, 2, or 3.")
        if profile == "1":
            cpu_workers, vm_workers, io_workers, default_duration, vm_bytes = 2, 1, 1, 30, "256M"
        elif profile == "2":
            cpu_workers, vm_workers, io_workers, default_duration, vm_bytes = 4, 2, 2, 60, "512M"
        elif profile == "3":
            cpu_workers, vm_workers, io_workers, default_duration, vm_bytes = 8, 4, 4, 120, "1G"
        # Allow the user to override the default duration.
        override = input(f"Default test duration is {default_duration} seconds. Would you like to change it? (y/n): ").strip().lower()
        if override == 'y':
            try:
                duration = int(input("Enter desired duration in seconds: ").strip())
            except ValueError:
                print("Invalid input. Using default duration.")
                duration = default_duration
        else:
            duration = default_duration

    # Ask if the user wants to log resource usage.
    log_file = None
    while True:
        log_choice = input("\nDo you want to log resource usage to a file? (y/n): ").strip().lower()
        if log_choice in ("y", "n"):
            break
        print("Please enter 'y' or 'n'.")
    if log_choice == "y":
        log_file = input("Enter the full path for the log file (e.g., /home/user/stress_log.txt): ").strip()
        try:
            with open(log_file, "w") as f:
                f.write("TimeElapsed(s),CPU(%),Memory(%)\n")
        except Exception as e:
            print(f"{RED}Could not open log file: {e}{RESET}")
            log_file = None

    # Ask if CPU usage alerts should be set.
    threshold = None
    if psutil:
        while True:
            threshold_choice = input("\nWould you like to set a CPU usage threshold alert? (y/n): ").strip().lower()
            if threshold_choice in ("y", "n"):
                break
            print("Please enter 'y' or 'n'.")
        if threshold_choice == "y":
            while True:
                try:
                    threshold = float(input("Enter the CPU usage threshold percentage (e.g., 90): ").strip())
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number (e.g., 90).")

                       # Build the stress command.
    cmd_parts = []
    if stress_tool in ["stress", "stress-ng"]:
        if cpu_workers > 0:
            cmd_parts.append(f"--cpu {cpu_workers}")
        if vm_workers > 0:
            cmd_parts.append(f"--vm {vm_workers}")
            if vm_bytes:
                cmd_parts.append(f"--vm-bytes {vm_bytes}")
        if io_workers > 0:
            cmd_parts.append(f"--io {io_workers}")
        # For stress-ng, use a timeout with an "s" suffix.
        if stress_tool == "stress-ng":
            timeout_arg = f"--timeout {duration}s"
        else:
            timeout_arg = f"--timeout {duration}"
        cmd_parts.append(timeout_arg)
        cmd = f"{stress_tool} " + " ".join(cmd_parts)
    else:
        print(f"{RED}Error: No stress tool selected.{RESET}")
        return

    print(f"\n{GREEN}Starting stress test with command:{RESET}\n{cmd}\n")
    
    # Force the process to run in /tmp:
    # 1. Change the current working directory.
    # 2. Update the environment variables TMPDIR and PWD to /tmp.
    os.chdir("/tmp")
    env = os.environ.copy()
    env["TMPDIR"] = "/tmp"
    env["PWD"] = "/tmp"
    
    process = subprocess.Popen(cmd, shell=True, env=env)

    
    # Launch the stress test.
    process = subprocess.Popen(cmd, shell=True)
    start_time = time.time()

    try:
        while process.poll() is None:
            elapsed = time.time() - start_time
            remaining = max(0, duration - int(elapsed))
            status_str = f"Elapsed: {int(elapsed)}s, Remaining: {remaining}s"
            if psutil:
                cpu_usage = psutil.cpu_percent(interval=0.5)
                mem_usage = psutil.virtual_memory().percent
                status_str += f", CPU: {cpu_usage}%, Memory: {mem_usage}%"
                if threshold is not None and cpu_usage > threshold:
                    print(f"\n{RED}Alert: CPU usage exceeded {threshold}%!{RESET}")
            print(status_str, end="\r", flush=True)
            if log_file and psutil:
                with open(log_file, "a") as f:
                    f.write(f"{int(elapsed)},{cpu_usage},{mem_usage}\n")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{RED}Stress test interrupted by user.{RESET}")
        process.terminate()
        return

    print("\n" + f"{GREEN}Stress test completed.{RESET}")
    if psutil:
        final_cpu = psutil.cpu_percent(interval=1)
        final_mem = psutil.virtual_memory().percent
        print(f"Final CPU Usage: {final_cpu}%")
        print(f"Final Memory Usage: {final_mem}%")

def adjust_for_linux_version():
    """
    If running on Linux, print the distribution and version.
    You can expand this function to adjust commands or behavior based on the Linux version.
    """
    if platform.system() == "Linux":
        try:
            import distro  # Requires 'pip install distro' if not already installed
            distro_name = distro.name()
            distro_version = distro.version()
            print(f"{GREEN}Detected Linux distribution: {distro_name} {distro_version}{RESET}")
            # Example adjustment: warn if using an older version (customize as needed)
            # if distro.id() == "ubuntu" and tuple(map(int, distro_version.split('.'))) < (18, 4):
            #     print(f"{RED}Warning: Your Ubuntu version ({distro_version}) might not support all features of this script.{RESET}")
        except ImportError:
            # Fallback if 'distro' is not available
            print(f"{GREEN}Running on Linux, kernel version: {platform.release()}{RESET}")


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
        "7": ("Stress Testing", stress_test),
        "8": ("Exit", None),
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
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")


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
        adjust_for_linux_version()  # Check and display Linux version details (if applicable)
        display_dependencies()
        main_menu()
    except KeyboardInterrupt:
        print(f"{RED}Program interrupted by user..{RESET}")
        sys.exit(0)
