import os
import pandas as pd
import argparse

# Handle command line arguments
parser = argparse.ArgumentParser(description="Combine Excel files")
parser.add_argument('folderPath', type=str, help='The path to the folder containing the Excel files')
parser.add_argument('savePath', type=str, help='The path where the combined Excel file should be saved')
args = parser.parse_args()

folderPath = args.folderPath
savePath = args.savePath
firstFile = True
fileProcessed = False

# Combine Excel files in pandas DataFrame
for root, dirs, files in os.walk(folderPath):
  for file in files:
    filePath = os.path.join(root, file)
    df_temp = pd.read_excel(filePath)
    df_temp = df_temp.stack().reset_index(drop=True).to_frame()  # Convert to single-column DataFrame
    if firstFile:
      df = df_temp
      firstFile = False
      fileProcessed = True
    else:
      df = pd.concat([df, df_temp], ignore_index=True)

# Save the combined DataFrame to an Excel file if files were processed
if fileProcessed:
    df.to_excel(savePath, index=False)
else:
    print("No files were processed. Please check the directory.")