import argparse
import time
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor

totalLinesTranslated = 0
parser = argparse.ArgumentParser(description='Translate a dataset.')
parser.add_argument('dataset', type=str, help='The name of the dataset to translate.')
args = parser.parse_args()

def translate_line(args):
    line, sourceLanguage, targetLanguage, startTime, totalLines = args
    global totalLinesTranslated

    translator = GoogleTranslator(source=sourceLanguage, target=targetLanguage)  
    totalLinesTranslated += 1
    currentTime = time.time()
    averageTimePerLine = (currentTime - startTime) / totalLinesTranslated
    timeRemaining = (totalLines - totalLinesTranslated) * averageTimePerLine
    print(f'Line {totalLinesTranslated}/{totalLines} - Time remaining: {timeRemaining / 60} minutes')

    try:
        translated_text = translator.translate(line)
    except Exception as e:
        print(f"Error translating line: {e}")
        translated_text = ""

    return translated_text

def TranslateFile(inputFile, outputFile, sourceLanguage, targetLanguage):
    with open(inputFile, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    totalLines = len(lines)
    startTime = time.time()
    
    numThreads = 5
    with ThreadPoolExecutor(max_workers=numThreads) as executor:
        translatedLines = list(executor.map(translate_line, [(line, sourceLanguage, targetLanguage, startTime, totalLines) for line in lines]))

    endTime = time.time()
    totalTime = endTime - startTime
    print(f'Total translation time: {totalTime / 60} minutes')

    with open(outputFile, 'w', encoding='utf-8') as file:
        for line in translatedLines:
            try:
                file.write(line + '\n')
            except Exception as e:
                print(f"Error writing line: {e}")

if __name__ == '__main__':
    inputFile = 'datasets/' + args.dataset + '.train'
    TranslateFile(inputFile, 'Translated_datasets/' + args.dataset + '_translatedOutput.txt', 'en', 'nl')