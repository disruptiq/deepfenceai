import json
import os
import subprocess
import shutil
import sys
import pathlib
import webbrowser
import threading
import concurrent.futures
import time

from src.ascii_art import print_ascii_art, Fore, Style

print_lock = threading.Lock()

def clone_repo(repo_url, dest_folder):
    """Clone or update a GitHub repository in the specified folder."""
    try:
        if os.path.exists(dest_folder):
            # Assume it's a git repo, pull updates
            result = subprocess.run(['git', 'pull'], cwd=dest_folder, capture_output=True, text=True, check=True)
            with print_lock:
                print(f"{Fore.CYAN}Updated {repo_url} in {dest_folder}{Style.RESET_ALL}")
                if result.stdout:
                    print(result.stdout.rstrip())
                if result.stderr:
                    print(result.stderr.rstrip())
        else:
            result = subprocess.run(['git', 'clone', repo_url, dest_folder], capture_output=True, text=True, check=True)
            with print_lock:
                print(f"{Fore.GREEN}Cloned {repo_url} to {dest_folder}{Style.RESET_ALL}")
                if result.stdout:
                    print(result.stdout.rstrip())
                if result.stderr:
                    print(result.stderr.rstrip())
    except subprocess.CalledProcessError as e:
        with print_lock:
            print(f"{Fore.RED}Failed to clone/update {repo_url}: {e}{Style.RESET_ALL}")
            if e.stdout:
                print(e.stdout.rstrip())
            if e.stderr:
                print(e.stderr.rstrip())

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
                print(f"{Fore.BLUE}Collected output from {agent_name} to {dest}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}output.json not found in {agent_folder}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to run {agent_name}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}main.py not found in {agent_folder}{Style.RESET_ALL}")

def run_reporter_agent(agent_folder, agent_name, outputs_folder):
    """Run the reporter agent and collect its output files."""
    main_py = os.path.join(agent_folder, 'main.py')
    if os.path.exists(main_py):
        try:
            subprocess.run(['python', 'main.py', os.path.abspath(outputs_folder)], cwd=agent_folder, check=True)
            # Check for output.json first
            output_json = os.path.join(agent_folder, 'output.json')
            if os.path.exists(output_json):
                dest = os.path.join(outputs_folder, f"{agent_name}_output.json")
                shutil.copy(output_json, dest)
                print(f"{Fore.CYAN}Collected JSON output from {agent_name} to {dest}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}output.json not found in {agent_folder}{Style.RESET_ALL}")

            # Check for output.html
            output_html = os.path.join(agent_folder, 'output.html')
            if os.path.exists(output_html):
                dest = os.path.join(outputs_folder, f"{agent_name}_report.html")
                shutil.copy(output_html, dest)
                print(f"{Fore.MAGENTA}Collected HTML report from {agent_name} to {dest}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}output.html not found in {agent_folder}{Style.RESET_ALL}")

            # Also check for output directory like organizers
            reporter_output_dir = os.path.join(agent_folder, 'output')
            if os.path.exists(reporter_output_dir):
                agent_output_dir = os.path.join(outputs_folder, agent_name)
                os.makedirs(agent_output_dir, exist_ok=True)
                for file in os.listdir(reporter_output_dir):
                    src = os.path.join(reporter_output_dir, file)
                    dest = os.path.join(agent_output_dir, file)
                    if os.path.isdir(src):
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy(src, dest)
                    print(f"{Fore.LIGHTCYAN_EX}Collected {file} from {agent_name} to {dest}{Style.RESET_ALL}")

            # # Copy the entirety of the reporter agent repo to the collected reports area
            # collected_reports_dir = os.path.join(outputs_folder, 'reporter_reports')
            # shutil.copytree(agent_folder, collected_reports_dir, dirs_exist_ok=True)
            # print(f"{Fore.GREEN}Copied entire reporter agent repo to collected reports area: {collected_reports_dir}{Style.RESET_ALL}")

            # Ensure reporter collected reports dir exists
            collected_reports_dir = os.path.join(outputs_folder, 'reporter')
            os.makedirs(collected_reports_dir, exist_ok=True)

            # Copy topological graph from mapper-agent to reporter outputs
            src_topo = os.path.join(outputs_folder, 'mapper-agent', 'topological-graph-output.json')
            dst_topo = os.path.join(collected_reports_dir, 'reports', 'topological-graph-output.json')
            if os.path.exists(src_topo):
                try:
                    shutil.copy2(src_topo, dst_topo)
                    print(f"{Fore.GREEN}Copied topological graph to {dst_topo}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Failed to copy topological graph: {e}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Source topological graph not found at {src_topo}{Style.RESET_ALL}")

            # Recursively find the HTML document in that dir and open it
            html_files = [p for p in pathlib.Path(collected_reports_dir).rglob('*.html') if p.name.lower() == 'cybersecurity-report.html']
            if html_files:
                html_file = str(html_files[0])  # Take the first one
                print(f"{Fore.BLUE}HTML report available at: {html_file}{Style.RESET_ALL}")
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(html_file)
                        print(f"{Fore.BLUE}Opened HTML report in default application.{Style.RESET_ALL}")
                    else:
                        webbrowser.open(html_file)
                        print(f"{Fore.BLUE}Opened HTML report in web browser.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}Unable to open HTML report automatically (likely no GUI available): {e}. Report is available at {html_file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No HTML report found in collected reports area.{Style.RESET_ALL}")
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
                    if os.path.isdir(src):
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy(src, dest)
                    print(f"{Fore.LIGHTMAGENTA_EX}Collected {file} from {agent_name} to {dest}{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Failed to run {agent_name}: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}main.py not found in {agent_folder}{Style.RESET_ALL}")

def main():
    start_time = time.time()
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
        print(f"{Fore.MAGENTA}Archived existing outputs to {archive_dest}{Style.RESET_ALL}")

    print_ascii_art('dirs', "Setting up workspace directories...")
    # Create directories
    agents_folder = 'agents'
    os.makedirs(agents_folder, exist_ok=True)
    os.makedirs(outputs_folder, exist_ok=True)

    print_ascii_art('clone', "Fetching agent repositories...")
    clone_tasks = []
    # Collect mapper agents
    for agent in config.get('mapper_agents', []):
        name = agent['name']
        repo = agent['repo']
        dest = os.path.join(agents_folder, name)
        clone_tasks.append((repo, dest))

    # Collect organizer agents
    for agent in config.get('organizer_agents', []):
        name = agent['name']
        repo = agent['repo']
        dest = os.path.join(agents_folder, name)
        clone_tasks.append((repo, dest))

    # Collect reporter agent
    reporter = config.get('reporter_agent')
    if reporter:
        name = reporter['name']
        repo = reporter['repo']
        dest = os.path.join(agents_folder, name)
        clone_tasks.append((repo, dest))

    # Clone in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda task: clone_repo(*task), clone_tasks)

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

    elapsed_time = time.time() - start_time
    print(f"{Fore.BLUE}Total execution time: {elapsed_time:.2f} seconds{Style.RESET_ALL}")

if __name__ == '__main__':
    main()