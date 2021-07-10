import python.pattern.SpecificationProposal as SpecificationProposal

'''package jfr.cerec.pattern;

import java.util.ArrayList;
import java.util.StringJoiner;

import jfr.cerec.util.CELogger;
'''

class StructuralSpecificationProposal(SpecificationProposal.SpecificationProposal):

  '''/**
   * One or more tags, where each tag will result in a unique clone of a given structure
   * with the respective tag at the given position (determined by the indexChainToRoot)
   */
  private ArrayList<String> specificationTags;

  /**
   * Index position, where the tag is to be placed
   */
  private int specificationIndex;

  /**
   * Tag of the intruder: this can be used, when the intruding sentence is also causal
   * and the intruder requires a pattern structure on its own
   */
  private String intruderTag;

  /**
   * When creating new dependency structure elements, the position of the corresponding leaf node
   * (index of the leaf in the sentence) is used for ordering dependency structures graphically
   */
  private int position;

  /**
   * Static code that can be used as a specification or intruder tag, which will result in creating
   * no structure node at the given position. This results in the clone of the structure being exactly
   * the same and is only applicable in combination with other specification tags
   */'''

  NO_TAG_APPLICABLE = "no_tag_applicable"

  #public StructuralSpecificationProposal(IStructureElement root, String specificationTag, String intruderTag, int specificationIndex) {
  def __init__(self, root, specificationTag_s, intruderTag, specificationIndex):
    super().__init__(root)
    #super(root)
    if type(specificationTag_s).__name__ == 'list':
      self.specificationTags = specificationTag_s
    else:
      self.specificationTags = [ specificationTag_s ]

    self.specificationIndex = specificationIndex
    self.intruderTag = intruderTag

  '''public StructuralSpecificationProposal(IStructureElement root, ArrayList<String> specificationTags, String intruderTag, int specificationIndex) {
    super(root);
    this.specificationTags = specificationTags;
    this.specificationIndex = specificationIndex;
    this.intruderTag = intruderTag;
  }'''

  #@Override
  def getPrecision(self):
    # TODO Auto-generated method stub
    return 1

  #@Override
  def resolveSpecificationProposal(self, originalStructure):
    import python.pattern.DependencyStructureElement as DependencyStructureElement
    import python.pattern.ConstituentStructureElement as ConstituentStructureElement
    import python.pattern.DependencyStructure as DependencyStructure
    import python.pattern.ConstituentStructure as ConstituentStructure
    resultingStructureRoots = []

    # create one resulting structure for each proposed specification tag
    for specificationTag in self.specificationTags:
      specifiedRoot = originalStructure.getRoot().clone()

      # if the specification tag is NO_TAG_APPLICABLE, do not change the original structure
      #if(!specificationTag.contentEquals(NO_TAG_APPLICABLE)) {
      if specificationTag is not StructuralSpecificationProposal.NO_TAG_APPLICABLE:
        # identify the target node, where the specification will be added
        target = self.getElement(specifiedRoot)

        if(target is not None):
          specificator = None
          # create a specificator depending on the type of structure
          if isinstance(specifiedRoot, DependencyStructureElement.DependencyStructureElement):
            specificator =  DependencyStructureElement.DependencyStructureElement(specificationTag, self.specificationIndex)
            specificator.setPosition(self.position)
          else:
            specificator =  ConstituentStructureElement.ConstituentStructureElement(specificationTag, self.specificationIndex)

          # add the specificator to the target node
          target.addChild(specificator, self.specificationIndex)

          # add the resulting specified structure to the list of resulting structures
          specifiedStructure = None
          if isinstance(specifiedRoot, DependencyStructureElement.DependencyStructureElement):
            specifiedStructure =  DependencyStructure.DependencyStructure(specifiedRoot)
          else:
            specifiedStructure =  ConstituentStructure.ConstituentStructure(specifiedRoot)

          resultingStructureRoots.append(specifiedStructure)
        else:
          print("Could not get the target element of the structural specification proposal")
          print("Current structure: " + specifiedRoot.toString())
          print("Index chain from target to root: " + str(self.getIndexChainToRoot()))

    return resultingStructureRoots


  def getSpecificationTags(self):
    return self.specificationTags


  def setSpecificationTag(self, specificationTags):
    self.specificationTags = specificationTags


  def getSpecificationIndex(self):
    return self.specificationIndex


  def setSpecificationIndex(self, specificationIndex):
    self.specificationIndex = specificationIndex


  def getPosition(self):
    return self.position


  def setPosition(self, position):
    self.position = position

  #@Override
  def getCounterpart(self):
    counterpart = StructuralSpecificationProposal(None, self.intruderTag, StructuralSpecificationProposal.NO_TAG_APPLICABLE, self.specificationIndex)
    counterpart.setIndexChainToRoot(self.getIndexChainToRoot())
    counterpart.setTargetTag(self.getTargetTag())
    return counterpart

  #@Override
  def toString(self):
    result = self.pathToString()
    sj = [""]
    for t in self.specificationTags:
      sj.append(t)
    result = result + " '" + ''.join(sj) + "' at #" + str(self.specificationIndex) + " with prec: " + str(self.getPrecision())

    return result
