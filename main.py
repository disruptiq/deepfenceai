import json
import os
import subprocess
import shutil
import sys

try:
    import colorama
    colorama.init()
    from colorama import Fore, Back, Style
except ImportError:
    print("colorama not installed. Installing...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'colorama'], check=True)
    import colorama
    colorama.init()
    from colorama import Fore, Back, Style

def print_ascii_art(stage, message):
    """Print ASCII art for a stage with color."""
    arts = {
        'start': f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  🚀 {Fore.YELLOW}DeepFence AI - Starting the Journey{Fore.GREEN} 🚀                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'config': f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ⚙️  {Fore.CYAN}Loading Configuration{Fore.BLUE} ⚙️                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'archive': f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  📦 {Fore.RED}Archiving Previous Outputs{Fore.MAGENTA} 📦                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'dirs': f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  📁 {Fore.GREEN}Preparing Directories{Fore.CYAN} 📁                                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'clone': f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  🔄 {Fore.RED}Cloning Agent Repositories{Fore.YELLOW} 🔄                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'run': f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ▶️  {Fore.BLUE}Running Agents{Fore.GREEN} ▶️                                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'mapper': f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  🗺️  {Fore.CYAN}Executing Mapper Agents{Fore.BLUE} 🗺️                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'organizer': f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  📋 {Fore.RED}Executing Organizer Agents{Fore.MAGENTA} 📋                            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'reporter': f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  📊 {Fore.GREEN}Generating Reports{Fore.CYAN} 📊                                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""",
        'complete': f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ✅ {Fore.YELLOW}All Tasks Completed Successfully{Fore.GREEN} ✅                         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    }
    art = arts.get(stage, "")
    if art:
        print(art)
    print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")

def clone_repo(repo_url, dest_folder):
    """Clone or update a GitHub repository in the specified folder."""
    try:
        if os.path.exists(dest_folder):
            # Assume it's a git repo, pull updates
            subprocess.run(['git', 'pull'], cwd=dest_folder, check=True)
            print(f"{Fore.GREEN}Updated {repo_url} in {dest_folder}{Style.RESET_ALL}")
        else:
            subprocess.run(['git', 'clone', repo_url, dest_folder], check=True)
            print(f"{Fore.GREEN}Cloned {repo_url} to {dest_folder}{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Failed to clone/update {repo_url}: {e}{Style.RESET_ALL}")

def run_mapper_agent(agent_folder, agent_name, outputs_folder, param):
    """Run the mapper agent and collect its output.json."""
    main_py = os.path.join(agent_folder, 'main.py')
    if os.path.exists(main_py):
        try:
            subprocess.run(['python', 'main.py', param], cwd=agent_folder, check=True)
            output_json = os.path.join(agent_folder, 'output.json')
            if os.path.exists(output_json):
                dest = os.path.join(outputs_folder, f"{agent_name}_output.json")
                shutil.copy(output_json, dest)
                print(f"{Fore.GREEN}Collected output from {agent_name} to {dest}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}output.json not found in {agent_folder}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to run {agent_name}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}main.py not found in {agent_folder}{Style.RESET_ALL}")

def run_reporter_agent(agent_folder, agent_name, outputs_folder):
    """Run the reporter agent and collect its output.json."""
    main_py = os.path.join(agent_folder, 'main.py')
    if os.path.exists(main_py):
        try:
            subprocess.run(['python', 'main.py'], cwd=agent_folder, check=True)
            output_json = os.path.join(agent_folder, 'output.json')
            if os.path.exists(output_json):
                dest = os.path.join(outputs_folder, f"{agent_name}_output.json")
                shutil.copy(output_json, dest)
                print(f"{Fore.GREEN}Collected output from {agent_name} to {dest}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}output.json not found in {agent_folder}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to run {agent_name}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}main.py not found in {agent_folder}{Style.RESET_ALL}")

def run_organizer_agent(agent_folder, agent_name, outputs_folder, param):
    """Run the organizer agent."""
    main_py = os.path.join(agent_folder, 'main.py')
    if os.path.exists(main_py):
        try:
            subprocess.run(['python', 'main.py'], cwd=agent_folder, check=True)
            # Organizers may produce outputs in their own output dir; collect if present
            organizer_output_dir = os.path.join(agent_folder, 'output')
            if os.path.exists(organizer_output_dir):
                agent_output_dir = os.path.join(outputs_folder, agent_name)
                os.makedirs(agent_output_dir, exist_ok=True)
                for file in os.listdir(organizer_output_dir):
                    src = os.path.join(organizer_output_dir, file)
                    dest = os.path.join(agent_output_dir, file)
                    shutil.copy(src, dest)
                    print(f"{Fore.GREEN}Collected {file} from {agent_name} to {dest}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to run {agent_name}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}main.py not found in {agent_folder}{Style.RESET_ALL}")

def main():
    print_ascii_art('start', "Initializing DeepFence AI system...")

    # Get param from command line
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python main.py <param>{Style.RESET_ALL}")
        sys.exit(1)
    param = os.path.abspath(sys.argv[1])

    print_ascii_art('config', "Reading configuration settings...")
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)

    print_ascii_art('archive', "Backing up previous session outputs...")
    # Archive existing outputs if present
    archive_folder = 'archive'
    os.makedirs(archive_folder, exist_ok=True)
    outputs_folder = 'outputs'
    if os.path.exists(outputs_folder):
        # Find the next archive number
        existing_archives = [f for f in os.listdir(archive_folder) if f.startswith('output-') and f[7:].isdigit()]
        if existing_archives:
            nums = [int(f[7:]) for f in existing_archives]
            next_num = max(nums) + 1
        else:
            next_num = 1
        archive_dest = os.path.join(archive_folder, f"output-{next_num:05d}")
        shutil.move(outputs_folder, archive_dest)
        print(f"{Fore.GREEN}Archived existing outputs to {archive_dest}{Style.RESET_ALL}")

    print_ascii_art('dirs', "Setting up workspace directories...")
    # Create directories
    agents_folder = 'agents'
    os.makedirs(agents_folder, exist_ok=True)
    os.makedirs(outputs_folder, exist_ok=True)

    print_ascii_art('clone', "Fetching agent repositories...")
    # Clone mapper agents
    for agent in config.get('mapper_agents', []):
        name = agent['name']
        repo = agent['repo']
        dest = os.path.join(agents_folder, name)
        clone_repo(repo, dest)

    # Clone organizer agents
    for agent in config.get('organizer_agents', []):
        name = agent['name']
        repo = agent['repo']
        dest = os.path.join(agents_folder, name)
        clone_repo(repo, dest)

    # Clone reporter agent
    reporter = config.get('reporter_agent')
    if reporter:
        name = reporter['name']
        repo = reporter['repo']
        dest = os.path.join(agents_folder, name)
        clone_repo(repo, dest)

    print_ascii_art('mapper', "Launching mapper agents to process data...")
    # Run mapper agents and collect outputs
    for agent in config.get('mapper_agents', []):
        name = agent['name']
        agent_folder = os.path.join(agents_folder, name)
        run_mapper_agent(agent_folder, name, outputs_folder, param)

    print_ascii_art('organizer', "Organizing and structuring the processed data...")
    # Run organizer agents after mappers complete
    for agent in config.get('organizer_agents', []):
        name = agent['name']
        agent_folder = os.path.join(agents_folder, name)
        run_organizer_agent(agent_folder, name, outputs_folder, param)

    print_ascii_art('reporter', "Generating comprehensive reports...")
    # Run reporter agent after organizers complete
    if reporter:
        name = reporter['name']
        agent_folder = os.path.join(agents_folder, name)
        run_reporter_agent(agent_folder, name, outputs_folder)

    print_ascii_art('complete', "DeepFence AI processing completed!")

if __name__ == '__main__':
    main()