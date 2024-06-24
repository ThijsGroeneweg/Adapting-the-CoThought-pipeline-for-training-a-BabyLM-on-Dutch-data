import subprocess
import time
import argparse

# Commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('--issmall', type=bool, default=False, help='Use random 1/8 of the data to process')
parser.add_argument('--useOldPrompt', type=bool, default=False, help='Use random 1/8 of the data to process')


def run_batch_scripts(filePath, numLines):
    # Define the list of google server names
    server_names = [
        "us-central1",
        "asia-east1",
        "asia-east2",
        "asia-northeast1",
        "asia-northeast3",
        "asia-south1",
        "asia-southeast1",
        "australia-southeast1",
        "europe-central2",
        "europe-north1",
        "europe-southwest1",
        "europe-west1",
        "europe-west2",
        "europe-west3",
        "europe-west4",
        "europe-west6",
        "europe-west8",
        "europe-west9",
        "us-east1",
        "us-east4",
        "us-south1",
        "us-west1",
        "us-west4"
    ]

    useRandomData = input("Use random 1/8 of the data to process? (y/n): ")
    if useRandomData.lower() == "y":
        useRandomData = True
    else:
        useRandomData = False

    useNewPrompt = input("Use new prompt? (y/n): ")
    if useNewPrompt.lower() == "y":
        useNewPrompt = True
    else:
        useNewPrompt = False
    
    googleCloudProjectID = input("Enter your Google Cloud Project ID: ")

    numServers = len(server_names)
    linesPerServer = numLines // numServers

    processes = []
    for i, location in enumerate(server_names, start=1):
        start_index = (i - 1) * linesPerServer
        end_index = min(i * linesPerServer, numLines)
        command = ["python", "GenerateNLUTasksGemini.py", str(start_index), str(end_index), location, f"Chisor_NLU_{i}", filePath, googleCloudProjectID]
        if not useNewPrompt:
            command.extend(["--useOldPrompt", "True"])
        if useRandomData:
            command.extend(["--isSmall", "True"])
        processes.append(subprocess.Popen(command))

        time.sleep(30)
    
    # Wait for all processes to finish
    for p in processes:
        p.wait()
        
def getNumLines(file_path):
    numLines = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        while file.readline():
            numLines += 1
    return numLines

if __name__ == "__main__":
    filePath = input("Enter the file path: ")
    numLines = getNumLines(filePath)

    run_batch_scripts(filePath, numLines)
