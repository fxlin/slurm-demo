import os
import argparse
from collections import defaultdict

def parse_squeue_line(line):
    # squeue format:
    # JOBID PARTITION NAME USER STATE TIME TIME_LIMI NODES NODELIST(REASON)
    fields = line.split()
    # ... only care about gpu 
    if len(fields) >= 3 and "gpu" in fields[1].lower():
        return fields[2]  # NAME is the third column
    return None

def parse_sacct_line(line):
    # sacct format:
    # JobID JobName Partition Account AllocCPUS State ExitCode
    job_name = line[13:23].strip()  # 'JobName' is generally in a fixed column range
    partition = line[23:33].strip()  # 'Partition' is generally in a fixed column range
    # only care about gpu... 
    if "gpu" in partition.lower():
        return job_name
    return None

def extract_job_names(log_file):
    job_counts = defaultdict(int)
    parsing_squeue = False
    parsing_sacct = False
    skip_section = False

    # Read the log file line by line
    with open(log_file, 'r') as file:
        for line in file:
            line = line.rstrip()
            
            if line.startswith("===== squeue"):
                parsing_squeue = True
                parsing_sacct = False
                skip_section = False
                continue

            if line.startswith("===== sacct"):
                parsing_squeue = False
                parsing_sacct = True
                skip_section = False
                continue

            if line.startswith("===== scontrol") or line.startswith("===== info"):
                skip_section = True
                continue

            if line.startswith("====="):
                skip_section = False
                parsing_squeue = False
                parsing_sacct = False
                continue

            if skip_section:
                continue

            if parsing_squeue:
                if line.startswith("JOBID") or line == "":
                    continue
                job_name = parse_squeue_line(line)
                if job_name:
                    job_counts[job_name] += 1

            if parsing_sacct:
                if line.startswith("JobID") or line == "":
                    continue
                job_name = parse_sacct_line(line)
                if job_name:
                    job_counts[job_name] += 1

    return job_counts

def main():
    parser = argparse.ArgumentParser(description="Process SLURM log files to extract job names and count their occurrences.")
    parser.add_argument("-d", "--directory", help="Directory containing log files (*.log) to process.")
    parser.add_argument("-i", "--input", help="Single input log file to process.")
    args = parser.parse_args()

    job_counts = defaultdict(int)

    if args.directory:
        # Process all *.log files in the given directory
        for filename in os.listdir(args.directory):
            if filename.endswith(".log"):
                file_path = os.path.join(args.directory, filename)
                file_job_counts = extract_job_names(file_path)
                for job, count in file_job_counts.items():
                    job_counts[job] += count
    elif args.input:
        # Process a single input file
        job_counts = extract_job_names(args.input)
    else:
        # Default to processing "slurm_log.txt"
        job_counts = extract_job_names("slurm_log.txt")

    # Rank job names by frequency and display the results
    sorted_job_counts = sorted(job_counts.items(), key=lambda x: x[1], reverse=True)
    total_jobs = sum(job_counts.values())
    cumulative_count = 0
    threshold_50 = 0.5 * total_jobs
    threshold_80 = 0.8 * total_jobs
    threshold_90 = 0.9 * total_jobs
    max_job_name_length = max(len(job) for job in job_counts.keys())

    print(f"{'Job Name'.ljust(max_job_name_length)}\tCount")
    print("-" * (max_job_name_length + 6))
    printed_50 = False
    printed_80 = False
    printed_90 = False

    for job, count in sorted_job_counts:
        cumulative_count += count
        print(f"{job.ljust(max_job_name_length)}\t{count}")
        if not printed_50 and cumulative_count > threshold_50:
            print("---- 50% ----")
            printed_50 = True
        if not printed_80 and cumulative_count > threshold_80:
            print("---- 80% ----")
            printed_80 = True
        if not printed_90 and cumulative_count > threshold_90:
            print("---- 90% ----")
            printed_90 = True
            break

    # Print remaining jobs if any
    for job, count in sorted_job_counts[sorted_job_counts.index((job, count)) + 1:]:
        print(f"{job.ljust(max_job_name_length)}\t{count}")

if __name__ == "__main__":
    main()
