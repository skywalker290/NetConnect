import os
import platform
from colorama import init

def clear_terminal():
    init(autoreset=True)
    system_platform = platform.system().lower()
    if system_platform == "windows":
        os.system("cls")
    else:
        os.system("clear")



def print_file_content(file_path):
    clear_terminal()
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

print_file_content("Chat.txt")
input("helo_>")


print_file_content("Chat.txt")
input("helo_>")