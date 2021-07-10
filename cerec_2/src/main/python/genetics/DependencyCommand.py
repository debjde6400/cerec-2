'''package jfr.cerec.genetics;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.Leaf;'''

from abc import ABC, abstractmethod
class DependencyCommand(ABC):

  #private DependencyCommand successor;

  #public DependencyCommand(DependencyCommand successor) {
  def __init__(self, successor):
    #super();
    self.successor = successor

  def getSuccessor(self):
    return self.successor

  def setSuccessor(self, successor):
    self.successor = successor

  @abstractmethod
  def extractLeafs(self, fragment):
    pass

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  @abstractmethod
  def toString(self):
    pass
