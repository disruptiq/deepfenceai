import json
import os
import subprocess
import shutil
import sys

def clone_repo(repo_url, dest_folder):
    """Clone or update a GitHub repository in the specified folder."""
    try:
        if os.path.exists(dest_folder):
            # Assume it's a git repo, pull updates
            subprocess.run(['git', 'pull'], cwd=dest_folder, check=True)
            print(f"Updated {repo_url} in {dest_folder}")
        else:
            subprocess.run(['git', 'clone', repo_url, dest_folder], check=True)
            print(f"Cloned {repo_url} to {dest_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone/update {repo_url}: {e}")

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
                print(f"Collected output from {agent_name} to {dest}")
            else:
                print(f"output.json not found in {agent_folder}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to run {agent_name}: {e}")
    else:
        print(f"main.py not found in {agent_folder}")

def main():
    # Get param from command line
    if len(sys.argv) < 2:
        print("Usage: python main.py <param>")
        sys.exit(1)
    param = os.path.abspath(sys.argv[1])

    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Create directories
    agents_folder = 'agents'
    outputs_folder = 'outputs'
    os.makedirs(agents_folder, exist_ok=True)
    os.makedirs(outputs_folder, exist_ok=True)

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

    # Run mapper agents and collect outputs
    for agent in config.get('mapper_agents', []):
        name = agent['name']
        agent_folder = os.path.join(agents_folder, name)
        run_mapper_agent(agent_folder, name, outputs_folder, param)

if __name__ == '__main__':
    main()
