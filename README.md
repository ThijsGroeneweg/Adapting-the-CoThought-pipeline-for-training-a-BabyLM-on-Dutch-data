# Adapting the CoThought Pipeline for Training a BabyLM on Dutch Data

This repository contains the code and resources used for the thesis project titled "Adapting the CoThought pipeline for training a BabyLM on Dutch data". The project explores the adaptation of the CoThought pipeline, originally designed for English data, for use with Dutch language data.

## Overview

The CoThought pipeline (https://github.com/oooranz/Baby-CoThought) is aimed at training smaller language models (BabyLMs) with limited data. This research investigates the application of this pipeline to Dutch data by:

- Translating the English BabyLM challenge dataset into Dutch.
- Experimenting with various prompting strategies for large language models (LLMs).
- Integrating originally Dutch data into the training process.
- Using adapters, a more parameter-efficient technique, on a BERT model for fine-tuning.

The performance of the adapters was evaluated on two Natural Language Understanding (NLU) tasks: Natural Language Inference and Sentiment Analysis. The results indicate that the CoThought pipeline can be effectively adapted for Dutch data, with performance comparable to existing Dutch models, especially in Natural Language Inference.

## Resources

- **Datasets**: The generated datasets are available at https://drive.google.com/drive/folders/1EW2bgdH0OVriijsXU6JOG3fZUcjmHjbs?usp=sharing. Each dataset includes a combined excel file and separate files for each part of the BabyLM challenge dataset (https://babylm.github.io/). The folders are labeled with the models trained on the dataset.
- **Adapters**: The pretrained and fine-tuned adapters, along with various metrics calculated during training, can be found at https://drive.google.com/drive/folders/1Xa83i4y4Ut6d6NBV4W-TlLBNyx1GZZnk?usp=sharing. The folders are labeled with the models trained on the dataset.

## Setup

Before running the scripts, ensure the required packages are installed:
```
pip install -r requirements.txt
```

## Scripts
### TranslateDataset.py
This script is designed to translate the text from the BabyLM challenge dataset from English ('en') to Dutch ('nl'), using the Google Translator API. It utilizes multithreading to improve the efficiency of the translation process.

Usage:
```
python TranslateDataset.py --dataset <path_to_input_file>
```

### Finetune adapter.ipynb
This notebook is designed for fine-tuning a pre-trained BERT model with adapters for Natural Language Inference (NLI) or Sentiment Analysis.

Usage:
- The script is tailored for use in a Jupyter Notebook environment.
- It requires specifying the task (NLI or Sentiment Analysis) at the beginning of the script.
- The paths for loading and saving adapters need to be adjusted based on the environment (e.g., Google Colab or Kaggle).

### Pretrain adapter.ipynb
This notebook is designed for pre-training adapters for a BERT model for Natural Language Inference (NLI) or Sentiment Analysis.

Usage:
- The script is tailored for use in a Jupyter Notebook environment.
- The paths for loading and saving adapters need to be adjusted based on the environment (e.g., Google Colab or Kaggle).

### RunNLUGeneration.py
This script is designed for distributing the task of generating Natural Language Understanding (NLU) data across multiple Google Cloud servers using parallel processing.

Usage:
- Configure Google Cloud dependencies and Vertex AI access.
- Run the script and provide the necessary input parameters. 

### calculateProportion.py
This script calculates the proportion of lines in each Excel file within a specified folder relative to a total number of lines provided by the user. This was used to calculate the proportions of the datasets.

Usage:
```
python calculateProportion.py --folder_path <folder> --total_lines <total>
```

### CombineGeneratedNLUFiles.py
This script combines multiple Excel files from a specified folder into a single Excel file. Each Excel file's content is stacked into a single column in the combined file.

Usage:
```
python CombineGeneratedNLUFiles.py --folderPath <folder> --savePath <path_to_save_combined_file>
```

### combineSentimentAnalysisFiles.py
This script combines all the files in a specified folderinto a single Excel file. It is specific to the DRDB v3.0 dataset used in our research. It processes each file to extract its content and assigns a label ('positive', 'negative', or 'unknown') based on the subfolder it resides in. The combined data, including content and labels, is then saved into an Excel file.

Usage:
```
python combineSentimentAnalysisFiles.py --folderPath <path_to_folder> --saveFolder <path_to_save_combined_file>
```

### FilterCoherency.py
This script evaluates the coherence of text paragraphs using a language model and filters out paragraphs that do not meet a specified coherence threshold. It utilizes Vertex AI's GenerativeModel for generating coherence scores and filters paragraphs based on these scores. This script is designed to be intergrated in another script.

Usage:
This script is designed to be integrated into another script.

### GenerateNLUTasksGemini.py
This script generates responses for Natural Language Understanding (NLU) tasks using the Gemini 1.0 pro model from Vertex AI. It processes a specified range of lines from an input file, generates prompts using either a new or old prompt generation method (prompt 2 or 6 from our research), and filters the responses for coherency. The script supports parallel processing to enhance efficiency.

Usage:
This script is designed to be integrated into another script.

### GeneratePrompt.py
This script contains two functions, GeneratePromptNew and GeneratePromptOld, which are used to generate prompt 6 and prompt 2, respectively.

Usage:
This script is designed to be integrated into another script.
