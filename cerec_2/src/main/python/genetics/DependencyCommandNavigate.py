'''package jfr.cerec.genetics;

import java.util.ArrayList;
import java.util.StringJoiner;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;'''
from python.genetics.DependencyCommand import DependencyCommand
from python.sentence.Leaf import Leaf

class DependencyCommandNavigate(DependencyCommand):

  #private ArrayList<NavigationStep> tagset;

  def __init__(self):
    super().__init__(None)
    self.tagset = []

  def getTagset(self):
    return self.tagset

  def setTagset(self, tagset):
    self.tagset = tagset

  
  def addTag(self, tag, offset=None):
    self.tagset.append(tag)

  '''def addTag(String tag, int offset) {
    this.tagset.add(new NavigationStep(tag, offset));
  }'''

  #@Override
  def extractLeafs(self, fragment):
    if(not isinstance(fragment, Leaf)):
      print("Attempting to invoke a dependency navigate command on a non-leaf");
      return None

    current = fragment

    for step in self.tagset:
      positionOfGoverned = step.getIndex()
      tag = step.getTag()
      nextFound = False

      index = 0
      for governed in current.getGoverned():
        if(governed.getDependencyRelationType().contentEquals(tag)):
          if(index == positionOfGoverned):
            current = governed
            nextFound = True
            
            break
          else:
            index += 1


      if(not nextFound):
        print("Attempting to navigate through to a non-existent leaf of dependency relation type '" + tag + "'")
        return None

    if(super.getSuccessor() is not None):
      return self.getSuccessor().extractLeafs(current)
    
    else:
      print("No successor defined after navigate");
      return None

  #@Override
  def toString(self):
    sb = []

    sb.append("navigate --")

    sj = ["--"]
    for step in self.tagset:
      if(step.getIndex() == 0):
        sj.append(step.getTag())
      else:
        sj.append(step.getTag() + "#" + step.getIndex())
    
    sb.append(sj.toString())
    sb.append("-->");

    if(self.getSuccessor() is not None):
      sb.append(" " + super.getSuccessor().toString())
      
    else:
      print("No successor of navigation command found")

    return ' '.join(sb)
