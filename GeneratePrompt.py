def GeneratePromptNew(sentences):
  prompt = f'''
  Gebruik de gegeven invoerzinnen om een voorbeeldparagraaf te genereren voor een specifieke
  NLU-taak en de bijbehorende labels te identificeren.

  Jouw uitvoer moet het volgende formaat hebben:
  Plan:
  Beschrijf in een paar zinnen hoe je de taak zult aanpakken.
  
  Paragraaf:
  Genereer een voorbeeldparagraaf op basis van de gegeven invoerzinnen.
  
  Taak:
  Specificeer de NLU-taak, kies uit: Part-Of-Speech Tagging, Named Entity Recognition, Word Sense Disambiguation, Pronoun Disambiguation, Causal Reasoning, Natural Language Inference, Sentiment Analysis, Abusive Language Detection of Question Answering. Geef alleen de taaknaam.
  
  Labels:
  Geef de alleen labels voor de gegenereerde paragraaf aan (bijv. positief/negatief sentiment, entiteitstypen)

  De 5 te gebruiken invoerzinnen zijn:
  {sentences}
  '''
  return prompt

def GeneratePromptOld(sentences):
  prompt = f'''
  Gebruik de gegeven zinnen om een voorbeeldparagraaf te maken van een NLU taak en de
  bijbehorende labels. De 5 zinnen zijn: {sentences}.
  Jouw uitvoer moet het volgende formaat hebben:
  Plan:
  Jouw plan hier.
  Paragraaf:
  Jouw alinea hier.
  Taak:
  [Alleen de NLU taaknaam hier, zonder extra informatie.]
  Labels:
  [Alleen de labels hier, zonder extra informatie.]
  '''
  return prompt