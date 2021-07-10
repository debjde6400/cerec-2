import python.pattern.IStructureElement as IStructureElement
#from python.sentence.Fragment import Fragment
from python.sentence.Node import Node
'''package jfr.cerec.pattern

import java.util.ArrayList

import jfr.cerec.sentence.Fragment
import jfr.cerec.sentence.Node'''

class ConstituentStructureElement(IStructureElement.IStructureElement):

  #public ConstituentStructureElement(String tag, int index) {
  def __init__(self, tag, index):
    super().__init__(tag, index)


  #@Override
  def isFragmentTypeCompliant(self, fragment):
    return True

  #@Override
  def getFragmentChildrenAtIndex(self, list, index):
    fragmentChildren = []  #new ArrayList<Fragment>()

    for fragment in list:
      child = fragment.getChildByIndex(index)
      if(child is not None):
        fragmentChildren.append(child)

      else:
        return None

    return fragmentChildren

  #@Override
  def getFragmentChildAtIndex(self, intruder, index):
    return intruder.getChildByIndex(index)

  #@Override
  def getHighestIndexOfStructures(self, current):
    max = 0
    for c in current:
      if(isinstance(c, Node)):
        #print(c.toString(True, False))
        if(len(c.getChildren()) > max):
          max = len(c.getChildren())

    if(len(self.children) > max):
      max = len(self.children)

    return max


  #@Override
  def isStructureElementAtIndexUniversal(self, fragments, index):
    tag = ""
    for fragment in fragments:
      #print(len(fragment.children))
      childAtIndex = fragment.getChildByIndex(index)

      if(childAtIndex is None):
        #print('Tong')
        return False
      else:
        #print(childAtIndex.toString(True, False))
        if(not tag):
          # this is the first node under investigation - set a proposed tag value
          tag = childAtIndex.getTag()
        else:
          if(tag != childAtIndex.getTag()):
            return False

    return True

  #@Override
  def getFragmentTag(self, fragment):
    return fragment.getTag()

  #@Override
  def generateUniversalSuccessor(self, primeChild, tag, index):
    if isinstance(primeChild, Node):
      # the child nodes of all accepted sentences and the intruding sentences is equal and will be added in order to progress
      commonChild = ConstituentStructureElement(tag, index)
      self.addChild(commonChild, index)
      return commonChild

    return None


  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def clone(self):
    cl = ConstituentStructureElement(self.tag, self.index)

    for constraint in self.constraints:
      cl.addConstraint(constraint.clone())

    for child in self.children:
      #print('Cl1: ', cl.toString())
      #print('chl : ', str([p.toString() for p in cl.children]))
      # NEW!
      cl.children.append(child.clone())
      cl.children[-1].setParent(cl)
      #print('Cl2: ', cl.toString())
    
    #print('Cl3: ', cl.toString())
    return cl
