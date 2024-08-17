import sys
import traceback
from datetime import datetime
from colorama import init, Fore, Style
import re
import os
import time

# Define the license text
license_text = """
### err-simplifier License Agreement

1. Acceptance and Binding Nature of Agreement
By using, accessing, or interacting with the err-simplifier software (“the Software”) in any manner, you acknowledge and agree to be bound by the terms of this License Agreement, regardless of whether you have read or fully understood these terms. This License Agreement serves as a binding contract, terms of service, and terms of use. You will be held responsible for compliance with this Agreement, even if you are unaware of its contents.

2. Grant of License
You are granted a limited, non-exclusive, non-transferable, and revocable license to use the Software for non-commercial, personal, or educational purposes only, subject to the terms and conditions outlined below.

3. Permitted Use
You are specifically permitted to use the Software for the following purposes:
   - Debugging: Using the Software to help debug your own Python code.
   - Error Interpretation: Using the Software to interpret, simplify, or understand complex error outputs from a Python terminal.
   - Code Obfuscation Interpretation: Using the Software to understand or de-obfuscate complex, error-prone, or obfuscated Python code.

You are explicitly prohibited from using the Software to write or develop your own version of the Software or any similar software.

4. Assertion of Intellectual Property Rights
The author of the Software asserts certain rights traditionally associated with copyright, patent, and trademark law, even though the Software may not be officially registered under these categories. This license seeks to provide protections that mirror those granted by such registrations, to the extent permitted by law.

   - Copyright-Like Rights: The author retains all rights over the specific expression of ideas contained in the Software. You may not copy, distribute, modify, or create derivative works of the Software without explicit permission.
   - Patent-Like Rights: The author asserts rights over any methods, processes, or functionalities contained in the Software. You are prohibited from filing patents or creating derivative technologies based on the Software without explicit permission.
   - Trademark-Like Rights: The name “err-simplifier” and any associated branding are protected under this license. You may not use the name, branding, or any confusingly similar names/brands in any manner that might imply endorsement or affiliation without explicit permission.

5. Prohibited Uses
You are explicitly prohibited from:
   - Commercial Use: Using the Software or any modified version for any commercial purposes.
   - Modification and Distribution: Altering, modifying, or creating derivative works based on the Software, or distributing the Software or any derivative works, without express permission.
   - Reverse Engineering: Attempting to decompile, reverse engineer, or disassemble the Software.
   - Development of Similar Software: Writing or developing a version of the Software or any software with similar functionalities.

6. Violation of License
If you copy, reproduce, or distribute any portion of the Software in violation of this license, or if you incorporate any lines from the Software into your own projects without permission, the author reserves the right to take legal action for breach of this license. While this license does not constitute an official copyright, patent, or trademark, it is intended to provide the author with rights similar to those protections under the law.

7. Third-Party Dependencies and Packages
This license does not apply to any dependencies, libraries, or third-party packages that are used in the creation or operation of the Software (“Third-Party Packages”). You are free to use, modify, or distribute these Third-Party Packages according to their respective licenses. This License Agreement only applies to the original code, methods, and content created by the author of the Software. Any use of the Third-Party Packages is governed by their respective licenses, and no part of those packages is protected under this License Agreement unless specifically created by the author of this Software.

8. License Limitations
This license does not constitute an official registration under copyright, patent, or trademark law. However, by using the Software, you agree to respect the rights asserted by the author in this agreement. The author does not claim ownership of rights not granted by law, but this license is intended to protect the author’s interests as if those rights were officially registered.

9. Responsibility and Common Sense Usage
You are expected to use the Software responsibly and with common sense. The author is not responsible for any misuse of the Software that results from negligence, lack of understanding, or failure to adhere to the terms of this Agreement. Users should ensure they are acting within the legal and ethical boundaries as outlined by this License.

10. Termination
This license will automatically terminate if you violate any of its terms. Upon termination, you must destroy all copies of the Software in your possession and cease all use.

11. Disclaimer of Warranty
The Software is provided "as-is" without any warranty of any kind, either express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement.

12. Limitation of Liability
In no event shall the author be liable for any claims, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

13. Governing Law
This License shall be governed by and construed in accordance with the laws of the Commonwealth of Pennsylvania, without regard to its conflict of laws principles.

14. Entire Agreement
This License constitutes the entire agreement between you and the author of the Software and supersedes any prior agreements, understandings, or representations, whether written or oral, concerning the subject matter of this License.

By using the Software, you agree to be bound by the terms of this License.
"""

