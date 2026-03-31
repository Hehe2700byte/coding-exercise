#!/usr/bin/env python3
"""
Auto-tester for Pentago game.
Compares outputs from q3.py and q3sample with sample input files.
"""

import os
import subprocess
import sys
from pathlib import Path


def get_input_files(input_dir):
    """Get all input files from the input directory, sorted by name."""
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found!")
        return []
    
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    return sorted(input_files)


def extract_serial_number(filename):
    """
    Extract a unique serial identifier from filename.
    E.g., 'pentago-10x10-input1.txt' -> '10x10-1'
          'pentago-8x8-input1.txt' -> '8x8-1'
          'pentago-6x6-input3.txt' -> '6x6-3'
    """
    # Remove .txt extension
    name_without_ext = filename.replace('.txt', '')
    # Split by '-' to extract board size and input number
    # Format: pentago-NxN-inputX
    parts = name_without_ext.split('-')
    if len(parts) >= 3:
        board_size = parts[1]  # NxN
        input_num = parts[2].replace('input', '')  # X
        return f"{board_size}-{input_num}"
    return "unknown"


def run_game(game_file, input_file, output_file):
    """Run a game with given input file and save output to output_file."""
    try:
        with open(input_file, 'r') as infile:
            with open(output_file, 'w') as outfile:
                result = subprocess.run(
                    [sys.executable, game_file],
                    stdin=infile,
                    stdout=outfile,
                    stderr=subprocess.STDOUT,
                    timeout=30
                )
        return True, None
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def run_executable(executable_path, input_file, output_file):
    """Run an executable with given input file and save output to output_file."""
    try:
        with open(input_file, 'r') as infile:
            with open(output_file, 'w') as outfile:
                result = subprocess.run(
                    [executable_path],
                    stdin=infile,
                    stdout=outfile,
                    stderr=subprocess.STDOUT,
                    timeout=30
                )
        return True, None
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def compare_files(file1, file2):
    """Compare two files and return True if they are identical."""
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            return f1.read() == f2.read()
    except Exception as e:
        print(f"Error comparing files: {e}")
        return False


def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    input_dir = os.path.join(script_dir, "q3_sample_inputs")
    tested_dir = os.path.join(script_dir, "tested")
    q3_py = os.path.join(script_dir, "q3.py")
    q3sample_exe = os.path.join(script_dir, "q3sample")
    
    # Verify paths exist
    if not os.path.isfile(q3_py):
        print(f"Error: q3.py not found at {q3_py}")
        sys.exit(1)
    
    if not os.path.isfile(q3sample_exe):
        print(f"Error: q3sample executable not found at {q3sample_exe}")
        sys.exit(1)
    
    if not os.path.isdir(tested_dir):
        os.makedirs(tested_dir)
        print(f"Created tested directory at {tested_dir}")
    
    # Get input files
    input_files = get_input_files(input_dir)
    if not input_files:
        print("No input files found!")
        sys.exit(1)
    
    print(f"Found {len(input_files)} input files")
    print()
    
    # Process each input file
    all_passed = True
    for input_file in input_files:
        serial_num = extract_serial_number(input_file)
        input_path = os.path.join(input_dir, input_file)
        
        # Output file paths
        your_output = os.path.join(tested_dir, f"your-output{serial_num}.txt")
        sample_output = os.path.join(tested_dir, f"sample-output{serial_num}.txt")
        
        print(f"Processing input{serial_num}:")
        
        # Run your q3.py
        print(f"  Running q3.py...", end=" ", flush=True)
        success, error = run_game(q3_py, input_path, your_output)
        if not success:
            print(f"FAILED ({error})")
            all_passed = False
            continue
        print("OK")
        
        # Run q3sample
        print(f"  Running q3sample...", end=" ", flush=True)
        success, error = run_executable(q3sample_exe, input_path, sample_output)
        if not success:
            print(f"FAILED ({error})")
            all_passed = False
            continue
        print("OK")
        
        # Compare outputs
        print(f"  Comparing outputs...", end=" ", flush=True)
        if compare_files(your_output, sample_output):
            print("OK")
            print(f"✓ input{serial_num} tested successfully")
        else:
            print("MISMATCH")
            print(f"✗ input{serial_num} test failed")
            all_passed = False
        
        print()
    
    # Summary
    print("-" * 50)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed. Check the output files in the 'tested' directory.")
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
