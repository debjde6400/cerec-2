#from python.ceg.ICausalElement import ICausalElement
from python.ceg.CausalPhrase import CausalPhrase
from python.util.Utils import Utils
#from typing import overload

class CausalPhrasePlaceholder:

  '''/**
   * The extractor is a specific extraction algorithm that, when applied to a sentence,
   * substitutes this placeholder by the causal phrase extracted by the extractor
   */
  private ExtractionAlgorithm extractor;'''

  def __init__(self, extractor):
    super().__init__()
    self.extractor = extractor

  #@Override

  def createPattern(self, sentence, extractionAlgorithmGenerator):
    #/ the existence of causal phrase placeholdes indicates, that this ceg is already a pattern
    return None

  #@Override
  def isComplete(self):
    return (self.extractor is not None)

  #@Override
  def resolvePattern(self, root):
    # TODO something new
    actualPhrase = None
    # extracted = self.extractor.generateCEElement(root) <old>
    # new
    extracted = []
    #print('Extracted : ', extracted)
    for e in self.extractor:
      extracted.append(e.generateCEElement(root))
    #extracted = Utils.resolvePunctuations(extracted, False)
    #extracted = Utils.resolveContractions(extracted, False)
    actualPhrase = CausalPhrase(extracted)
    actualPhrase.setGenerated(True)
    
    return actualPhrase
  
  def addExtractor(self, sentence, phrase, extractionAlgorithmGenerator):
    from python.ceg.ExtractionAlgorithm import ExtractionAlgorithm
    command = extractionAlgorithmGenerator.generateCommandPattern(sentence, phrase)
    
    if command is not None:
      extractor = ExtractionAlgorithm(command)
      self.extractor.append(extractor)

  #@Override
  def equals(self, other):
    return True

  #@Override
  def toString(self, pattern, indent):
    if(not pattern):
      return indent + "(extractor)"
    else:
      #return indent + self.extractor.toString()
      str_exts = 'EITHER OF'
      for e in self.extractor:
        str_exts = str_exts + '\n<< \n' + e.toString() + '\n>> OR'
        
      str_exts = str_exts[:-3] + '\n'
      return indent + str_exts
  
  #@Override
  def __str__(self):
    return self.toString(False, "")
