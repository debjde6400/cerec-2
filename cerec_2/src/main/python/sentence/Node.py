from python.sentence.Fragment import Fragment
from python.util.Globals import Globals
from multipledispatch import dispatch
#from typing import overload

'''package jfr.cerec.sentence;

import java.util.ArrayList;
import java.util.StringJoiner;

import jfr.cerec.util.Globals;'''

#public class Node extends Fragment {
class Node(Fragment):

  #private ArrayList<Fragment> children;

  #public Node(String tag, String coveredText, int index) {
  def __init__(self, tag, coveredText, index):
    super().__init__(tag, coveredText, index)
    #children = new ArrayList<Fragment>();
    self.children = []

  #@Override
  def getDepth(self):
    max = 0
    for child in self.children:
      current = child.getDepth()
      if(current > max):
        max = current

    return max+1

  def addChild(self, child):
    child.setParent(self)
    self.children.append(child)

  #@Override
  def getChildren(self):
    return self.children

  #@Override
  def getChildByIndex(self, index):
    for child in self.children:
      if(child.getIndex() == index):
        return child

    return None


  #@Override
  def getPosition(self):
    return self.children[0].getPosition()

  '''/**
   * Returns only those children that have children themselves (meaning that they are relevant for the structure)
   * @return A list of all child nodes, that have child nodes themselves
   */'''
  def getParentingChildren(self):
    parenting = []

    for child in self.children:
      if(child.getChildren() != None):
        parenting.add(child)

    return parenting

  '''/**
   * {@inheritDoc}
   */'''
  #@Override
  def getAllLeafs(self):
    result = []

    for child in self.children:
      result.extend(child.getAllLeafs())

    return result

  '''/**
   * {@inheritDoc}
   */'''
  #@Override
  def getLeafByBeginIndex(self, beginIndex):
    for child in self.children:
      result = child.getLeafByBeginIndex(beginIndex)
      if(result != None):
        return result

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getLeafByAbsPos(self, apos):
    for child in self.children:
      result = child.getLeafByAbsPos(apos)
      if(result != None):
        return result

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def isParenting(self, other):
    for child in self.children:
      if(child == other):
        return True


      if(child.isParenting(other)):
        return True

    return False

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def split(self):
    return self.children

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getBy(self, byType, indicator, selected):
    if(byType and self.getTag() == indicator):
      selected.append(self)

    elif(not byType and self.getCoveredText() == indicator):
      selected.append(self)

    for child in self.children:
      child.getBy(byType, indicator, selected)

    return selected

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getLeafs(self, byType, indicator, selected):
    for child in self.children:
      child.getLeafs(byType, indicator, selected)

    return selected

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def select(self, byType, indicator, selected):
    if(byType and self.getTag() == indicator):
      selected.append(self)
      return selected
    
    elif(not byType and self.getCoveredText() == indicator):
      #print('Matched: ' + self.getCoveredText())
      selected.append(self)
      return selected

    for child in self.children:
      child.select(byType, indicator, selected)

    return selected


  '''/**
   * {@inheritDoc}
   */'''
  #@Override
  def getParentOf(self, child):
    for own_child in self.children:
      if(own_child.contains(child)):
        return own_child

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getDirectParentOf(self, child):
    for own_child in self.children:
      for grandchild in own_child.getChildren():
        if(grandchild == child):
          return own_child

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getRootGovernor(self):
    for child in self.children:
      if(child.getRootGovernor() != None):
        return child.getRootGovernor()

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  #@dispatch(object, bool, str)
  def containsByInd(self, byType, indicator):
    if(byType and self.getTag() == indicator):
      return True
    elif(not byType and self.getCoveredText() == indicator):
      return True

    for child in self.children:
      if(child.containsByInd(byType, indicator)):
        return True
    return False

  '''/**
   * {@inheritDoc}
   */'''
  #@Override
  #@overload
  #@dispatch(object)
  def contains(self, fragment):
    if(self == fragment):
      return True

    for child in self.children:
      if(child.contains(fragment)):
        return True

    return False

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getCompositionFor(self, expression):
    container = []
    if(expression in self.getCoveredText()):
      # recursively continue with child nodes
      beginIndex = self.getCoveredText().index(expression)

      for child in self.children:
        if(child.getPosition() >= beginIndex):
          container.extend(child.getCompositionFor(expression))

    elif self.getCoveredText() in expression:
      container.append(self)

    return container

  def __eq__(self, other):
    if(isinstance(other, Node)):
      oNode = other
      if(self.getTag() == other.getTag() and self.getCoveredText() == other.getCoveredText()):
        # negative-checks if children are equals
        if(len(self.children) != len(oNode.getChildren())):
          return False

        #for(int i = 0; i < children.size(); i++) {
        for i in range(len(self.children)):
          ownChild = self.children[i]
          otherChild = oNode.getChildren()[i]
          if(not ownChild == otherChild):
            return False

        # if all negative-checks pass, it must be equal
        return True


    return False


  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch()
  def toString(self):
    sb = []
    for child in self.children:
      sb.append(child.toString())
      sb.append('(' + child.getCoveredText() + ', ' + str(child.getIndex()) + ')')

    return ' '.join(sb)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch(bool, bool)
  def toString(self, structurized, dependencies):
    result = ""
    if(structurized):
      sj = []
      sj.append("(" + self.getTag() + ") { ")
      for c in self.children:
        sj.append(c.toString(True, dependencies))
      #children.forEach(c -> sj.add(c.toString(true, dependencies)));
      sj.append("} ")
      result = ' '.join(sj) #sj.toString()
    else:
      sj = [" "]
      for c in self.children:
        sj.append(c.toString(False, dependencies))
      #children.forEach(c -> );
      result = ' '.join(sj)

    #TODO refine this replacement
    #result = result.replace(" .", ".").replace(" :", ":").replace(" ,", ",").replace(" ;", ";")
    return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch(int, bool)
  def toString(self, indent, showConstituentText):
    result = Globals.getInstance().getIndentation(" ", indent)
    result = result + " (" + self.getTag()+ ")"
    if(showConstituentText):
      result = result + " " + self.getCoveredText()

    for child in self.children:
      result = result + "\n" + child.toString(indent+1, showConstituentText)

    return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch(list)
  def toString(self, highlights):
    if(highlights.contains(self)):
      sj = [" "]
      for c in self.children:
        sj.append("*" + c.toString(highlights) + "*")
      #children.forEach(c -> sj.add("*" + c.toString(highlights) + "*"));
      return ' '.join(sj)
    else:
      sj = [" "]
      for c in self.children:
        sj.add(c.toString(highlights))
      #children.forEach(c -> sj.add(c.toString(highlights)));
      return ' '.join(sj)

  '''/**
   * {@inheritDoc}
   */'''
  #@Override
  def structureToString(self, constituent):
    if(constituent):
      result = " (" + self.getTag() + ")"
      #result = self.getTag()

      sj = [" "]
      for child in self.children:
        childStructure = child.structureToString(constituent)
        if(childStructure is not None):
          sj.append(childStructure)

      childStructure = ' '.join(sj)
      if(childStructure is not None):
        result = result + "(" + childStructure + ") "
      return result
    
    else:
      return self.getRootGovernor().structureToString(constituent)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def size(self):
    result = 1

    for child in self.children:
      result = result + child.size()

    return result
