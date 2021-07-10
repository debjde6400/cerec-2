from python.util.GlobalConfiguration import GlobalConfiguration
from python.pattern.ConstituentStructureElement import ConstituentStructureElement
from python.pattern.ConstituentStructure import ConstituentStructure
from python.sentence.Node import Node

'''package jfr.cerec.pattern

import jfr.cerec.sentence.Fragment
import jfr.cerec.sentence.ISentence
import jfr.cerec.sentence.Node
import jfr.cerec.util.GlobalConfiguration'''

class ConstituentStructureGenerator: #implements IStructureGenerator {

  '''/*
   * {@inheritDoc}
   */
  @Override'''
  def generateStructure(self, sentence):
    root = sentence.getRootConstituent()
    structureRoot = None

    if(GlobalConfiguration.incrementalSentenceStructure):
      structureRoot = ConstituentStructureElement(root.getTag(), root.getIndex())
    else:
      structureRoot = self.generateFullStructure(root)

    return ConstituentStructure(structureRoot)



  def generateFullStructure(self, fragment):
    structure = ConstituentStructureElement(fragment.getTag(), fragment.getIndex())

    for child in fragment.getChildren():
      if isinstance(child, Node):
        childStructure = self.generateFullStructure(child)
        if(childStructure is not None):
          structure.addChild(childStructure)

    return structure
