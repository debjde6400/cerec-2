from abc import ABC, abstractmethod
from multipledispatch import dispatch

'''package jfr.cerec.pattern;

import java.util.ArrayList;'''

class SpecificationProposal(ABC):

  '''protected ArrayList<Integer> indexChainToRoot;

  /**
   * Type of the node which is targeted by the specificaion, which is later used to calculate
   * the precision of the specification proposal
   */
  protected String targetTag;
  '''
  @dispatch(object)
  def __init__(self, fragment):
    if(fragment is not None):
      self.setIndexChainToRoot(fragment.getIndexChain())
      self.targetTag = fragment.getTag()
    
    else:
      self.indexChainToRoot = [] # new ArrayList<Integer>();
  
  @dispatch(list, str)
  def __init__(self, indexChainToRoot, targetTag):
    self.indexChainToRoot = indexChainToRoot
    self.targetTag = targetTag

  def getIndexChainToRoot(self):
    return self.indexChainToRoot

  def setIndexChainToRoot(self, indexChainToRoot):
    self.indexChainToRoot = indexChainToRoot

  def getElement(self, root):
    return root.getStructureElementByIndexChain(self.indexChainToRoot)


  def getTargetTag(self):
    return self.targetTag


  def setTargetTag(self, targetTag):
    self.targetTag = targetTag

  '''/**
   * Calculates a precision value of the specification proposal: the higher the value, the more eligible
   * is the proposed specification for the pattern's sentence structure
   * @return The precision score of this specification proposal
   */'''
  @abstractmethod
  def getPrecision(self):
    pass

  '''/**
   * Resolves a specification proposal by identifying the desired fragment and creating a specification
   * @param root The root node of the sentence, where the specifying fragment is to be found
   * @return A list of specified structures that are created when applying the proposed specification
   */'''
  def resolveSpecificationProposal(self, root):
    pass

  '''/**
   * Generates a counterpart to this specification proposal
   * @return A specification proposal, that implies the opposite specification at the same location
   */'''
  @abstractmethod
  def getCounterpart(self):
    pass

  @abstractmethod
  def toString(self):
    pass


  def pathToString(self):
    sb = []
    #.forEach(i -> );
    for i in self.indexChainToRoot:
      sb.append(" > "+ str(i))

    sb.append("-->")

    return ' '.join(sb)
