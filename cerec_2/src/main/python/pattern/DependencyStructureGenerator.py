from python.util.GlobalConfiguration import GlobalConfiguration 
import python.pattern.DependencyStructureElement as DependencyStructureElement
'''package jfr.cerec.pattern

import jfr.cerec.sentence.ISentence
import jfr.cerec.sentence.Leaf
import jfr.cerec.util.GlobalConfiguration'''

class DependencyStructureGenerator: #implements IStructureGenerator

  '''/*
   * {@inheritDoc}
   */
  @Override'''
  def generateStructure(self, sentence):
    dependencyRoot = None

    if(GlobalConfiguration.incrementalSentenceStructure):
      # if the sentence structure is to be built incrementally, start only with the root node
      dependencyRelationType = sentence.getRootDependency().getDependencyRelationType()
      leafIndex = 0
      dependencyRoot = DependencyStructureElement(dependencyRelationType, leafIndex)
      dependencyRoot.setPosition(sentence.getRootDependency().getPosition())

    else:
      # if the sentence structure is not to be built incrementally, generate the full structure
      root = sentence.getRootDependency()
      dependencyRoot = self.generateFullStructure(root, 0)

    return dependencyRoot


  '''/**
   * Generates the root dependency structure element and triggers generation of all successive nodes recursively
   * @param current The current Leaf node from the sentence, which is parsed into a dependency structure element
   * @param index The current index of this node, which is used for better identification
   * @return The current Leaf node parsed into a dependency structure element
   */'''
  def generateFullStructure(self, current, index):
    dependencyRelationType = current.getDependencyRelationType()
    leafIndex = index
    structure = DependencyStructureElement(dependencyRelationType, leafIndex)
    structure.setPosition(current.getPosition())

    #for(int i = 0 i <  i++) {
    for i in range(current.getGoverned().size()):
      child = current.getGoverned()[i]
      structure.addChild(self.generateFullStructure(child, i))


    return structure
