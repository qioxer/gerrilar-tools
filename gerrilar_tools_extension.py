import os
import subprocess
import webbrowser
from colorama import init, Fore

# Inicjalizacja colorama
init(autoreset=True)

def print_boxed_title(title):
    title_line = f"  {title}  "
    border = "+" + "-" * (len(title_line)) + "+"
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"|{title_line}|")
    print(Fore.CYAN + border)

def get_gerrilar_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_folder = os.path.join(desktop_path, "gerrilar tools")
    if os.path.isdir(target_folder):
        return target_folder
    else:
        print(Fore.RED + "Gerrilar Tools folder not found. Please initialize the environment (option 11) in the main MultiTools.")
        return None

def list_files_and_folders(folder):
    print(Fore.GREEN + f"Listing contents of {folder}:")
    for root, dirs, files in os.walk(folder):
        level = root.replace(folder, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

def load_dll_files(folder):
    dll_folder = os.path.join(folder, "dlls")
    if os.path.isdir(dll_folder):
        print(Fore.GREEN + "Found the following DLL files:")
        for file in os.listdir(dll_folder):
            if file.lower().endswith(".dll"):
                print(Fore.GREEN + f" - {file}")
        # Możesz dodać kod dynamicznego ładowania bibliotek przy użyciu ctypes tutaj
    else:
        print(Fore.RED + "No 'dlls' subfolder found in Gerrilar Tools folder.")

def launch_extension_wireshark(folder):
    ws_folder = os.path.join(folder, "wireshark")
    if os.path.isdir(ws_folder):
        potential_files = [f for f in os.listdir(ws_folder) if f.lower().endswith(".exe")]
        if potential_files:
            ws_path = os.path.join(ws_folder, potential_files[0])
            print(Fore.GREEN + f"Launching Wireshark extension from {ws_path} ...")
            try:
                if os.name == "nt":
                    os.startfile(ws_path)
                else:
                    subprocess.Popen([ws_path])
            except Exception as e:
                print(Fore.RED + f"Error launching Wireshark extension: {e}")
        else:
            print(Fore.RED + "No executable found in the 'wireshark' subfolder.")
    else:
        print(Fore.RED + "No 'wireshark' subfolder found in Gerrilar Tools folder.")

def main():
    folder = get_gerrilar_folder()
    if not folder:
        return

    print_boxed_title("Gerrilar Tools Extension")
    while True:
        print(Fore.MAGENTA + "1. List contents of Gerrilar Tools folder")
        print(Fore.MAGENTA + "2. Load DLL files (simulate dynamic loading)")
        print(Fore.MAGENTA + "3. Launch Wireshark extension (simulate)")
        print(Fore.MAGENTA + "4. Open Gerrilar Tools folder in Explorer")
        print(Fore.MAGENTA + "5. Exit Extension")
        choice = input(Fore.YELLOW + "Enter your choice (1-5): ").strip()
        if choice == "1":
            list_files_and_folders(folder)
        elif choice == "2":
            load_dll_files(folder)
        elif choice == "3":
            launch_extension_wireshark(folder)
        elif choice == "4":
            try:
                if os.name == "nt":
                    os.startfile(folder)
                else:
                    subprocess.run(["xdg-open", folder])
            except Exception as e:
                print(Fore.RED + f"Error opening folder: {e}")
        elif choice == "5":
            print(Fore.CYAN + "Exiting Extension...")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")
        input(Fore.YELLOW + "Press Enter to continue...")

if __name__ == "__main__":
    main()
import os
import subprocess
import webbrowser
from colorama import init, Fore

# Inicjalizacja colorama
init(autoreset=True)

def print_boxed_title(title):
    title_line = f"  {title}  "
    border = "+" + "-" * (len(title_line)) + "+"
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"|{title_line}|")
    print(Fore.CYAN + border)

def get_gerrilar_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_folder = os.path.join(desktop_path, "gerrilar tools")
    if os.path.isdir(target_folder):
        return target_folder
    else:
        print(Fore.RED + "Gerrilar Tools folder not found. Please initialize the environment (option 11) in the main MultiTools.")
        return None

def list_files_and_folders(folder):
    print(Fore.GREEN + f"Listing contents of {folder}:")
    for root, dirs, files in os.walk(folder):
        level = root.replace(folder, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

def load_dll_files(folder):
    dll_folder = os.path.join(folder, "dlls")
    if os.path.isdir(dll_folder):
        print(Fore.GREEN + "Found the following DLL files:")
        for file in os.listdir(dll_folder):
            if file.lower().endswith(".dll"):
                print(Fore.GREEN + f" - {file}")
        # Możesz dodać kod dynamicznego ładowania bibliotek przy użyciu ctypes tutaj
    else:
        print(Fore.RED + "No 'dlls' subfolder found in Gerrilar Tools folder.")

def launch_extension_wireshark(folder):
    ws_folder = os.path.join(folder, "wireshark")
    if os.path.isdir(ws_folder):
        potential_files = [f for f in os.listdir(ws_folder) if f.lower().endswith(".exe")]
        if potential_files:
            ws_path = os.path.join(ws_folder, potential_files[0])
            print(Fore.GREEN + f"Launching Wireshark extension from {ws_path} ...")
            try:
                if os.name == "nt":
                    os.startfile(ws_path)
                else:
                    subprocess.Popen([ws_path])
            except Exception as e:
                print(Fore.RED + f"Error launching Wireshark extension: {e}")
        else:
            print(Fore.RED + "No executable found in the 'wireshark' subfolder.")
    else:
        print(Fore.RED + "No 'wireshark' subfolder found in Gerrilar Tools folder.")

def main():
    folder = get_gerrilar_folder()
    if not folder:
        return

    print_boxed_title("Gerrilar Tools Extension")
    while True:
        print(Fore.MAGENTA + "1. List contents of Gerrilar Tools folder")
        print(Fore.MAGENTA + "2. Load DLL files (simulate dynamic loading)")
        print(Fore.MAGENTA + "3. Launch Wireshark extension (simulate)")
        print(Fore.MAGENTA + "4. Open Gerrilar Tools folder in Explorer")
        print(Fore.MAGENTA + "5. Exit Extension")
        choice = input(Fore.YELLOW + "Enter your choice (1-5): ").strip()
        if choice == "1":
            list_files_and_folders(folder)
        elif choice == "2":
            load_dll_files(folder)
        elif choice == "3":
            launch_extension_wireshark(folder)
        elif choice == "4":
            try:
                if os.name == "nt":
                    os.startfile(folder)
                else:
                    subprocess.run(["xdg-open", folder])
            except Exception as e:
                print(Fore.RED + f"Error opening folder: {e}")
        elif choice == "5":
            print(Fore.CYAN + "Exiting Extension...")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")
        input(Fore.YELLOW + "Press Enter to continue...")

if __name__ == "__main__":
    main()
