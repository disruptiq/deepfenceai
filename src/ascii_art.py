try:
    import colorama
    colorama.init()
    from colorama import Fore, Back, Style
except ImportError:
    print("colorama not installed. Installing...")
    import subprocess
    import sys
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'colorama'], check=True)
    import colorama
    colorama.init()
    from colorama import Fore, Back, Style

def print_ascii_art(stage, message):
    """Print ASCII art for a stage with color."""
    arts = {
        'start': f"""
{Fore.GREEN}+================================================================+
|                                                                |
|  [START] {Fore.YELLOW}DeepFence AI - Starting the Journey{Fore.GREEN} [START]          |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'config': f"""
{Fore.BLUE}+================================================================+
|                                                                |
|  [CONFIG] {Fore.CYAN}Loading Configuration{Fore.BLUE} [CONFIG]                      |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'archive': f"""
{Fore.MAGENTA}+================================================================+
|                                                                |
|  [ARCHIVE] {Fore.RED}Archiving Previous Outputs{Fore.MAGENTA} [ARCHIVE]                |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'dirs': f"""
{Fore.CYAN}+================================================================+
|                                                                |
|  [DIRS] {Fore.GREEN}Preparing Directories{Fore.CYAN} [DIRS]                        |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'clone': f"""
{Fore.YELLOW}+================================================================+
|                                                                |
|  [CLONE] {Fore.RED}Cloning Agent Repositories{Fore.YELLOW} [CLONE]                   |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'mapper': f"""
{Fore.BLUE}+================================================================+
|                                                                |
|  [MAPPER] {Fore.CYAN}Executing Mapper Agents{Fore.BLUE} [MAPPER]                    |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'organizer': f"""
{Fore.MAGENTA}+================================================================+
|                                                                |
|  [ORGANIZER] {Fore.RED}Executing Organizer Agents{Fore.MAGENTA} [ORGANIZER]            |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'reporter': f"""
{Fore.CYAN}+================================================================+
|                                                                |
|  [REPORTER] {Fore.GREEN}Generating Reports{Fore.CYAN} [REPORTER]                     |
|                                                                |
+================================================================+{Style.RESET_ALL}
""",
        'complete': f"""
{Fore.GREEN}+================================================================+
|                                                                |
|  [COMPLETE] {Fore.YELLOW}All Tasks Completed Successfully{Fore.GREEN} [COMPLETE]        |
|                                                                |
+================================================================+{Style.RESET_ALL}
"""
    }
    art = arts.get(stage, "")
    if art:
        print(art)
    print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")
