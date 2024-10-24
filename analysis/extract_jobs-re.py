import re
from collections import defaultdict

def extract_job_names(log_file):
    # Regular expressions to capture job names from 'squeue' and 'sacct'
    squeue_pattern = re.compile(r"\s+\d+\s+\S+\s+(\S+)\s+\S+\s+\S+")
    sacct_pattern = re.compile(r"^\s*\d+\S*\s+(\S+)", re.MULTILINE)

    job_counts = defaultdict(int)

    # Read the log file
    with open(log_file, 'r') as file:
        log_content = file.read()

    # Extract and count job names from squeue sections
    squeue_sections = re.findall(r"===== squeue .*?=====\n(.*?)\n\n", log_content, re.DOTALL)
    for section in squeue_sections:
        for match in squeue_pattern.findall(section):
            job_counts[match] += 1

    # Extract and count job names from sacct sections
    sacct_sections = re.findall(r"===== sacct .*?=====\n(.*?)\n\n", log_content, re.DOTALL)
    for section in sacct_sections:
        for match in sacct_pattern.findall(section):
            job_counts[match] += 1

    return job_counts

def main():
    log_file = "slurm_log.txt"  # Replace with your log file path
    job_counts = extract_job_names(log_file)

    # Display the results
    print("Job Name\tCount")
    print("-" * 20)
    for job, count in sorted(job_counts.items()):
        print(f"{job}\t{count}")

if __name__ == "__main__":
    main()
