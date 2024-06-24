import os
import pandas as pd
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description='Calculate proportion of lines in Excel files.')
parser.add_argument('folder_path', type=str, help='The path to the folder containing the Excel files.')
parser.add_argument('total_lines', type=int, help='The total number of lines to consider for the proportion calculation.')
args = parser.parse_args()

folder_path = args.folder_path

# Get the list of files in the folder
file_list = os.listdir(folder_path)

for file_name in file_list:
  # Check if the file is an Excel file
  if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
    # Construct the file path
    file_path = os.path.join(folder_path, file_name)
    
    df = pd.read_excel(file_path)
    
    # Calculate the number of lines in the file
    num_lines = len(df) - 1

    proportion = num_lines / args.total_lines * 100
    
    # Print the result
    print(f"proportion of lines minus 1 in {file_name}: {proportion}")