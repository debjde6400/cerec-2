'''package jfr.cerec.ceg;

import java.util.ArrayList;
import java.util.StringJoiner;

import jfr.cerec.genetics.ICommandGenerator;
import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.ISentence;'''
from python.ceg.ICausalRelation import ICausalRelation
from typing import overload

class CausalConjunction(ICausalRelation):

  #private ArrayList<ICausalElement> conjuncted;

  '''def __init__(self):
    super(null);
    conjuncted = new ArrayList<ICausalElement>();'''

  def __init__(self, conjuncted=[], output=None):
    super().__init__(output)
    self.conjuncted = conjuncted

  def getConjuncted(self):
    return self.conjuncted

  #@Override
  def createPattern(self, sentence, extractionAlgorithmGenerator):
    patternConjuncted = []
    for c in self.conjuncted:
      patternConjuncted.append(c.createPattern(sentence, extractionAlgorithmGenerator))
    patternTarget = self.getTarget().createPattern(sentence, extractionAlgorithmGenerator)
    return CausalConjunction(patternConjuncted, patternTarget)

  #@Override
  def isComplete(self):
    for element in self.conjuncted:
      if element is None:
        return False
      else:
        if(not element.isComplete()):
          return False

    return (self.target is None and self.target.isComplete())

  #@Override
  def resolvePattern(self, root):
    resolvedConjuncted = []

    for c in self.conjuncted:
      resolvedConjuncted.append(c.resolvePattern(root))
      resolvedTarget = self.getTarget().resolvePattern(root)

    return CausalConjunction(resolvedConjuncted, resolvedTarget)

  #@Override
  def equals(self, other):
    if isinstance(other, CausalConjunction):
      otherCon = other

      if(not otherCon.getTarget().equals(self.target)):
        return False

      if(otherCon.getConjuncted().size() == self.conjuncted.size()):
        for i in range(self.conjuncted.size()):
          if(not self.conjuncted[i].equals(otherCon.getConjuncted()[i])):
            return False

        return True
      else:
        return False

    return False


  #@Override
  @overload
  def toString(self):
    return self.toString(False, "");

  #@Override
  @overload
  def toString(self, pattern, indent):
    if(not pattern):
      sj = [" /\\ "]
      for c in self.conjuncted:
        sj.append(c.toString())

    result = "(" + ''.join(sj) + ")"
    if(self.getTarget() is not None):
      result = result + self.getTarget().toString()
      return result

    else:
      sj = ["\n"]

      sj.append(indent + "conjuncts")
      for c in self.conjuncted:
        sj.add(c.toString(pattern, indent + " "))

      return ''.join(sj)