# Print the license text
print(license_text)

# Wait for a few seconds to allow the user to read
print("\nPlease read the above license carefully. Continuing in 15 seconds...")
time.sleep(15)

# Proceed with the rest of the code
print("\nContinuing with the execution of the program...")

# Rest of your code goes here
# For example:
print("Executing the main functionality of the software...")

# Initialize colorama
init(autoreset=True)

# Check if the terminal supports color
def supports_color():
    return sys.stdout.isatty() and (os.getenv('COLORTERM') in ['truecolor', '24bit'] or os.getenv('TERM') == 'xterm-256color')

def format_output(output_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gray_timestamp = f"{Style.DIM}{timestamp}{Style.RESET_ALL}" if supports_color() else timestamp
    
    if output_type == "info":
        color = Fore.BLUE if supports_color() else ''
        formatted_message = f"{gray_timestamp} {color}INFO{Style.RESET_ALL}: {simplify_message(message)}"
    elif output_type == "warning":
        color = Fore.YELLOW if supports_color() else ''
        formatted_message = f"{gray_timestamp} {color}WARNING{Style.RESET_ALL}: {simplify_message(message)}"
    elif output_type == "error":
        color = Fore.RED if supports_color() else ''
        formatted_message = f"{gray_timestamp} {color}ERROR{Style.RESET_ALL}: {simplify_message(message)}"
    else:
        color = Fore.CYAN if supports_color() else ''
        formatted_message = f"{gray_timestamp} {color}OTHER{Style.RESET_ALL}: {simplify_message(message)}"
    
    return formatted_message

def log_message(output_type, message):
    formatted_message = format_output(output_type, message)
    print(formatted_message)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    simplified_message = simplify_traceback(tb)
    log_message("error", f"{exc_type.__name__}: {exc_value}")
    log_message("error", simplified_message)

def simplify_traceback(traceback_str):
    lines = traceback_str.strip().split('\n')
    simplified_lines = []
    
    for line in lines:
        if "File" in line and "line" in line:
            simplified_lines.append(line.strip())
        elif any(keyword in line for keyword in ["Error", "Exception"]):
            simplified_lines.append(line.strip())
    
    return '\n'.join(simplified_lines)

def simplify_message(message):
    # Check for specific key phrases and simplify the message
    if "already satisfied" in message:
        match = re.search(r"Requirement already satisfied: (\S+)", message)
        if match:
            return f"Already satisfied/installed: {match.group(1)}"
    
    if "Defaulting to user installation" in message:
        return "Defaulting to user installation because system-wide site-packages are not writable."
    
    if "Requirement already satisfied" in message:
        match = re.search(r"Requirement already satisfied: (\S+) in", message)
        if match:
            return f"Already satisfied/installed: {match.group(1)}"
    
    if "pip" in message and "Requirement already satisfied" in message:
        return "The pip package is already installed."

    # Detailed error simplifications
    if "ModuleNotFoundError" in message:
        match = re.search(r"No module named '(.+)'", message)
        if match:
            return f"Module '{match.group(1)}' not found. Did you forget to install it?"
    
    if "ImportError" in message:
        match = re.search(r"cannot import name '(.+)'", message)
        if match:
            return f"Failed to import '{match.group(1)}'. Check if it is correctly installed and accessible."
    
    if "FileNotFoundError" in message:
        match = re.search(r"No such file or directory: '(.+)'", message)
        if match:
            return f"File '{match.group(1)}' not found. Check the file path and ensure it exists."
    
    if "ZeroDivisionError" in message:
        return "Attempted to divide by zero. Ensure the denominator is not zero."
    
    if "ValueError" in message:
        match = re.search(r"invalid literal for int\(\) with base 10: '(.+)'", message)
        if match:
            return f"Value '{match.group(1)}' is not a valid integer. Ensure the value can be converted to an integer."
    
    # Add more error simplifications as needed

    return message

sys.excepthook = handle_exception

# Example usage of logging messages
if __name__ == "__main__":
    try:
        log_message("info", "This is an informational message.")
        log_message("warning", "This is a warning message.")
        log_message("error", "This is an error message.")
        log_message("other", "This is some other type of message.")
        
        # Example error
        x = 1 / 0
        
    except Exception as e:
        handle_exception(type(e), e, e.__traceback__)
