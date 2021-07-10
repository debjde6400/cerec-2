from python.ceg.ICausalRelation import ICausalRelation
'''package jfr.cerec.ceg;

import java.util.StringJoiner;

import jfr.cerec.genetics.ICommandGenerator;
import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.ISentence;'''

class CausalImplication(ICausalRelation):

  def __init__(self, origin, target):
    super().__init__(target)
    self.origin = origin

  def getOrigin(self):
    return self.origin

  def setOrigin(self, origin):
    self.origin = origin

  #@Override
  def createPattern(self, sentence, extractionAlgorithmGenerator):
    patternOrigin = self.origin.createPattern(sentence, extractionAlgorithmGenerator)
    patternTarget = self.getTarget().createPattern(sentence, extractionAlgorithmGenerator)
    return CausalImplication(patternOrigin, patternTarget)

  #@Override
  def isComplete(self):
    return (self.origin is not None and self.origin.isComplete()) and (self.target is not None and self.target.isComplete())


  #@Override
  def resolvePattern(self, root):
    resolvedOrigin = self.origin.resolvePattern(root)
    resolvedTarget = self.getTarget().resolvePattern(root)
    return CausalImplication(resolvedOrigin, resolvedTarget)

  #@Override
  def __eq__(self, other):
    if isinstance(other, CausalImplication):
      if(other.getOrigin() == self.origin and other.getTarget() == self.target):
        return True

    return False
  
  def matchResolved(self, other, url):
    if isinstance(other, CausalImplication) and self.origin is not None and self.target is not None:
      #new will include changes for return types
      origin_state = self.origin.matchResolved(other.getOrigin(), url)
      #print("Origin state : ", origin_state)
      target_state = self.target.matchResolved(other.getTarget(), url)
      #print("Target state : ", target_state)
      
      if origin_state and target_state:
        return 3  # both extracted
      elif not origin_state and target_state:
        return 2  # effect extracted
      elif origin_state and not target_state:
        return 1  # cause extracted
      else:
        return 0  # none extracted and specification required

    return False
  
  def addExtractor(self, candidate, ceg, extractionAlgorithmGenerator, effect=False):
    if not effect:
      self.origin.addExtractor(candidate, ceg.getCause(), extractionAlgorithmGenerator)
    else:
      self.target.addExtractor(candidate, ceg.getEffect(), extractionAlgorithmGenerator)

  #@Override
  def toString(self, pattern, indent):
    if(not pattern):
      return str(self.origin) + " --> " + str(self.target)

    else:
      sj = ['']
      sj.append(self.origin.toString(pattern, indent + " "))
      sj.append(indent + "  CAUSING  ")
      sj.append(self.getTarget().toString(pattern, indent + " "))

      return '\n'.join(sj)

  #@Override
  def __str__(self):
    return self.toString(False, '')

