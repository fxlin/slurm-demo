# #!/bin/bash

# /bigtemp/cqx3bu/rivanna_10_15
# my dir 
# DEST_DIR="/bigtemp/xl6yq/rivanna_10_15"

SOURCE_DIR="/bigtemp/cqx3bu/rivanna_10_15"
DEST_DIR="/bigtemp/xl6yq/rivanna_10_15"

NFILES=100

MAX_SIZE=$((100 * 1024 * 1024))  # 100MB in bytes

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# List and sort files by timestamp
files=($(ls "$SOURCE_DIR" | sort))

total_size=0
selected_files=()

# Calculate the interval for uniform sampling
interval=$(( ${#files[@]} / NFILES ))

# Select files uniformly in time
for (( i=0; i<${#files[@]}; i+=interval )); do
    file="${files[$i]}"
    file_size=$(stat -c%s "$SOURCE_DIR/$file")
    
    if (( total_size + file_size > MAX_SIZE )); then
        break
    fi
    
    selected_files+=("$file")
    total_size=$((total_size + file_size))
done

# Copy selected files to the destination directory
for file in "${selected_files[@]}"; do
    cp "$SOURCE_DIR/$file" "$DEST_DIR"
done

echo "Total number of files in source directory: ${#files[@]}"
echo "Copied ${#selected_files[@]} files to $DEST_DIR, total size: $((total_size / 1024 / 1024)) MB"

