import python.pattern.IStructureElement as IStructureElement
from python.sentence.Leaf import Leaf

'''package jfr.cerec.pattern

import java.util.ArrayList

import jfr.cerec.sentence.Fragment
import jfr.cerec.sentence.Leaf
import jfr.cerec.util.CELogger'''
         
class DependencyStructureElement(IStructureElement.IStructureElement):

  '''/**
   * Index of the corresponding leaf in the constituency tree for further ordering
   */
  private int position'''

  #public DependencyStructureElement(String  {
  def __init__(self, dependencyRelation, index):
    super().__init__(dependencyRelation, index)

  def getPosition(self):
    return self.position

  def setPosition(self, position):
    self.position = position


  #@Override
  def isFragmentTypeCompliant(self, fragment):
    return isinstance(fragment, Leaf)

  #@Override
  def getFragmentChildrenAtIndex(self, list, index):
    fragmentChildren = [] #new ArrayList<Fragment>()

    for fragment in list:
      if isinstance(fragment, Leaf):
        leaf = fragment

        child = leaf.getGoverned(index)
        if(child is not None):
          fragmentChildren.append(child)
        else:
          return None

      else:
        print("Found a non-leaf node referenced to a dependency structure element")
        return None

    return fragmentChildren

  #@Override
  def getFragmentChildAtIndex(self, intruder, index):
    if isinstance(intruder, Leaf):
      return intruder.getGoverned(index)

    return None

  #@Override
  def getHighestIndexOfStructures(self, currentLeafs):
    max = 0
    for currentFragment in currentLeafs:
      if isinstance(currentFragment, Leaf):
        current = currentFragment
        if(current.getGoverned().size() > max):
          max = current.getGoverned().size()

    if(self.children.size() > max):
      max = self.children.size()

    return max


  #@Override
  def isStructureElementAtIndexUniversal(self, currentFragments, index):
    tag = ""
    for currentFragment in currentFragments:
      if isinstance(currentFragment, Leaf):
        current = currentFragment
        childAtIndex = current.getGoverned(index)

        if(childAtIndex == None):
          return False

        else:
          if(tag.isEmpty()):
            # this is the first node under investigation - set a proposed tag value
            tag = childAtIndex.getDependencyRelationType()
          else:
            if(not tag == childAtIndex.getDependencyRelationType()):
              return False

    return True


  #@Override
  def getFragmentTag(self, fragment):
    if isinstance(fragment, Leaf):
      return fragment.getDependencyRelationType()

    return None


  #@Override
  def generateUniversalSuccessor(self, primeChild, tag, index):
    commonChild = DependencyStructureElement(tag, index)
    self.addChild(commonChild, index)
    return commonChild

  #@Override
  def clone(self):
    clone = DependencyStructureElement(self.tag, self.index)

    for constraint in self.constraints:
      clone.addConstraint(constraint.clone())

    for child in self.children:
      clone.addChild(child.clone())

    return clone
