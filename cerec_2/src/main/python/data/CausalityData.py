from python.ceg.CausalPhrase import CausalPhrase
from python.ceg.CausalImplication import CausalImplication
from python.ceg.CauseEffectGraph import CauseEffectGraph

'''
/**
 *
 * @author Julian Frattini
 *
 * Container class for data entries, which consists of a sentence and an optional cause-effect-graph,
 * if the sentence is causal
 */
'''

class CausalityData:
  
  def __init__(self, index, sentence, cause=None, effect=None):
    self.index = index
    self.sentence = sentence
    self.ceg = None

    if (cause is not None and effect is not None):
      causeNode = CausalPhrase(cause)
      effectNode = CausalPhrase(effect)
      graphRoot = CausalImplication(causeNode, effectNode)
      self.ceg = CauseEffectGraph(graphRoot)

  def isCausal(self):
    return self.ceg is not None

  def getSentence(self):
    return self.sentence

  def getCause(self):
    return self.ceg.getCause()

  def getEffect(self):
    return self.ceg.getEffect()

  def getCEG(self):
    return self.ceg

  #@Override
  def __str__(self):
    if(self.isCausal()):
      return "id #"+ str(self.index) + " : " + self.sentence + " (C -> R : " + self.getCause() + " -> " + self.getEffect() + ")"

    else:
      return "id #"+ str(self.index) + " : " + self.sentence + " (-- NO CEG --)"
