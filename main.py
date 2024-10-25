import os
import ctypes
import sys
import re
import time
import subprocess
import platform
import psutil
import win32com.client
from colorama import init, Fore, Style

# >> Initialize colorama
init()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# >> used for requests admin privileges
def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_command(command):
    os.system(command)

def run_background(command):
    subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_apache():
    run_background('c:\\swamp\\bin\\httpd\\bin\\httpd.exe -d c:\\swamp\\bin\\httpd\\')
    print(f"{Fore.GREEN}Apache started in background.{Style.RESET_ALL}")

def start_mysql():
    # mysql_command = (
    #     'c:\\swamp\\bin\\mysql\\bin\\mysqld.exe '
    #     '--datadir=c:\\swamp\\etc\\config\\mysql\\ '
    #     '--log-error=c:\\swamp\\logs\\mysql\\mysql_error.log '
    #     '--general-log=1 '
    #     '--general-log-file=c:\\swamp\\logs\\mysql\\general_query.log '
    #     '--slow-query-log=1 '
    #     '--slow-query-log-file=c:\\swamp\\logs\\mysql\\slow_query.log '
    #     '--long-query-time=2 '
    #     '--log-bin=c:\\swamp\\logs\\mysql\\binlog'
    # )

    # >> Disable query log
    mysql_command = (
        'c:\\swamp\\bin\\mysql\\bin\\mysqld.exe '
        '--datadir=c:\\swamp\\etc\\config\\mysql\\ '
        '--log-error=c:\\swamp\\logs\\mysql\\mysql_error.log '
        '--log-bin=c:\\swamp\\logs\\mysql\\binlog'
    )
    run_background(mysql_command)
    print(f"{Fore.GREEN}MySQL started in background.{Style.RESET_ALL}")

