"""This script combines all the files in a folder of the Sentiment Analysis dataset into a single Excel file."""

import os
import pandas as pd
import concurrent.futures
import argparse

def processFile(root, file):
    # Get the file path
    file_path = os.path.join(root, file)
    
    # Read the contents of the file
    with open(file_path, 'r', encoding="utf-8") as f:
        content = f.read()
    
    # Determine the label based on the subfolder
    if 'pos' in root:
        label = 'positive'
    elif 'neg' in root:
        label = 'negative'
    else:
        label = 'unknown'
    
    new_row = {'Content': content, 'Label': label}
    return pd.DataFrame([new_row])

def combineFiles(folder_path):
    df = pd.DataFrame()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(folder_path):
            # Use the executor to process files in parallel
            futures = [executor.submit(processFile, root, file) for file in files]
            
            # Collect the results as they become available
            for future in concurrent.futures.as_completed(futures):
                df = pd.concat([df, future.result()], ignore_index=True)

    df.to_excel(args.saveFolder + 'combined.xlsx', index=False)

parser = argparse.ArgumentParser(description='Combine all the files in a folder into a single Excel file.')
parser.add_argument('folderPath', type=str, help='The path of the folder to process.')
parser.add_argument('saveFolder', type=str, help='The path of the folder to save in.')

args = parser.parse_args()

combineFiles(args.folder_path)