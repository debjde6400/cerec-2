import json
from python.data.CausalityData import CausalityData

'''
  @author Julian Frattini

  Reader class capable of reading JSON-Files. The file must have the following structure:
   [
  {
   "sentence": "This is a causal sentence example, because it contains a causality.",
   "causality": {
    "cause": "it contains a causality",
    "effect": "This is a causal sentence example"
   }
  }, {
   "sentence": "This is a non-causal sentence example"
  }, ...
 ]
 '''

class JSONCausalityDataReader: #implements ICausalityDataReader {

  def __init__(self):
    self.examples = []
    self.initialized = False
    self.data = dict()

  def initialize(self, file):
    try:
      fr = open(file, 'r')
      self.data = json.load(fr)
      fr.close()
      self.initialized = True

    except FileNotFoundError as fnf:
      print(fnf)

  def isInitialized(self):
    return self.initialized


  def readExamples(self):
    result = []

    if(self.initialized):
      for i, exampleJSON in enumerate(self.data):
        #JSONObject exampleJSON = examples.getJSONObject(i);

        sentence = exampleJSON["sentence"]

        if("causality" in exampleJSON):
          cause = exampleJSON["causality"]["cause"]
          effect = exampleJSON["causality"]["effect"]

          example = CausalityData(i, sentence, cause, effect)

        else:
          example = CausalityData(i, sentence)

        result.append(example)

      return result