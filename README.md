# Craig's QA Kit

**Craig's QA Kit** is a collection of command-line utilities designed to streamline and expedite testing workflows for QA engineers. Originally created to reduce the time spent preparing specific test cases at work, this kit has grown into a versatile toolkit packed with useful features for both new and experienced testers.

---

## Overview

Traditionally, when working with multicast addresses for NWTest, testers had to:

- **Manually search for the multicast address**  
- **Copy or memorize the address**  
- **Construct and run the NWTest command with the correct arguments**  

Craig's QA Kit automates this process by scanning for multicast addresses, displaying them in the terminal, and directly integrating them with NWTest. This automation not only saves time but also minimizes errors—especially when running hundreds of tests.

---

## Key Features

- **Automated Test Preparation**  
  Quickly prepare and execute common test cases with minimal manual setup.

- **NWTest Multicast Automation**  
  Automatically scan for multicast addresses and feed them into NWTest without needing to remember or manually type commands.

- **Alias Creation**  
  Easily create an alias to run the kit from any directory.

- **Stress Testing Tools**  
  Run CPU, memory, and I/O stress tests with guided, user-friendly options.

- **Dependency Checks**  
  Built-in functions verify that required tools (such as ImageMagick, FFmpeg, NWTest, stress, and stress-ng) are installed, providing helpful feedback if any are missing.

---

## Getting Started

### Prerequisites

Ensure you have the following tools installed on your system:

- **ImageMagick** (for `convert`)  
- **FFmpeg** (for video processing)  
- **NWTest** (for network tests)  
- **stress** or **stress-ng** (for stress testing)  
- *(Optional)* **psutil** (for dynamic monitoring; install via `pip install psutil`)  

> **Note:**  
> The kit is designed primarily for **Linux**. It may also work on **macOS** with minor adjustments. Windows support is limited unless you use a Unix-like shell (e.g., Git Bash or WSL).

Contributing
This kit is a work in progress. There may be bugs or features that need refinement. If you find any issues or have suggestions for improvements:

Report Issues: Create a GitHub issue.
Contribute: Fork the repository and submit a pull request.
Your contributions and feedback are highly appreciated!

License
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
You may not remove or alter the original author's name (Craig Douglas) from any copies, forks, or derivative works.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Enjoy using Craig's QA Kit and happy testing!
