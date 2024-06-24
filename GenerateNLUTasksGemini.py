import pandas as pd
from GeneratePrompt import GeneratePromptNew, GeneratePromptOld
import time
from multiprocessing import Pool, Manager
from FilterCoherency import filterInstances
import vertexai
from vertexai.generative_models import GenerativeModel
import argparse
import random
from tqdm import tqdm

# Commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('linesfrom', type=int, help='Lines to process from')
parser.add_argument('linesuntill', type=int, help='Lines to process untill')
parser.add_argument('server', type=str, help='Server to connect to')
parser.add_argument('filename', type=str, help='what to name the file')
parser.add_argument('inputfile', type=str, help='what to use as input')
parser.add_argument('projectID', type=str, help='Google Cloud Project ID')
parser.add_argument('--isSmall', type=bool, default=False, help='Use random 1/8 of the data to process')
parser.add_argument('--useOldPrompt', type=bool, default=False, help='Use random 1/8 of the data to process')
cmdargs = parser.parse_args()

if cmdargs.useOldPrompt:
    from GeneratePrompt import GeneratePromptOld as GeneratePrompt
else:
    from GeneratePrompt import GeneratePromptNew as GeneratePrompt
from FilterCoherency import filterInstances

def GenerateResponse(i, lines, totalIterationTime, iterationsCompleted, rowLength):
    startTime = time.time()
    timeoutTime = 120
    # Initialize Vertex AI
    PROJECT_ID = cmdargs.projectID
    REGION = cmdargs.server
    vertexai.init(project=PROJECT_ID, location=REGION)
    model = GenerativeModel('gemini-1.0-pro')

    response = None  # Initialize response
    try:
        iterationStartTime = time.time()

        # Get the 5 rows as input for GeneratePrompt
        inputText = ''.join(str(line) for line in lines)

        # Generate the prompt
        prompt = GeneratePrompt(inputText)

        # Generate the prompt and get the response
        while True:
            try:
                response = model.generate_content(prompt).text
                break  # If the operation is successful, break the loop
            except Exception as e:
                print(e)
                time.sleep(60)  # If ResourceExhausted error is caught, wait for 60 seconds and retry
                if time.time() - startTime > timeoutTime:
                    print("time out time reached")
                    iterationTime = time.time() - iterationStartTime
                    totalIterationTime.value += iterationTime
                    iterationsCompleted.value += 1
                    return None

        time.sleep(3)  # Sleep for 3 second to avoid rate limiting

        filteredResponse = filterInstances(response, cmdargs.server)

        iterationTime = time.time() - iterationStartTime
        totalIterationTime.value += iterationTime
        iterationsCompleted.value += 1
        # print progress
        print(f'Current progress: {i}/{rowLength}. Total time: {(time.time() - startTime) / 60} minutes.')

    except Exception as e:
        print(f'Error at {i}: {e}')
        pass

    return filteredResponse

if __name__ == '__main__':
    startTime = time.time()
    totalIterationTime = Manager().Value('d', 0)
    iterationsCompleted = Manager().Value('i', 0)

    # Read the translated file in chunks
    with open(cmdargs.inputfile, 'r', encoding='utf-8') as file:
        rows = []
        for i, line in enumerate(file):
            if cmdargs.linesfrom <= i < cmdargs.linesuntill:
                rows.append(line)

    rowLength = len(rows)
    totalIterations = rowLength / 5

    toProcessList = []

    # Loop over the rows in groups of 5
    for i in range(0, rowLength, 5):
      toProcessList.append((i, rows[i:i+5], totalIterationTime, iterationsCompleted, rowLength))

    del rows

    # If isSmall is True, shuffle the rows and use only 1/8 of them
    if cmdargs.isSmall:
        random.shuffle(toProcessList)
        toProcessList = toProcessList[:int(len(toProcessList)/8)]

    numProcesses = 2
    # Create a pool of processes to process concurrently
    with Pool(numProcesses) as p:
        processedList = []
        with tqdm(total=len(toProcessList)) as pbar:
            for result in p.imap_unordered(GenerateResponse, toProcessList):
                processedList.append(result)
                pbar.update()

    # Calculate total time taken
    endTime = time.time()
    totalTime = endTime - startTime
    print(f'Total time taken: {totalTime} seconds')

    responses = [r for r in processedList if r is not None]

    notSaved = True
    while notSaved:
        try:
            df = pd.DataFrame(responses, columns=['Response'])
            df.to_excel("NLUFiles\\" + str(cmdargs.filename) + '.xlsx', index=False)
            notSaved = False
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(120)
