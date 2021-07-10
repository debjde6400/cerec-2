'''package jfr.cerec.genetics;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;'''
from python.genetics.DependencyCommand import DependencyCommand

class DependencyCommandMultiSelect(DependencyCommand):

  #public ArrayList<DependencyCommand> selectors;

  #public DependencyCommandMultiSelect() {
  def __init__(self):
    super().__init__(None)
    self.selectors = []

  #@Override
  def extractLeafs(self, fragment):
    result = []

    for selector in self.selectors:
      foundPhrase = selector.extractLeafs(fragment)

      if(foundPhrase is not None and not len(foundPhrase) > 0):
        result.extend(foundPhrase)
      else:
        print("At least one select-command in a multi-select did not yield any result")
        print(" Current fragment: " + fragment.getCoveredText())
        print(" Fragment structure: " + fragment.structureToString(False))
        print(" Invoked command: " + selector.toString())

    return result

  def addSelector(self, selector):
    self.selectors.append(selector)

  #@Override
  def toString(self):
    sb = []

    sb.append("multiselect")
    for command in self.selectors:
      sb.append("\n  |--> " + command.toString())

    return ''.join(sb)
