import time
from multiprocessing import Pool
import re
import vertexai
from vertexai.generative_models import GenerativeModel

# Define the prompt for coherence scoring
scorePrompt = '''Analyseer de volgende paragraaf, en eindig met op de laatste lijn: "Daarom is de coherentiescore {s}", waar s een integer van 1 tot 10 is.
'''

# Define the threshold for filtering
coherency_threshold = 7.0

# Function to generate response from LLM
def GenerateResponseFilter(prompt, server):
  startTime = time.time()
  timeoutTime = 100
  PROJECT_ID = "virtual-cairn-420509"
  vertexai.init(project=PROJECT_ID, location=server)
  model = GenerativeModel('gemini-1.0-pro')
  response = None  # Initialize response
  while True:
    try:
      # Generate the prompt and get the response
      response = model.generate_content(prompt).text
      break
    except Exception as e:
      print(e)
      time.sleep(60)
    if time.time() - startTime > timeoutTime:
        print("time out time reached")
        return response

  return response

# Function to evaluate coherence
def evaluateCoherence(paragraph, server):
    try:
        coherenceCompletePrompt = scorePrompt + paragraph
        response = GenerateResponseFilter(coherenceCompletePrompt, server)
    except Exception as e:
        print(e)
        response = None


    coherenceScore = 0
    try:
      reMatch = re.findall(r'coherentiescore (\d+)', response, re.IGNORECASE)
      if reMatch:
          coherenceScore = reMatch[0]
    except:
      pass
    return coherenceScore

# Function to filter instances based on coherence score
def filterInstances(instance, server):
    coherence_score = evaluateCoherence(instance, server)
    try:
      if float(coherence_score) >= coherency_threshold:
          return instance
      else:
          return None
    except:
      return None