'''package jfr.cerec.pattern;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;'''
from abc import ABC, abstractmethod
#from multipledispatch import dispatch

class IConstraint(ABC):

  '''/**
   * Checks whether the constrained is fulfilled by the given fragment
   * @param fragment A given fragment
   * @return True, if the fragment fulfills the constraint
   */
  public abstract boolean isFulfilledBy(Fragment fragment);'''
  @abstractmethod
  def isFulfilledBy(self, fragment):
    pass

  '''/**
   * Checks whether the constrained is fulfilled by all given fragments
   * @param fragments A list of fragment
   * @return True, if all fragments fulfill the constraint
   */'''

  def isFulilledBy(self, fragments):
    for fragment in fragments:
      if(not self.isFulfilledBy(fragment)):
        return False

    return True


  '''/**
   * Checks whether the constrained is fulfilled by none of the given fragments
   * @param fragments A list of fragment
   * @return True, if none of the fragments fulfill the constraint
   */'''
  def isFulilledByNone(self, fragments):
    for fragment in fragments:
      if(self.isFulfilledBy(fragment)):
        return False

    return True


  '''/**
   * Generates a specification proposal to the given fragment with this constraint
   * @param fragment Structure element, where the constraint is to be placed
   * @return A specification proposal to this fragment
   */'''
  @abstractmethod
  def generateProposal(self, fragment):
    pass

  @abstractmethod
  def toString():
    pass

  @abstractmethod
  def clone():
    pass

  #@abstractmethod
  #def equals(other):
  #  pass
