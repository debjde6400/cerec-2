from abc import ABC, abstractmethod
import python.pattern.StructuralSpecificationProposal as StructuralSpecificationProposal
from multipledispatch import dispatch

class IStructureElement(ABC):

  '''/**
   * The tag identifies the structure element, which has different meanings
   * depending on the type of structure element:
   *  - ConstituencyStructureElement: constituency type
   *  - DependencyStructureElement: dependency relation type
   */
  protected String tag

  /**
   * A list of constraints which fragments must fulfill in order to be compliant
   * to this structure element
   */
  protected ArrayList<IConstraint> constraints

  /**
   * The index further identifies a structure element within its tree structure,
   * which has different meanings depending on the type of structure element:
   *  - ConstituencyStructureElement: index of the child in the constituency tree
   *  - DependencyStructureElement: index of the child in the dependency tree
   */
  protected int index

  /**
   * Child elements of this structure element
   */
  protected ArrayList<IStructureElement> children

  /**
   * Reference of this structure element to the element parenting it
   */
  protected IStructureElement parent

  /**
   * Attribute stating, if this structure element is only temporal and product of a incremental
   * structural specification, where the element will be deleted if its not further used
   */
  private boolean temporal'''

  def __init__(self, tag, index):
    self.tag = tag
    self.index = index
    self.children = [] #new ArrayList<IStructureElement>()
    self.constraints = [] #new ArrayList<IConstraint>()
    self.temporal = False
    self.parent = None

  def getTag(self):
    return self.tag

  def setTag(self, tag):
    self.tag = tag

  def getIndex(self):
    return self.index

  def setIndex(self, index):
    self.index = index

  def getParent(self):
    return self.parent

  def setParent(self, parent):
    self.parent = parent

  def getChildren(self):
    return self.children

  #@overload
  @dispatch(object)
  def addChild(self, child):
    #String classThis = this.getClass().getSimpleName()
    #String classChild = child.getClass().getSimpleName()
    classThis = type(self).__name__
    classChild = type(child).__name__

    if(classThis == classChild):
      self.children.append(child)
      child.setParent(self)
    else:
      print("Attempting to add a " + classChild + " object into a " + classThis + "!")

  #@overload
  @dispatch(object, int)
  def addChild(self, child, index):
    classThis = type(self).__name__
    classChild = type(child).__name__

    if(classThis == classChild):
      if(len(self.children) > index):
        self.children.insert(index, child)

      else:
        self.children.append(child)

      child.setParent(self)

    else:
      print("Attempting to add a " + classChild + " object into a " + classThis + "!")

  def getChildAtIndex(self, index):
    for child in self.children:
      if(child.getIndex() == index):
        return child

    return None

  def addConstraint(self, constraint):
    self.constraints.append(constraint)


  def getConstraints(self):
    return self.constraints

  def isTemporal(self):
    return self.temporal

  def setTemporal(self, temporal):
    self.temporal = temporal

  '''/**
   * Recursively remove all temporal structure elements
   */'''
  def cleanTemporal(self):
    for child in self.children:
      if(child.isTemporal()):
        self.children.remove(child)
      else:
        child.cleanTemporal()

  '''/**
   * Checks whether the given fragment complies the structure
   * @param fragment Root of a sentence fragment
   * @return True, if the pattern structure tree is contained in the sentence structure tree and all constraints are fulfilled
   */'''
  def isCompliedBy(self, fragment):
    if(not self.isFragmentTypeCompliant(fragment)):
      return False

    if(not self.tag == self.getFragmentTag(fragment)):
      return False

    for constraint in self.constraints:
      if(not constraint.isFulfilledBy(fragment)):
        '''res, _ = self.checkSimilarWord(constraint, fragment)
        if not res:'''
        return False

    if(len(self.children) > 0):
      for child in self.children:
        childIndex = child.getIndex()
        childFragment = self.getFragmentChildAtIndex(fragment, childIndex)

        if(childFragment is None):
          return False

        if(not child.isCompliedBy(childFragment)):
          return False

    return True
  
  #TODO new!
  '''def checkSimilarWord(self, constraint, fragment):
    w1 = constraint.word
    w2s = fragment.getAllLeafs()
    
    for w2 in w2s:
      ip = w1 + ' ' + w2.getCoveredText()
    
      tokens = nlp(ip)
      tk1, tk2 = tokens[0], tokens[1]
      
      sm = tk2.similarity(tk1)
      if sm >= 0.75:
        print(f"\nComparing {w1} with {w2.getCoveredText()} gave similarity: {sm}")
        return True, w2.getCoveredText()
      
      return False, None'''
  
  '''/**
   * Checks whether the fragment type of a given sentence structure element is compliant to this structure element:
   *  - ConstituentStructureElement: Fragment (Node or Leaf)
   *  - DependencyStructureElement: Leaf
   * @param fragment Current fragment under investigation
   * @return True, if the given fragment is of the type that the structure element expects
   */'''

  @abstractmethod
  def isFragmentTypeCompliant(self, fragment):
    pass

  '''/**
   * Finds all nodes within the structure , which is erroneously compliant to the structure
   * @param constraintGenerators List of constraint generators, which aretree which are eligible for differentiation when applying one of the possible constraints
   * @param accepted List of fragments from the already accepted sentences
   * @param intruder Fragment of the intruding sentence used to propose a constraint to a structure node
   * @return A list of specification proposals, where each proposal suggest one constraint to be added to a specific node in order to differentiate the intruder from the accepted
   */'''
  #public ArrayList<SpecificationProposal> detectEligibleDifferentiator(ArrayList<Fragment> accepted, Fragment intruder, ArrayList<IConstraintGenerator> constraintGenerators) {
  def detectEligibleDifferentiator(self, accepted, intruder, constraintGenerators):
    specificationProposals = [] # new ArrayList<SpecificationProposal>()
    constraints = [] # new ArrayList<IConstraint>()

    # determine all constraints, which - when applied to this element - would differentiate the accepted fragments from the intruder
    for generator in constraintGenerators:
      if(generator.differentiates(accepted, intruder)):
        constraints.extend(generator.generateConstraints(accepted, intruder))

    # wrap constraints around specification proposals
    #constraints.forEach(c -> specificationProposals.add(c.generateProposal(this)))
    #print('root scanned')
    for c in constraints:
      specificationProposals.append(c.generateProposal(self))

    for child in self.children:
      childIndex = child.getIndex()
      f_children = self.getFragmentChildrenAtIndex(accepted, childIndex)
      intrudingChild = self.getFragmentChildAtIndex(intruder, childIndex) #intruder.getChildByIndex(childIndex)

      if(f_children is not None and intrudingChild is not None):
        specificationProposals.extend(child.detectEligibleDifferentiator(f_children, intrudingChild, constraintGenerators))

    return specificationProposals

  '''/**
   * Gathers all fragments, that are children of a current list of fragments at a given position.
   * The type of parent-child relation is dependent on the type of structure elements:
   *  - constituent structure: fragment children
   *  - dependency structure: governed children
   * @param current List of current fragments
   * @param childIndex Position of the child
   * @return List of children at a given position of the current list of fragments
   */'''
  #protected abstract ArrayList<Fragment> getFragmentChildrenAtIndex(ArrayList<Fragment> current, int childIndex)
  @abstractmethod
  def getFragmentChildrenAtIndex(self, current, childIndex):
    pass

  '''/**
   * Returns the child of a fragment at a given position, where the parent-child relation is dependent on the type of structure elements:
   *  - constituent structure: fragment children
   *  - dependency structure: governed children
   * @param element Current fragment
   * @param childIndex Position of the child
   * @return Child of the intruder at a given position
   */
  protected abstract Fragment getFragmentChildAtIndex(Fragment element, int childIndex)'''
  @abstractmethod
  def getFragmentChildAtIndex(self, element, childIndex):
    pass

  '''/**
   * Generates a chain of indices that leaf from the root node to this structure element
   * @return ArrayList of indices, which, when given to the root structure element via getStructureElementByIndexChain will return this element
   */'''
  def getIndexChain(self):
    indexChainToThisElement = None
    if(self.parent is None):
      indexChainToThisElement = []

    else:
      indexChainToThisElement = self.parent.getIndexChain()
      indexChainToThisElement.append(self.index)
      
    return indexChainToThisElement


  '''/**
   * Resolves an index chain and returns the structure element at this position
   * @param indexChain ArrayList of indices, that lead to the desired structure element
   * @return The desired structure element, if the path of indices exists
   */'''
  def getStructureElementByIndexChain(self, indexChain):
    if(not indexChain):
      return self

    else:
      #print(indexChain)
      nextIndex = indexChain[0]
      successor = self.getChildAtIndex(nextIndex)
      #print(successor.toString())

      if(successor is not None):
        # since this structure element will be used for a certain specification, it is no longer temporal
        successor.setTemporal(False)
        return successor.getStructureElementByIndexChain(indexChain[1:len(indexChain)])

      else:
        print("Attempting to get a structure element by index chain, but the current element does not have a child at the given index")
        return None


  '''/**
   * Generates a structural specification proposal from a single tag at this structure element
   * @param tag The tag the specificating structure element will be using
   * @param intruderTag The tag of the intruder, which differs from the specificating tag
   * @param index The index, at which the specificating structure element will be placed
   * @param position The position of the respective word within the sentence (for formatting purposes)
   * @return A specification proposal to place an structure element with the given tag at the given position
   */
  protected SpecificationProposal generateStructuralSpecificationProposalsFromTags(String tag, String intruderTag, int index, int position) {
  def generateStructuralSpecificationProposalsFromTags(self, tag, intruderTag, index, position):
    tags = [] #new ArrayList<String>()
    tags.append(tag)

    return generateStructuralSpecificationProposalsFromTags(tags, intruderTag, index, position)

  /**
   * Generates a structural specification proposal from a list of tags at this structure element
   * @param tags The list of tags used by the accepted sentences at the specificating position
   * @param intruderTag The tag of the intruder, which differs from the specificating tag
   * @param index The index, at which the specificating structure element will be placed
   * @param position The position of the respective word within the sentence (for formatting purposes)
   * @return A specification proposal to place structure elements with the given tags at the given position
   */
  protected SpecificationProposal generateStructuralSpecificationProposalsFromTags(ArrayList<String> tags, String intruderTag, int index, int position) {'''
  def generateStructuralSpecificationProposalsFromTags(self, tag_s, intruderTag, index, position):
    if type(tag_s).__name__ != 'list':
      tags = [ tag_s ]
    else:
      tags = tag_s
    sp = StructuralSpecificationProposal.StructuralSpecificationProposal(self, tags, intruderTag, index)
    sp.setPosition(position)

    return sp


  '''/**
   * Only for incremental structures: increase the precision of a structure by adding nodes to the tree
   * @param accepted List of the accepted sentences, which should be maintained to be compliant to the structure
   * @param intruder Sentence, where the relevant portion of the structure is compliant to the structure
   * @param specifications List of specification proposals which will enforce the specification
   * @return True, if a specification could differentiate the accepted sentences from the intruder
   */'''
  def specifySoftVersus(self, accepted, intruder, specifications):
    #print('Self: ', self.toString())
    maxNumberOfChildren = self.getHighestIndexOfStructures(accepted)
    #print(maxNumberOfChildren)
    #for(int i = 0 i <  i++) {
    for i in range(maxNumberOfChildren):
      #print('\n',self.toString())
      #print('Child ', i, ' : ', ((self.getChildAtIndex(i).toString()), 'No further exec in this loop') if self.getChildAtIndex(i) is not None else 'None')
      if(self.getChildAtIndex(i) is None):
        if(self.isStructureElementAtIndexUniversal(accepted, i)):
          primeChild = self.getFragmentChildAtIndex(accepted[0], i)
          #print('Prime child : ', primeChild.toString(True, False))
          universalTag = self.getFragmentTag(primeChild)

          if(intruder is None):
            # there cannot be a leaf node of the intruding sentence with the required universal tag at index i, therefore this is an specification
            specifications.append(self.generateStructuralSpecificationProposalsFromTags(universalTag, "no_tag_applicable", i, 0))
            return True
          else:
            intrudingChild = self.getFragmentChildAtIndex(intruder, i)
        
            if(intrudingChild is not None):
              #print('Intruder child : ', intrudingChild.toString(True, False))
              tagOfIntruding = self.getFragmentTag(intrudingChild)

              if(not tagOfIntruding == universalTag):
                # the tag is an eligible differentiator and can be used for specification
                specifications.append(self.generateStructuralSpecificationProposalsFromTags(universalTag, tagOfIntruding, i, 0))
                return True  #end if successful
              else:
                # TODO rethink this
                #print('Ting')
                universalSuccessor = self.generateUniversalSuccessor(primeChild, universalTag, i)
                if(universalSuccessor is not None):
                  universalSuccessor.setTemporal(True)
                  #print('Structure after adding newc : ', self.toString())
    
    #print('Done')
    # if no specificator could be found in this dependency structure element, continue recursively
    for child in self.children:
      #print(child.toString())
      if(intruder is not None):
        childIndex = child.getIndex() #0
        nextIntruder = self.getFragmentChildAtIndex(intruder, childIndex)
        nextAccepted = self.getFragmentChildrenAtIndex(accepted, childIndex)

        if(nextAccepted is not None):
          if(child.specifySoftVersus(nextAccepted, nextIntruder, specifications)):
            return True

    return False

  '''/**
   * Gets the highest child node count in all fragments
   * @param current List of current fragments
   * @return Highest number if child nodes
   */'''
  @abstractmethod
  def getHighestIndexOfStructures(self, current):
    pass

  '''/**
   * Identify, if all accepted sentences as well as this sentence structure contain the same structural
   * node at a given index. This is an indicator for a soft specification.
   * @param current Fragments List of current fragments
   * @param index The index under investigation
   * @return True, if all children at the position index of the current fragments have the same tag
   */'''
  def isStructureElementAtIndexUniversal(self, current, index):
    pass

  '''/**
   * Gets the corresponding tag of the given fragment according to the patterns structure type:
   *  - constituent structure: Constituency/POS tag
   *  - dependency structure: dependency relation type
   * @param fragment Current fragment
   * @return Tag of the given fragment
   */'''
  @abstractmethod
  def getFragmentTag(self, fragment):
    pass

  '''/**
   * Generates a universal successor to this structural element
   * @param tag The tag associated with the successor
   * @param index The index associated with the successor
   * @return The structure element that was created
   */'''
  @abstractmethod
  def generateUniversalSuccessor(self, primeChild, tag, index):
    pass

  '''/**
   * Only for incremental structure: increasing the precision of a structure by adding nodes to the tree.
   * In contrast to specifySoftVersus, this method will disregard the compliance of every other accepted sentence
   * than the first accepted sentence, which is called the prime sentence
   * @param prime Root fragment of the sentence, which's compliance is to be maintained throughout the specification process
   * @param otherAccepted Root fragments of the accepted sentences of the pattern excluding the prime sentence
   * @param intruder Root fragment of the sentence, where the relevant portion of the structure is erroneously compliant to the structure
   * @param specifications List of specification proposals for all sentences, that are disregarded by this pattern after the specification
   * @return True, if the specification process was successful
   */'''
  def specifyHardVersus(self, prime, accepted, intruder, specifications):
    maxNumberOfChildren = self.getHighestIndexOfStructures(accepted)

    #for(int i = 0 i <  i++) {
    for i in range(maxNumberOfChildren):
      if(self.getChildAtIndex(i) is None):
        primeFragmentAtIndex = self.getFragmentChildAtIndex(prime, i)

        if(primeFragmentAtIndex is not None):
          primeTag = self.getFragmentTag(primeFragmentAtIndex)
          acceptedTags = self.getTagsUsedByAcceptedSentencesAtIndex(accepted, i)

          intrudingChildAtIndex = self.getFragmentChildAtIndex(intruder, i)
          intrudingTag = None
          if(intrudingChildAtIndex is not None):
            intrudingTag = self.getFragmentTag(intrudingChildAtIndex)
          else:
            intrudingTag = "no_tag_applicable" #StructuralSpecificationProposal.NO_TAG_APPLICABLE


          if(primeTag != intrudingTag and intrudingTag not in acceptedTags):
            specificationTags = [] #new ArrayList<String>()
            specificationTags.extend(acceptedTags)
            if(primeTag not in specificationTags):
              specificationTags.append(primeTag)

            specifications.append(self.generateStructuralSpecificationProposalsFromTags(specificationTags, intrudingTag, i, 0))
            return True

    # if no specificator could be found in this dependency structure element, continue recursively
    for child in self.children:
      if(intruder is not None):
        childIndex = child.getIndex()

        nextPrime = self.getFragmentChildAtIndex(prime, childIndex)
        nextAccepted = self.getFragmentChildrenAtIndex(accepted, childIndex)
        nextIntruder = self.getFragmentChildAtIndex(intruder, childIndex)

        if(nextAccepted is not None):
          if(child.specifyHardVersus(nextPrime, nextAccepted, nextIntruder, specifications)):
            return True

    return False

  '''/**
   * Returns a list of all tags that are used by the children at a certain index of the current fragments
   * @param currentFragments List of all current fragments
   * @param index Index of the child position which is under investigation
   * @return List of tags used by all children at position index
   */'''
  def getTagsUsedByAcceptedSentencesAtIndex(self, currentFragments, index):
    acceptedTags = []  #new ArrayList<String>()

    for current in currentFragments:
      childAtIndex = self.getFragmentChildAtIndex(current, index)   #current.getChildByIndex(index)

      if(childAtIndex is None):
        if("no_tag_applicable" not in acceptedTags):
          acceptedTags.append("no_tag_applicable")

      else:
        tag = self.getFragmentTag(childAtIndex)   #childAtIndex.getTag()
        if(tag not in acceptedTags):
          acceptedTags.append(tag)

    return acceptedTags


  '''/**
   * Checks for each constraint if it can be moved to a deeper structure element, which would make the constraint more precise
   * @param accepted Current fragment of accepted sentences
   */'''
  def reevaluateConstraintPosition(self, accepted):
    for child in self.children:
      childIndex = child.getIndex()
      acceptedChildren = self.getFragmentChildrenAtIndex(accepted, childIndex)

      # redistribute all constraints that are still fulfilled by all accepted fragments respective to a child node
      toRemove = []   #new ArrayList<IConstraint>()
      if(acceptedChildren is not None):
        for constraint in self.constraints:
          if(constraint.isFulilledBy(acceptedChildren)):
            if constraint not in child.constraints:
              child.addConstraint(constraint)
            toRemove.append(constraint)
          '''else:
            for c in acceptedChildren:
              res, m = self.checkSimilarWord(constraint, c)
              if not res:
                break
            if res:
              if constraint not in child.constraints:
                from python.pattern.LexicalConstraint import LexicalConstraint
                child.addConstraint(LexicalConstraint(m, constraint.positive))
              toRemove.append(constraint)'''
              

      # remove all redistributed constraints from this structure element
      for c in toRemove:
        self.constraints.remove(c)

      # continue recursively
      child.reevaluateConstraintPosition(acceptedChildren)

  '''/**
   * Counts the size of the structure element tree
   * @return Number of nodes in this structure element tree
   */'''
  def size(self):
    result = 1

    for child in self.children:
      result = result + child.size()

    return result

  '''/*
   * Calculates the maximum depth of the tree structure
   * @return Length of the longest parent-child-chain
   */'''
  def getDepth(self):
    if(not self.children):
      return 1
    else:
      max = 0

      for child in self.children:
        current = child.getDepth()
        if(current > max):
          max = current

      return max+1

  '''/**
   * Gathers all leaf node of this tree structure in the given array
   * @param collection ArrayList in which the leaf nodes are stored (must be initiated)
   */'''
  def gatherAllLeafNodes(self, collection):
    if(self.children.isEmpty()):
      collection.append(self)
    else:
      for child in self.children:
        child.gatherAllLeafNodes(collection)


  '''/**
   * Calculates the number of tree nodes that are in one level
   * @param level The level, where the node width is of interest
   * @return Number of nodes that are contained at this depth level
   */'''

  def getWidthAtLevel(self, level):
    if(level == 0):
      return 1

    else:
      result = 0
      for child in self.children:
        result = result + child.getWidthAtLevel(level-1)

      return result

  '''/**
   * Gathers all node elements at a certain level
   * @param level The depth at which all nodes are collected
   * @return List of all nodes at that depth
   */'''
  def getElementsAtLevel(self, level):
    result = []   #new ArrayList<IStructureElement>()

    if(level == 0):
      result.append(self)

    else:
      if(len(self.children) > 0):
        for child in self.children:
          result.extend(child.getElementsAtLevel(level-1))

    return result

  '''/**
   * Creates a clone of this structure element and all subsequent children
   */
  public abstract IStructureElement clone()'''
  @abstractmethod
  def clone(self):
    pass

  def toString(self):
    sb = []

    sb.append("(" + self.tag + ")#" + str(self.index) + " ")
    #constraints.forEach(c -> sb.append(c.toString()))
    for c in self.constraints:
      sb.append(c.toString())


    if(len(self.children) > 0):
      sb.append("{ ")
      sj = [""]  #new StringJoiner(" ")
      #children.forEach(child -> sj.add(child.toString()))
      for child in self.children:
        sj.append(child.toString())

      sb.append(''.join(sj))
      sb.append("} ")

    return ''.join(sb)
