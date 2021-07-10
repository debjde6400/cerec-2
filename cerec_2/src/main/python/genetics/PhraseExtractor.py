'''package jfr.cerec.genetics;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;
import jfr.cerec.util.Constants;'''
from python.sentence.Leaf import Leaf

class PhraseExtractor: # implements ICommand {

  #public DependencyCommand extractionAlgorithm;

  #public PhraseExtractor(DependencyCommand extractionAlgorithm) {
  def __init__(self, extractionAlgorithm):
    self.extractionAlgorithm = extractionAlgorithm

  #@Override
  def generateOutput(self, fragment):
    root = None
    if isinstance(fragment, Leaf):
      root = fragment
    else:
      root = fragment.getRootGovernor()
      if(not root.getDependencyRelationType() == 'ROOT'):
        print("Cannot find the dependency root in the current fragment")
        print(" Current fragment: " + fragment.toString())
        return None

    leafs = self.extractionAlgorithm.extractLeafs(root)

    if(leafs is None):
      print("The phrase extraction did not work!");
      return ""

    #StringBuilder sb = new StringBuilder()
    sb = []
    for leaf in leafs:
      if(leaf is not None):
        sb.append(leaf.toString())
    

    return ' '.join(sb)
  

  #@Override
  def toString(self):
    return self.extractionAlgorithm.toString()