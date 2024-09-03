import os
import subprocess
import re
import time

from data.models import Report, AuthKeys
from data.datastore import Storage

from templates import aws_template, steampipe_config_template

from settings import (
    RESULTS_PATH,
    CONNECTIONS_PATH,
    CREDENTIALS_PATH
)

VALID_BENCHMARKS = [
    "audit_manager_control_tower",
    "cis_compute_service_v100",
    "cis_controls_v8_ig1",
    "cis_v120",
    "cis_v130",
    "cis_v140",
    "cis_v150",
    "cis_v200",
    "cis_v300",
    "cisa_cyber_essentials",
    "fedramp_low_rev_4",
    "fedramp_moderate_rev_4",
    "ffiec",
    "foundational_security",
    "gdpr",
    "gxp_21_cfr_part_11",
    "gxp_eu_annex_11",
    "hipaa_final_omnibus_security_rule_2013",
    "hipaa_security_rule_2003",
    "nist_800_171_rev_2",
    "nist_800_172",
    "nist_800_53_rev_4",
    "nist_800_53_rev_5",
    "nist_csf",
    "pci_dss_v321",
    "rbi_cyber_security",
    "rbi_itf_nbfc",
    "soc_2"
]

def validate_input(input: str):
    allowed_pattern = re.compile(r'^[\.a-zA-Z0-9_-]+$')
    if not allowed_pattern.match(input):
        raise ValueError(f"Invalid input {input}. Only alphanumeric characters, underscores, and hyphens are allowed.")

def validate_inputs(item_id: str, benchmark_name: str, search_path_prefix: str = None):
    # Define a regex pattern for allowed characters (alphanumeric, underscore, and hyphen)
    allowed_pattern = re.compile(r'^[\.a-zA-Z0-9_-/:]+$')
        
    if not allowed_pattern.match(item_id):
        raise ValueError("Invalid item_id. Only alphanumeric characters, underscores, and hyphens are allowed.")
    
    if not allowed_pattern.match(benchmark_name):
        raise ValueError("Invalid benchmark_name. Only alphanumeric characters, underscores, and hyphens are allowed.")
    
    if search_path_prefix:
        if not allowed_pattern.match(search_path_prefix):
            raise ValueError("Invalid search_path_prefix. Only alphanumeric characters, underscores, and hyphens are allowed.")
        
def write_credential_template(report: Report):
    with Storage() as s:
        auth_keys = s.get_one(AuthKeys, {'id': report.auth_key_id})
    if not auth_keys:
        raise Exception(f"Auth keys not found for id {report.auth_key_id}")

    template = aws_template.replace('<ACCOUNT_NAME>', report.id)
    template = template.replace('<ROLE_ARN>', auth_keys.role_id)
    template = template.replace('<EXTERNAL_ID>', auth_keys.external_id)

    credential_filepath = os.path.join(CREDENTIALS_PATH, "credentials")
    os.makedirs(CREDENTIALS_PATH, exist_ok=True)

    with open(credential_filepath, 'w') as f:
        f.write(template)

    return credential_filepath

def write_connection_template(report: Report):
    template = steampipe_config_template.replace('<ACCOUNT_NAME>', report.id)

    connection_filepath = os.path.join(CONNECTIONS_PATH, "aws.spc")
    os.makedirs(CONNECTIONS_PATH, exist_ok=True)

    with open(connection_filepath, 'w') as f:
        f.write(template)

    return connection_filepath

def run_benchmark(report: Report) -> tuple[bool, str]:
    # Assume our inputs are valid

    cred_file = write_credential_template(report)
    conn_file = write_connection_template(report)

    # Create the 'results' directory if it doesn't exist
    results_dir = RESULTS_PATH
    os.makedirs(results_dir, exist_ok=True)

    # Construct the output file path
    output_file = os.path.join(results_dir, f"{report.id}.html")

    powerpipe_directory = "/pp"

    # Construct the command
    command = f"powerpipe benchmark run aws_compliance.benchmark.{report.benchmark} --output html"
    command += f" --search-path-prefix aws_client_connection"
    # aws_client_connection must match the template connection name
    command += f" > {output_file}"

    try:
        subprocess.run('powerpipe benchmark list', cwd=powerpipe_directory, shell=True, check=True)
        subprocess.run(command, cwd=powerpipe_directory, shell=True, check=True)
        print(f"Benchmark results saved to {output_file}")
    except FileNotFoundError as e:
        print(f"Error running benchmark: {e}")
        with open(output_file, 'w') as f:
            f.write(f"<Title>Yay!</Title><h1>{report.benchmark}</h1>")
    except subprocess.CalledProcessError as e:
        print(f"Error running benchmark: {e}")
        with open(output_file, 'w') as f:
            f.write(f"<Title>Yay!</Title><h1>{report.benchmark}</h1>")
    

    try:
        os.remove(cred_file)
    except:
        print(f"ERROR - failed to remove credential file {cred_file}")
    try:
        os.remove(conn_file)
    except:
        print(f"ERROR - failed to remove connection file {conn_file}")


# def run_benchmark(item_id: str, benchmark_name: str, search_path_prefix: str = None):
#     # Validate inputs
#     try:
#         validate_inputs(item_id, benchmark_name, search_path_prefix)
#     except ValueError as e:
#         print(f"Input validation failed: {e}")
#         return

#     # Create the 'results' directory if it doesn't exist
#     results_dir = RESULTS_PATH
#     os.makedirs(results_dir, exist_ok=True)

#     # Construct the output file path
#     output_file = os.path.join(results_dir, f"{item_id}.html")

#     powerpipe_directory = "/pp"

#     # Construct the command
#     command = f"powerpipe benchmark run {benchmark_name} --output html"
#     if search_path_prefix:
#         command += f" --search-path-prefix {search_path_prefix}"

#     command += f" > {output_file}"

#     try:
#         time.sleep(5)
#         with open(output_file, 'w') as f:
#             f.write(f"<Title>Yay!</Title><p>{benchmark_name}</p>")
#         # subprocess.run(command, cwd=powerpipe_directory, shell=True, check=True)
#         print(f"Benchmark results saved to {output_file}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running benchmark: {e}")