'''package jfr.cerec.genetics;

import java.util.ArrayList;
import java.util.StringJoiner;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.util.CELogger;'''
from python.genetics.ConstituentCommand import ConstituentCommand
from python.genetics.NavigationStep import NavigationStep
#from typing import overload
from multipledispatch import dispatch

class ConstituentCommandNavigate(ConstituentCommand):

  #private ArrayList<NavigationStep> tagset;

  #@overload
  '''def __init__(self):
    self.tagset = []

  #public ConstituentCommandNavigate(ArrayList<NavigationStep> tagset) {'''
  def __init__(self, tagset=[]):
    super().__init__()
    self.tagset = tagset

  def getTagset(self):
    return self.tagset

  def setTagset(self, tagset):
    self.tagset = tagset
  
  @dispatch(str)
  def addTag(self, tag):
    self.tagset.append(tag)
  
  @dispatch(str, int)
  def addTag(self, tag, offset):
    self.tagset.add(NavigationStep(tag, offset))

  #@Override
  def generateOutput(self, fragment):
    # TODO problem may be here
    current = fragment
    for step in self.tagset:
      indexOfChild = step.getIndex()
      tag = step.getTag()
      nextFound = False

      index = 0
      for child in current.getChildren():
        #print(child.toString())
        if(child.getTag() == tag):
          if(index == indexOfChild):
            current = child
            #print(child.toString(True, False))
            nextFound = True
            break
          
          else:
            index += 1

      if(not nextFound):
        print("Navigation failed: " + current.getTag() + " -x-> " + tag)
        return None
      

    if(self.getSuccessor() is not None):
      return self.getSuccessor().generateOutput(current)
    
    else:
      print("No successor defined after navigate")
      return None

  #@Override
  def toString(self):
    sb = []

    sb.append("NAVIGATE from S through -> ")

    sj = [""]
    for step in self.tagset:
      if(step.getIndex() == 0):
        sj.append(step.getTag() + ' > ')
      else:
        sj.append(step.getTag() + " #" + str(step.getIndex()) + ' > ')
    
    sb.append(''.join(sj))
    sb.append(" -->")

    if(self.getSuccessor() is not None):
      sb.append(" " + self.getSuccessor().toString())
    
    else:
      print("No successor of navigation command found")

    return ' '.join(sb)