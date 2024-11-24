#!/usr/bin/env python3

# post process a *.err file (collection of a bunch of many err files), as from collect-error-logs.py
# and dedup repeated text blocks from the file 

from rapidfuzz import fuzz
import sys

def chunk_lines(lines, chunk_size):
    """Split lines into blocks of specified chunk size."""
    for i in range(0, len(lines), chunk_size):
        yield "".join(lines[i:i + chunk_size])

def deduplicate_text_blocks(lines, min_chunk_size=2, max_chunk_size=5, threshold=90):
    unique_blocks = []

    # Iterate through a series of chunk sizes
    for chunk_size in range(min_chunk_size, max_chunk_size + 1):
        blocks = list(chunk_lines(lines, chunk_size))

        # Deduplicate blocks at the current chunk size
        for block in blocks:
            if not any(fuzz.ratio(block, ub) > threshold for ub in unique_blocks):
                unique_blocks.append(block)

    return unique_blocks

if len(sys.argv) < 2:
    print("Usage: dedup.py <logfile>")
    sys.exit(1)

logfile = sys.argv[1]

with open(logfile, "r") as f:
    lines = f.readlines()

# Deduplicate based on a series of chunk sizes from 2 to 5 lines
deduped_blocks = deduplicate_text_blocks(lines, min_chunk_size=2, max_chunk_size=5, threshold=90)

for block in deduped_blocks:
    print(block)
