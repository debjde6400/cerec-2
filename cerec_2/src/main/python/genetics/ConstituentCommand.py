'''package jfr.cerec.genetics;

import jfr.cerec.sentence.Fragment;

/**
 * @author Julian Frattini
 *
 * Superclass of a simple version of commands. Commands can be chained together linearly via successors,
 * where the last command of each succession has to be a CommandSelect.
 */'''
from abc import ABC, abstractmethod

class ConstituentCommand(ABC):

  #protected ConstituentCommand successor;
  
  def __init__(self):
    self.successor = None

  def getSuccessor(self):
    return self.successor

  def setSuccessor(self, successor):
    self.successor = successor

  '''/**
   * Pushes a new command to the end of the line of succession
   * @param successor command, which shall be the last command of the succession
   */'''
  def chainCommand(self, successor):
    if(self.successor is None):
      self.successor = successor
    else:
      self.successor.chainCommand(successor)

  '''/**
   * Generates a reference to the last command in the succession of commands.
   * The final command has to be a 'select'-command. If not, there is an error.
   * @return The final command in the succession
   */'''
  def getFinal(self):
    if(self.successor is not None):
      return self.successor.getFinal()
    else:
      raise ValueError("Last command in the succession is not a 'SELECT'-command")

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  @abstractmethod
  def generateOutput(self, fragment):
    pass

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def toString(self):
    pass
