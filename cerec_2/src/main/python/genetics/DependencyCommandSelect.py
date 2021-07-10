'''package jfr.cerec.genetics;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;'''
from python.genetics.DependencyCommand import DependencyCommand
from python.sentence.Leaf import Leaf

class DependencyCommandSelect(DependencyCommand):

  '''/**
   * This option determines, how much of the given leaf node is selected
   *  - true: the whole governed phrase
   *  - false: only the covered text of the current leaf node
   */
  private boolean all;'''

  def __init__(self, all):
    super().__init__(None)
    self.all = all

  #@Override
  def extractLeafs(self, fragment):
    if(not isinstance(fragment, Leaf)):
      print("Attempting to invoke a dependency select command on a non-leaf")
      return None

    leaf = fragment
    result = []
    if(self.all):
      result.extend(leaf.getAllGoverned())
      
    else:
      result.append(leaf)
    
    return result
  

  #@Override
  def toString(self):
    if(self.all):
      return "select all governed"
    else:
      return "select covered"