def stop_service(service_name):
    subprocess.run(f'taskkill /f /im {service_name}.exe', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{Fore.YELLOW}{service_name.capitalize()} stopped.{Style.RESET_ALL}")

def stop_apache():
    stop_service("httpd")

def stop_mysql():
    stop_service("mysqld")

def check_status():
    apache_running = os.system('tasklist | findstr httpd.exe > nul') == 0
    mysql_running = os.system('tasklist | findstr mysqld.exe > nul') == 0
    return apache_running, mysql_running

def initialize_mysql():
    print(f"{Fore.YELLOW}Initializing MySQL database...{Style.RESET_ALL}")
    mysql_data_dir = 'c:\\swamp\\etc\\config\\mysql\\'
    
    if os.listdir(mysql_data_dir):
        print(f"{Fore.RED}Warning: The MySQL data directory is not empty.{Style.RESET_ALL}")
        choice = input(f"{Fore.YELLOW}Do you want to delete existing data and reinitialize? (y/n): {Style.RESET_ALL}").lower()
        if choice != 'y':
            print(f"{Fore.YELLOW}MySQL initialization cancelled.{Style.RESET_ALL}")
            return
        
        for item in os.listdir(mysql_data_dir):
            item_path = os.path.join(mysql_data_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                subprocess.run(f'rmdir /s /q "{item_path}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Initialize MySQL
    result = subprocess.run('c:\\swamp\\bin\\mysql\\bin\\mysql_install_db.exe --datadir=c:\\swamp\\etc\\config\\mysql\\', 
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"{Fore.GREEN}MySQL database initialized successfully.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error initializing MySQL database:{Style.RESET_ALL}")
        print(result.stderr)

def extract_version(text):
    match = re.search(r'\d+(\.\d+)+', text)
    return match.group() if match else "Not found"

def get_php_version():
    result = subprocess.run('c:\\swamp\\bin\\php\\php -v', shell=True, capture_output=True, text=True)
    return extract_version(result.stdout) if result.returncode == 0 else "PHP not found"

def get_mysql_version():
    result = subprocess.run('c:\\swamp\\bin\\mysql\\bin\\mysql -V', shell=True, capture_output=True, text=True)
    return extract_version(result.stdout) if result.returncode == 0 else "MySQL not found"

def get_phpmyadmin_version():
    readme_path = 'c:\\swamp\\etc\\phpmyadmin\\README'
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
            return extract_version(content)
    except FileNotFoundError:
        return "phpMyAdmin README not found"

def get_apache_version():
    result = subprocess.run('c:\\swamp\\bin\\httpd\\bin\\httpd -v', shell=True, capture_output=True, text=True)
    return extract_version(result.stdout) if result.returncode == 0 else "Apache not found"

# >> Get windows edition
def get_windows_edition():
    wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    system = wmi.ConnectServer(".", "root\\cimv2").ExecQuery("Select * from Win32_OperatingSystem")
    for os_info in system:
        edition = os_info.Caption
        # return edition.strip()
        return re.sub(r'Microsoft\s+', '', edition).strip() # >> remove Microsoft

def get_system_info():
    os_info = f"{get_windows_edition()} ({platform.release()})"
    architecture = platform.architecture()[0]
    
    ram_info = psutil.virtual_memory()
    ram_usage = f"{round(ram_info.used / (1024 ** 3), 2)} GB / {round(ram_info.total / (1024 ** 3), 2)} GB"
    
    return os_info, architecture, ram_usage

def print_menu(apache_status, mysql_status):
    clear_screen()

    # >> get version & stats
    php_version = get_php_version()
    mysql_version = get_mysql_version()
    phpmyadmin_version = get_phpmyadmin_version()
    apache_version = get_apache_version()
    os_info, architecture, ram = get_system_info()

    print(f"Information")
    print(f"-----------------------------------------------")
    print(f"Version     : {Fore.GREEN}SWAMP v1.0.0{Fore.WHITE}")
    print(f"OS          : {Fore.GREEN}{os_info}{Fore.WHITE}")
    print(f"Arch        : {Fore.GREEN}{architecture}{Fore.WHITE}")
    print(f"Ram         : {Fore.GREEN}{ram}{Fore.WHITE}")
    print(f"Apache      : {Fore.GREEN}{apache_version}{Fore.WHITE}")
    print(f"MySQL       : {Fore.GREEN}{mysql_version}{Fore.WHITE}")
    print(f"PHP         : {Fore.GREEN}{php_version}{Fore.WHITE}")
    print(f"PhpMyAdmin  : {Fore.GREEN}{phpmyadmin_version}{Fore.WHITE}")
    print(f"")
    print(f"Service status")
    print(f"-----------------------------------------------")
    print(f"Apache: {Fore.GREEN if apache_status else Fore.RED}{'Running' if apache_status else 'Stopped'}{Style.RESET_ALL}")
    print(f"MySQL:  {Fore.GREEN if mysql_status else Fore.RED}{'Running' if mysql_status else 'Stopped'}{Style.RESET_ALL}")
    print(f"")
    print(f"SWAMP Manager")
    print(f"-----------------------------------------------")
    print(f"1. {'Stop' if apache_status else 'Start'} Apache")
    print(f"2. {'Stop' if mysql_status else 'Start'} MySQL")
    print(f"3. Initialize MySQL Database")
    print(f"x. Exit")

def main_menu():
    while True:
        apache_status, mysql_status = check_status()
        print_menu(apache_status, mysql_status)
        
        choice = input(f"\n{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
        
        if choice == '1':
            if apache_status:
                stop_apache()
            else:
                start_apache()
        elif choice == '2':
            if mysql_status:
                stop_mysql()
            else:
                start_mysql()
        elif choice == '3':
            initialize_mysql()
        elif choice == 'x' or choice == 'X':
            print(f"\n{Fore.YELLOW}Stopping services...{Style.RESET_ALL}")
            stop_apache()
            stop_mysql()
            print(f"{Fore.GREEN}Bye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        
        time.sleep(1)

if __name__ == "__main__":
    if not is_admin():
        print(f"{Fore.YELLOW}Requesting administrator privileges...{Style.RESET_ALL}")
        run_as_admin()
    else:
        main_menu()
