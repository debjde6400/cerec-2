'''package jfr.cerec.genetics;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;

/**
 *
 * @author Julian Frattini
 *
 * Command for horizontal selection: pick commands traverse a sentence through the tree spanned by
 * the dependency parser. Pick commands can be executed recursively in order to reach deeper nodes of
 * the spanning tree.
 * It is defined by a dependencyType, which is the type of association between two nodes.
 */'''
from python.genetics.ConstituentCommand import ConstituentCommand
from python.sentence.Leaf import Leaf
#from typing import overload

class ConstituentCommandPick(ConstituentCommand):

  #private String dependencyType;

  # if one leaf governs multiple leafs with the same dependency type, enable an indexed picking
  #private int index;
  
  '''@overload
  def __init__(self, dependencyType):
    super().__init__()
    self.dependencyType = dependencyType
    self.index = 0'''

  #@overload
  def __init__(self, dependencyType, index=0):
    super().__init__()
    self.dependencyType = dependencyType
    self.index = index

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def generateOutput(self, fragment):
    if(not isinstance(fragment, Leaf)):
      print("Attempting to invoke a pick-command on a non-Leaf node");
      print(self.toString() + " on " + fragment.toString())
      return ""

    leaf = fragment

    # keep track of the number of occurrences of the dependency relation type
    # if one node has multiple child nodes associated to it via the same type, this count allows to distinct, which child node to select
    countOccurrencesOfDependencyType = 0

    for gov in leaf.getGoverned():
      # check for the specific dependency type
      if(gov.getDependencyRelationType() == self.dependencyType):
        # only select, if the index of the child node equals the counted occurrences of the dependency type
        if(countOccurrencesOfDependencyType == self.index):
          if(self.successor is None):
            # generate the cause-/effect-expression
            return gov.getCoveredText()
          else:
            # continue recursive traversal
            return self.successor.generateOutput(gov)
          
        else:
          countOccurrencesOfDependencyType += 1

    print("No governed leaf node found that complies the given dependency type")
    return ""

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def toString(self):
    return "pick " + self.dependencyType + ("" if self.successor is None else "->") + (self.successor.toString() if self.successor is not None else '')

