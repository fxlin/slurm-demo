#!/usr/bin/env python3

# collect *.err logs from /p/ in an ad hoc way 

import os
import shutil
from tqdm import tqdm

def find_and_copy_err_files(source_directory, output_file):
    # Counter for tracking progress
    file_count = 0

    # Collect all .err files to determine the total count for the progress bar
    err_files = []
    for root, dirs, files in os.walk(source_directory):
        print(f"\rSearch {root}.... found err files: %d" % len(err_files), end="")
        for file in files:
            if file.endswith(".err"):
                err_files.append(os.path.join(root, file))

    # Open the output file in write mode, or create it if it doesn't exist
    with open(output_file, 'w') as outfile:
        # Initialize the progress bar
        with tqdm(total=len(err_files), desc="Processing .err files") as pbar:
            for file_path in err_files:
                # Open each .err file and append its contents to the output file
                with open(file_path, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)
                    # Add a separator between file contents if needed
                    outfile.write("\n" + "=" * 40 + "\n")  # Optional: Separator between files

                # Increment the counter and update the progress bar
                file_count += 1
                pbar.update(1)
                print(f"Processed {file_count} files: {file_path}")

    print(f"All {file_count} .err files have been processed and copied to {output_file}.")

if __name__ == "__main__":
    # Define the source directory to search and the output file path
    
    # source_directory = "/p/lava"  # Change this to your directory
    # source_directory = "/p/citypm"  # Change this to your directory
    # source_directory = "/p/cavalier"  # Change this to your directory
    # source_directory = "/p/csd"  # Change this to your directory
    # source_directory = "/p/iterativeerror"  # Change this to your directory
    # source_directory = "/p/rosbot"
    source_directory = "/home/xl6yq/workspace-rwkv/RWKV-LM/RWKV-v5/out"
    # source_directory = "/p/pd"

    # Extract the last segment of the source directory to use as the output file name
    last_segment = os.path.basename(os.path.normpath(source_directory))
    output_file = f"./{last_segment}_err.txt"  # Change this to your output file path

    # Call the function to find .err files and copy contents
    find_and_copy_err_files(source_directory, output_file)
