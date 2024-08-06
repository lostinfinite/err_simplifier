import sys
import traceback
from datetime import datetime
from colorama import init, Fore, Style
import re
import os

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
