import os
import subprocess
import re
import requests
import webbrowser
import pyfiglet
import shutil
import codecs
from datetime import datetime
from colorama import init, Fore

# Inicjalizacja colorama
init(autoreset=True)

# Globalne zmienne środowiskowe
env_initialized = False
env_folder = None  # Folder "gerrilar tools" na pulpicie

def encrypt_content(content):
    """Prosta funkcja szyfrująca metodą ROT13."""
    return codecs.encode(content, 'rot_13')

def log_action(message):
    """Zapisuje komunikat do pliku logs.txt w folderze env_folder, jeśli środowisko jest zainicjalizowane."""
    global env_folder
    if env_initialized and env_folder:
        log_file = os.path.join(env_folder, "logs.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print(Fore.RED + f"Error writing log: {e}")

def require_initialized():
    """Sprawdza, czy środowisko zostało zainicjalizowane (opcja 11)."""
    if not env_initialized:
        print(Fore.RED + "Environment not initialized! Please run option 11 (Download Important Files) first.")
        return False
    return True

def safe_input(prompt):
    """Bezpieczne pobieranie danych od użytkownika (przechwytywanie Ctrl+C)."""
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Returning to main menu...")
        return ""

def print_boxed_title(title):
    title_line = f"  {title}  "
    border = "+" + "-" * (len(title_line)) + "+"
    print(Fore.CYAN + border)
    print(Fore.CYAN + f"|{title_line}|")
    print(Fore.CYAN + border)

def print_banner():
    banner = pyfiglet.figlet_format("GERRILAR TOOLS", font="slant")
    print(Fore.GREEN + banner)

# ------------------ EXE Files Python ------------------
def exe_converter():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("EXE Files Python")
    file_path = safe_input(Fore.YELLOW + "Enter full path to the .py file: ").strip()
    if file_path == "":
        return
    if not os.path.isfile(file_path):
        print(Fore.RED + "Error: File not found.")
        log_action("EXE Converter: File not found: " + file_path)
        safe_input("Press Enter to return to main menu...")
        return

    output_name = safe_input(Fore.YELLOW + "Enter desired output EXE name (without extension): ").strip()
    if output_name == "":
        safe_input("Press Enter to return to main menu...")
        return
    if output_name.lower().endswith(".exe"):
        output_name = output_name[:-4].strip()
    
    command = ["pyinstaller", "--onefile", "--name", output_name, file_path]
    print(Fore.YELLOW + "Converting, please wait...")
    try:
        subprocess.run(command, check=True)
        print(Fore.GREEN + f"Success! {output_name}.exe created in the 'dist' folder.")
        log_action(f"EXE Converter: Converted {file_path} to {output_name}.exe")
    except FileNotFoundError:
        print(Fore.RED + "Error: 'pyinstaller' not found. Ensure PyInstaller is installed and in your PATH.")
        log_action("EXE Converter: PyInstaller not found.")
        safe_input("Press Enter to return to main menu...")
        return
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Conversion failed: {e}")
        log_action(f"EXE Converter: Conversion failed for {file_path} with error: {e}")
        safe_input("Press Enter to return to main menu...")
        return

    # Dodaj dodatkowe pliki DLL, jeśli folder "dlls" istnieje
    dist_folder = os.path.join(os.getcwd(), "dist")
    dll_folder = os.path.join(os.getcwd(), "dlls")
    if os.path.isdir(dll_folder):
        print(Fore.YELLOW + "Adding additional DLL files...")
        for file in os.listdir(dll_folder):
            source_file = os.path.join(dll_folder, file)
            destination_file = os.path.join(dist_folder, file)
            try:
                shutil.copy(source_file, destination_file)
                print(Fore.GREEN + f"Copied DLL file: {file}")
                log_action(f"EXE Converter: Copied DLL file: {file}")
            except Exception as e:
                print(Fore.RED + f"Error copying {file}: {e}")
                log_action(f"EXE Converter: Error copying {file}: {e}")
    else:
        print(Fore.YELLOW + "No additional DLL folder found. Skipping DLL addition.")
        log_action("EXE Converter: No DLL folder found.")

    safe_input("Press Enter to return to main menu...")

# ------------------ Linkvertise Bypass ------------------
def linkvertise_bypass():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("Linkvertise Bypass")
    url = safe_input(Fore.YELLOW + "Enter Linkvertise URL: ").strip()
    if url == "":
        return
    if not url.startswith("http"):
        print(Fore.RED + "Error: Please enter a valid URL.")
        log_action("Linkvertise Bypass: Invalid URL provided.")
        safe_input("Press Enter to return to main menu...")
        return

    pattern = r'https?://(?:www\.)?linkvertise\.com/(?:[^/]+/)*([0-9a-zA-Z_-]+)'
    match = re.search(pattern, url)
    if not match:
        print(Fore.RED + "Error: Could not extract a valid link ID from the URL.")
        log_action("Linkvertise Bypass: Could not extract link ID from URL: " + url)
        safe_input("Press Enter to return to main menu...")
        return

    link_id = match.group(1)
    api_url = f"https://publisher.linkvertise.com/api/v1/redirect/link/static/{link_id}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            target_url = data.get("data", {}).get("target_url")
            if target_url:
                print(Fore.GREEN + f"Bypassed URL: {target_url}")
                log_action(f"Linkvertise Bypass: Successfully bypassed URL. Result: {target_url}")
            else:
                print(Fore.RED + "Error: Target URL not found in API response.")
                log_action("Linkvertise Bypass: Target URL not found in API response.")
        else:
            print(Fore.RED + f"Error: API returned status code {response.status_code}")
            log_action(f"Linkvertise Bypass: API returned status code {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        log_action("Linkvertise Bypass: Exception occurred: " + str(e))
    
    safe_input("Press Enter to return to main menu...")

# ------------------ IP Tools ------------------
def ip_tools():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    while True:
        print_boxed_title("IP Tools")
        print(Fore.YELLOW + "1. Check Public IP")
        print(Fore.YELLOW + "2. Check IP Safety")
        print(Fore.YELLOW + "3. Send IP to Webhook")
        print(Fore.YELLOW + "4. Return to main menu")
        choice = safe_input(Fore.YELLOW + "Select an option (1-4): ").strip()
        if choice == "1":
            try:
                ip = requests.get("https://api.ipify.org").text
                print(Fore.GREEN + f"Your Public IP: {ip}")
                log_action("IP Tools: Checked Public IP: " + ip)
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
                log_action("IP Tools: Error checking Public IP: " + str(e))
            safe_input("Press Enter to continue...")
        elif choice == "2":
            try:
                ip = requests.get("https://api.ipify.org").text
                print(Fore.GREEN + f"Your IP ({ip}) might be exposed. Consider using a VPN or proxy for enhanced privacy.")
                log_action("IP Tools: Checked IP Safety for: " + ip)
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
                log_action("IP Tools: Error checking IP Safety: " + str(e))
            safe_input("Press Enter to continue...")
        elif choice == "3":
            try:
                ip = requests.get("https://api.ipify.org").text
                webhook_url = safe_input(Fore.YELLOW + "Enter your webhook URL: ").strip()
                if webhook_url == "":
                    safe_input("Press Enter to return to IP Tools menu...")
                    continue
                payload = {"content": f"Alert: Current public IP is {ip}"}
                response = requests.post(webhook_url, json=payload)
                if response.status_code in [200, 204]:
                    print(Fore.GREEN + "Successfully sent IP to the webhook.")
                    log_action("IP Tools: Sent IP " + ip + " to webhook.")
                else:
                    print(Fore.RED + f"Failed to send IP to webhook. Status code: {response.status_code}")
                    log_action("IP Tools: Failed to send IP to webhook. Status code: " + str(response.status_code))
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
                log_action("IP Tools: Exception sending IP to webhook: " + str(e))
            safe_input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")
            safe_input("Press Enter to continue...")

# ------------------ Free VPN Launcher ------------------
def free_vpn():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("Free VPN")
    print(Fore.YELLOW + "Opening free VPN website...")
    webbrowser.open("https://protonvpn.com/free-vpn/")
    log_action("Free VPN: Launched ProtonVPN free page.")
    safe_input("Press Enter to return to main menu...")

# ------------------ Wireshark Launcher ------------------
def launch_wireshark():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("Wireshark Launcher")
    try:
        if os.name == "nt":
            # Próba uruchomienia wireshark.exe – może być potrzebna ścieżka, jeśli nie jest w PATH
            os.startfile("wireshark.exe")
        else:
            subprocess.Popen(["wireshark"])
        print(Fore.GREEN + "Wireshark launched successfully.")
        log_action("Wireshark Launcher: Wireshark launched.")
    except Exception as e:
        print(Fore.RED + f"Error launching Wireshark: {e}")
        log_action("Wireshark Launcher: Failed to launch Wireshark: " + str(e))
    safe_input("Press Enter to return to main menu...")

# ------------------ Discord Bot Script Generator ------------------
def discord_bot_script():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("Discord Bot Script Generator")
    default_name = "discord_bot.py"
    file_name = safe_input(Fore.YELLOW + f"Enter file name for the Discord bot script (default: {default_name}): ").strip()
    if file_name == "":
        file_name = default_name

    bot_script = f"""import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {{bot.user}}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I'm a bot with AI capabilities!")

# Insert your Discord bot token below
bot.run('YOUR_DISCORD_BOT_TOKEN')
"""
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(bot_script)
        print(Fore.GREEN + f"Discord bot script created and saved as '{file_name}'.")
        log_action("Discord Bot Script: Created file " + file_name)
    except Exception as e:
        print(Fore.RED + f"Error creating file: {e}")
        log_action("Discord Bot Script: Error creating file " + file_name + ": " + str(e))
    safe_input("Press Enter to return to main menu...")

# ------------------ AI Assistant ------------------
def ai_assistant():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("AI Assistant")
    print(Fore.YELLOW + "Type 'exit' to leave the AI Assistant.")
    while True:
        user_input = safe_input(Fore.CYAN + "You: ").strip()
        if user_input.lower() == "exit":
            break
        # Prosta symulacja – echo
        response = f"You said '{user_input}'. (Simulated response)"
        print(Fore.GREEN + f"AI: {response}")
        log_action("AI Assistant: User input: " + user_input + " | Response: " + response)
    safe_input("Press Enter to return to main menu...")

# ------------------ Help & Troubleshooting ------------------
def help_menu():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("Help & Troubleshooting")
    help_text = (
        "1. EXE Files Python: Upewnij się, że podany plik .py istnieje oraz PyInstaller jest zainstalowany.\n"
        "   Jeśli konwersja nie działa, sprawdź PATH oraz folder 'dlls' (umieść w nim wymagane pliki DLL).\n"
        "2. Linkvertise Bypass: Podaj prawidłowy URL z Linkvertise.\n"
        "3. IP Tools: Pozwala sprawdzić publiczne IP, bezpieczeństwo oraz wysłać IP do webhooka.\n"
        "4. Free VPN: Otwiera stronę z darmowym VPN.\n"
        "5. Wireshark Launcher: Próbuje uruchomić Wireshark (upewnij się, że jest zainstalowany).\n"
        "6. Discord Bot Script: Generuje przykładowy skrypt bota Discorda. Podmień 'YOUR_DISCORD_BOT_TOKEN' na własny token.\n"
        "7. AI Assistant: Symulowany asystent, który odpowiada na Twoje wejścia.\n"
        "8. Open Dist Folder: Otwiera folder z wygenerowanymi plikami EXE.\n"
        "9. Download Important Files: Inicjalizuje środowisko – tworzy folder 'gerrilar tools' na pulpicie, plik logs.txt,\n"
        "   README.txt (z instrukcją zamknięcia MultiTools i ponownym uruchomieniem),\n"
        "   _xynix_credist.txt (zaszyfrowane dane) oraz przykładowy plik important.dll.\n"
    )
    print(Fore.CYAN + help_text)
    safe_input("Press Enter to return to main menu...")

# ------------------ Open Dist Folder ------------------
def open_dist_folder():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("Open Dist Folder")
    dist_path = os.path.join(os.getcwd(), "dist")
    if os.path.isdir(dist_path):
        try:
            if os.name == "nt":
                os.startfile(dist_path)
            else:
                subprocess.run(["xdg-open", dist_path])
            print(Fore.GREEN + "Opened the 'dist' folder.")
            log_action("Open Dist Folder: Opened " + dist_path)
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            log_action("Open Dist Folder: Error opening folder: " + str(e))
    else:
        print(Fore.RED + "The 'dist' folder does not exist. Convert a file first.")
        log_action("Open Dist Folder: 'dist' folder not found.")
    safe_input("Press Enter to return to main menu...")

# ------------------ Download Important Files ------------------
def download_important_files():
    global env_initialized, env_folder
    print_boxed_title("Download Important Files")
    # Utwórz folder "gerrilar tools" na pulpicie
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_folder = os.path.join(desktop_path, "gerrilar tools")
    
    try:
        os.makedirs(target_folder, exist_ok=True)
        env_folder = target_folder
        env_initialized = True
        print(Fore.GREEN + f"Created folder: {target_folder}")
        # Utwórz/wyczyść plik logs.txt
        log_file = os.path.join(target_folder, "logs.txt")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("Gerrilar Tools Logs\n")
        print(Fore.GREEN + f"Log file created: {log_file}")
        log_action("Environment initialized.")
    except Exception as e:
        print(Fore.RED + f"Error creating folder: {e}")
    
    # Utwórz plik BAT do instalacji zależności
    bat_file_path = os.path.join(target_folder, "setup_tools.bat")
    bat_content = (
        "@echo off\n"
        "echo Installing necessary packages...\n"
        "pip install pyinstaller rich requests\n"
        "echo Downloading necessary DLLs and additional files...\n"
        "REM Add commands here to download any required DLLs\n"
        "echo IMPORTANT: After running this setup, please close MultiTools and restart it.\n"
        "pause\n"
    )
    
    try:
        with open(bat_file_path, "w", encoding="utf-8") as bat_file:
            bat_file.write(bat_content)
        print(Fore.GREEN + f"Batch file created: {bat_file_path}")
        log_action("Download Important Files: Batch file created.")
    except Exception as e:
        print(Fore.RED + f"Error creating batch file: {e}")
        log_action("Download Important Files: Error creating batch file: " + str(e))
    
    # Utwórz plik README.txt z instrukcją
    readme_path = os.path.join(target_folder, "README.txt")
    readme_content = (
        "Welcome to Gerrilar Tools setup folder.\n"
        "IMPORTANT: After running the setup_tools.bat file, you must close MultiTools and restart it.\n"
        "This folder also contains important DLL files and credential files.\n"
    )
    try:
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write(readme_content)
        print(Fore.GREEN + f"README file created: {readme_path}")
        log_action("Download Important Files: README file created.")
    except Exception as e:
        print(Fore.RED + f"Error creating README file: {e}")
        log_action("Download Important Files: Error creating README file: " + str(e))
    
    # Utwórz plik _xynix_credist.txt z zaszyfrowaną treścią
    credist_path = os.path.join(target_folder, "_xynix_credist.txt")
    credist_content = "Important credentials for _xynix. Do not share these details."
    encrypted_credist = encrypt_content(credist_content)
    try:
        with open(credist_path, "w", encoding="utf-8") as credist_file:
            credist_file.write(encrypted_credist)
        print(Fore.GREEN + f"Credential file created: {credist_path}")
        log_action("Download Important Files: _xynix_credist file created.")
    except Exception as e:
        print(Fore.RED + f"Error creating credential file: {e}")
        log_action("Download Important Files: Error creating _xynix_credist file: " + str(e))
    
    # Utwórz przykładowy plik DLL (zaszyfrowany)
    dll_file_path = os.path.join(target_folder, "important.dll")
    dll_content = "This is a dummy DLL file required for operation."
    encrypted_dll = encrypt_content(dll_content)
    try:
        with open(dll_file_path, "w", encoding="utf-8") as dll_file:
            dll_file.write(encrypted_dll)
        print(Fore.GREEN + f"DLL file created: {dll_file_path}")
        log_action("Download Important Files: important.dll file created.")
    except Exception as e:
        print(Fore.RED + f"Error creating DLL file: {e}")
        log_action("Download Important Files: Error creating important.dll: " + str(e))
    
    safe_input("Press Enter to return to main menu...")

# ------------------ About ------------------
def about():
    if not require_initialized():
        safe_input("Press Enter to return to main menu...")
        return

    print_boxed_title("About")
    about_text = (
        "GERRILAR TOOLS is a multi-tools suite developed in Python.\n"
        "Features include:\n"
        " - EXE Files Python (with additional DLL support)\n"
        " - Improved Linkvertise Bypass\n"
        " - IP Tools with Webhook notifier\n"
        " - Free VPN launcher\n"
        " - Wireshark launcher\n"
        " - Discord Bot Script generator\n"
        " - AI Assistant simulation\n"
        " - Download Important Files (environment initialization, including README, DLLs, and encrypted credential file)\n\n"
        "Use responsibly."
    )
    print(Fore.CYAN + about_text)
    safe_input("Press Enter to return to main menu...")

# ------------------ Main Menu ------------------
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print_banner()
        print_boxed_title("MultiTools - Gerrilar Tools")
        print(Fore.MAGENTA + "1. EXE Files Python")
        print(Fore.MAGENTA + "2. Linkvertise Bypass")
        print(Fore.MAGENTA + "3. IP Tools")
        print(Fore.MAGENTA + "4. Free VPN")
        print(Fore.MAGENTA + "5. Wireshark Launcher")
        print(Fore.MAGENTA + "6. Discord Bot Script Generator")
        print(Fore.MAGENTA + "7. AI Assistant")
        print(Fore.MAGENTA + "8. Help & Troubleshooting")
        print(Fore.MAGENTA + "9. Open Dist Folder")
        print(Fore.MAGENTA + "10. About")
        print(Fore.MAGENTA + "11. Download Important Files (Initialize Environment)")
        print(Fore.MAGENTA + "12. Exit")
        
        choice = safe_input(Fore.YELLOW + "\nEnter your choice (1-12): ").strip()
        
        if choice == "1":
            exe_converter()
        elif choice == "2":
            linkvertise_bypass()
        elif choice == "3":
            ip_tools()
        elif choice == "4":
            free_vpn()
        elif choice == "5":
            launch_wireshark()
        elif choice == "6":
            discord_bot_script()
        elif choice == "7":
            ai_assistant()
        elif choice == "8":
            help_menu()
        elif choice == "9":
            open_dist_folder()
        elif choice == "10":
            about()
        elif choice == "11":
            download_important_files()
        elif choice == "12":
            print(Fore.CYAN + "Exiting... Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.")
            safe_input("Press Enter to continue...")

if __name__ == "__main__":
    main()
