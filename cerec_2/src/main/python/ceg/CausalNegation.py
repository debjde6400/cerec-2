from python.ceg.ICausalRelation import ICausalRelation
from typing import overload

class CausalNegation(ICausalRelation):

  #private ICausalElement origin;

  #public CausalNegation(ICausalElement origin, ICausalElement target) {
  def __init__(self, origin, target):
    super().__init__(target)
    self.origin = origin

  def getOrigin(self):
    return self.sorigin

  def setOrigin(self, origin):
    self.origin = origin

  #@Override
  def createPattern(self, sentence, extractionAlgorithmGenerator):
    patternOrigin = self.origin.createPattern(sentence, extractionAlgorithmGenerator)
    patternTarget = self.getTarget().createPattern(sentence, extractionAlgorithmGenerator)
    return CausalNegation(patternOrigin, patternTarget)

  #@Override
  def isComplete(self):
    return (self.origin is not None and self.origin.isComplete()) and (self.target is not None and self.target.isComplete())


  #@Override
  def resolvePattern(self, root):
    resolvedOrigin = self.origin.resolvePattern(root)
    resolvedTarget = self.getTarget().resolvePattern(root)
    return CausalNegation(resolvedOrigin, resolvedTarget)

  #@Override
  def equals(self, other):
    if isinstance(other, CausalNegation):
      otherImpl = other
      if(otherImpl.getOrigin().equals(self.origin) and otherImpl.getTarget().equals(self.target)):
        return True
    return False

  #@Override
  @overload
  def toString(self):
    return self.toString(False, "")

  #@Override
  @overload
  def toString(self, pattern, indent):
    if(not pattern):
      return self.origin.toString() + " -~> " + self.target.toString()

    else:
      sj = [""]

      sj.append(self.origin.toString(pattern, indent + " "))
      sj.append(indent + "negates")
      sj.append(self.getTarget().toString(pattern, indent + " "))

      return '\n'.join(sj)

