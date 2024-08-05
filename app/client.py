import os
import subprocess
import re
import time

RESULTS_PATH = os.environ['RESULTS_PATH']

def validate_inputs(item_id: str, benchmark_name: str, search_path_prefix: str = None):
    # Define a regex pattern for allowed characters (alphanumeric, underscore, and hyphen)
    allowed_pattern = re.compile(r'^[\.a-zA-Z0-9_-]+$')
        
    if not allowed_pattern.match(item_id):
        raise ValueError("Invalid item_id. Only alphanumeric characters, underscores, and hyphens are allowed.")
    
    if not allowed_pattern.match(benchmark_name):
        raise ValueError("Invalid benchmark_name. Only alphanumeric characters, underscores, and hyphens are allowed.")
    
    if search_path_prefix:
        if not allowed_pattern.match(search_path_prefix):
            raise ValueError("Invalid search_path_prefix. Only alphanumeric characters, underscores, and hyphens are allowed.")

def run_benchmark(item_id: str, benchmark_name: str, search_path_prefix: str = None):
    # Validate inputs
    try:
        validate_inputs(item_id, benchmark_name, search_path_prefix)
    except ValueError as e:
        print(f"Input validation failed: {e}")
        return

    # Create the 'results' directory if it doesn't exist
    results_dir = RESULTS_PATH
    os.makedirs(results_dir, exist_ok=True)

    # Construct the output file path
    output_file = os.path.join(results_dir, f"{item_id}.html")

    powerpipe_directory = "/pp"

    # Construct the command
    command = f"powerpipe benchmark run {benchmark_name} --output html"
    if search_path_prefix:
        command += f" --search-path-prefix {search_path_prefix}"

    command += f" > {output_file}"

    try:
        time.sleep(5)
        with open(output_file, 'w') as f:
            f.write(f"<Title>Yay!</Title><p>{benchmark_name}</p>")
        # subprocess.run(command, cwd=powerpipe_directory, shell=True, check=True)
        print(f"Benchmark results saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running benchmark: {e}")