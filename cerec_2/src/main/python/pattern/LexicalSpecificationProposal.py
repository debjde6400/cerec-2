'''package jfr.cerec.pattern;

import java.util.ArrayList;'''
from python.pattern.SpecificationProposal import SpecificationProposal
from python.pattern.LexicalConstraint import LexicalConstraint
from python.pattern.IStructureElement import IStructureElement
from multipledispatch import dispatch

class LexicalSpecificationProposal(SpecificationProposal):

  #private LexicalConstraint lexicalConstraint;

  #public LexicalSpecificationProposal(ArrayList<Integer> indexChainToRoot, String targetTag, LexicalConstraint constraint) {
  @dispatch(list, str, object)
  def __init__(self, indexChainToRoot, targetTag, constraint):
    super().__init__(indexChainToRoot, targetTag)
    self.lexicalConstraint = constraint

  @dispatch(IStructureElement, object)
  #public LexicalSpecificationProposal(IStructureElement fragment, LexicalConstraint constraint) {
  def __init__(self, fragment, constraint):
    super().__init__(fragment)
    self.lexicalConstraint = constraint

  #public LexicalSpecificationProposal(IStructureElement fragment, String word, boolean positive) {
  @dispatch(IStructureElement, str, bool)
  def __init__(self, fragment, word, positive):
    super().__init__(fragment)
    self.lexicalConstraint = LexicalConstraint(word, positive)

  #@Override
  def getPrecision(self):
    from python.pattern.LexicalConstraintGenerator import LexicalConstraintGenerator
    precision = 0

    precision = precision + len(self.indexChainToRoot)
    for tag in LexicalConstraintGenerator.topLexicalConstraintTags:
      if(tag == self.targetTag):
        precision = precision + 5

    for word in LexicalConstraintGenerator.topLexicalConstraintWords:
      if(word == self.lexicalConstraint.getWord().lower()):
        precision = precision + 10

    return precision


  #@Override
  def resolveSpecificationProposal(self, originalStructure):
    resultingSpecifiedStructures = []
    specifiedStructure = originalStructure.clone()
    specifiedRoot = specifiedStructure.getRoot()

    element = self.getElement(specifiedRoot)

    if(element is not None):
      elementContainsConstraint = False
      for constraint in element.getConstraints():
        if(self.lexicalConstraint == constraint):
          elementContainsConstraint = True
          break

      if(not elementContainsConstraint):
        element.addConstraint(self.lexicalConstraint)

    resultingSpecifiedStructures.append(specifiedStructure)
    return resultingSpecifiedStructures

  #@Override
  def getCounterpart(self):
    counterConstraint = LexicalConstraint(self.lexicalConstraint.getWord(), not self.lexicalConstraint.isPositive())
    counterpart = LexicalSpecificationProposal(self.indexChainToRoot, self.targetTag, counterConstraint)
    return counterpart


  #@Override
  def toString(self):
    result = self.pathToString()
    result = result + " " + self.lexicalConstraint.toString() + " with prec: " + str(self.getPrecision())

    return result

