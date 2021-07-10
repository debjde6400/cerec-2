from python.sentence.Fragment import Fragment
from python.util.Globals import Globals
from multipledispatch import dispatch

class Leaf(Fragment):

  '''/**
   * Reference to the actual NLP-token, which is represented by this object
   */
  private int position;

  /**
   * Reference to the leaf node which is governing this node dependency-wise.
   * If this attribute is null, this node is the root dependency node
   */
  private Leaf governor;

  /**
   * Tag of the dependency relation, in which this node is to its governor
   */
  private String dependencyRelationType;

  /**
   * List of all leaf nodes that are governed by this node
   */
  private ArrayList<Leaf> governed;'''

  #public Leaf(String tag, String coveredText, int position, int index) {
  def __init__(self, tag, coveredText, position, abs_pos, index):
    super().__init__(tag, coveredText, index)
    self.position = position
    self.abs_pos = abs_pos

    self.governed = []
    self.dependencyRelationType = ""
    self.governor = None

  def getPosition(self):
    return self.position

  def setPosition(self, position):
    self.position = position

  #@Override
  def getDepth(self):
    return 1

  #@Override
  def getChildByIndex(self, index):
    return None

  def getGovernor(self):
    return self.governor

  '''@overload
  def setGovernor(self, governer):
    self.governor = governer;
    governer.addGoverned(self)'''

  #@overload
  def setGovernor(self, governer, dependencyRelationType=''):
    #print(type(governer))
    self.governor = governer
    governer.addGoverned(self)
    self.dependencyRelationType = dependencyRelationType

  #@overload
  @dispatch()
  def getGoverned(self):
    return self.governed

  #@overload
  @dispatch(int)
  def getGoverned(self, index):
    if(self.governed.size() > index):
      return self.governed[index]
    return None

  '''/**
   * Returns the first Leaf that contains the given Phrase as a covered Text
   * @param word The word of which the covering leaf is desired
   * @return The leaf, that covers the word or null if there is none
   */'''
  #@overload
  @dispatch(str)
  def getGoverned(self, word):
    if(self.getCoveredText() == word):
      return self

    else:
      for child in self.governed:
        if(child.getGoverned(word) is not None):
          return child.getGoverned(word)

      return None

  '''/**
   * Returns the leaf node that covers the given word and is closest to a given index
   * @param word The word of which the covering leaf is desired
   * @param covered If true use the covered text (single word), if false use the governed text
   * @param beginIndex The begin index within the sentence to which the leaf should be closest to
   * @param endIndex The end index within the sentence to which the leaf should be closest to
   * @return The leaf node covering the word and closest to the given index or null if there is none
   */'''
  #@overload
  @dispatch(str, bool, int, int)
  def getGoverned(self, word, covered, beginIndex, endIndex):
    content = (self.getCoveredText() if covered else self.getGovernedPhrase())
    if(content == word):
      return self

    else:
      # gather all leaf nodes that contain the given word
      eligible = []
      for child in self.governed:
        potential = child.getGoverned(word, covered, beginIndex, endIndex)
        if(potential is not None):
          eligible.append(potential)

      if(not eligible):
        return None

      elif(len(eligible) == 1):
        return eligible[0]

      else:
        # select the leaf that is the most eligible
        # TODO still multiple words possible
        mostEligible = None
        minDistance = 9999     # ??
        for elig in eligible:
          distance = elig.getPosition() - beginIndex
          end = elig.getPosition() + len(elig.getCoveredText())
          if(distance >= 0 and distance < minDistance and end <= endIndex):
            minDistance = distance
            mostEligible = elig

        return mostEligible

  def addGoverned(self, governed):
    self.governed.append(governed)

  def getDependencyRelationType(self):
    return self.dependencyRelationType

  def isRoot(self):
    return self.dependencyRelationType == 'ROOT'

  def setDependencyRelationType(self, dependencyRelationType):
    self.dependencyRelationType = dependencyRelationType

  '''/**
   * Identify if this node directly or transitively governing all given phrases
   * @param others List of phrases, where the governance is to be determined
   * @return True, if all given phrases are governed by this leaf node
   */'''
  def isGoverningAllPhrases(self, others):
    for other in others:
      if(not self.isGoverningPhrase(other)):
        return False

    return True

  '''/**
   * Determine, whether a given phrase is directly or transitively governed by this node
   * @param other The phrase, where the governance is to be determined
   * @return True, if the given phrase is governed by this leaf node
   */'''
  def isGoverningPhrase(self, other):
    for gov in self.governed:
      if(gov.getCoveredText() == other):
        # phrase is directly governed by this node
        return True
      else:
        # phrase might be transitively governed by this node
        if(gov.getCoveredText() != self.getCoveredText()):
          if(gov.isGoverningPhrase(other)):
            return True

        else:
          return False

    return False

  '''/**
   * Generates the phrase encompassed by this dependency structure
   * @return The coveredText of all transitive child nodes of this dependency leaf
   */'''
  def getGovernedPhrase(self):
    if(not self.governed):
      return self.getCoveredText()

    else:
      sj = []
      integratedThisCoveredText = False
      
      for gov in self.governed:
        if(not integratedThisCoveredText and gov.getPosition() > self.getPosition()):
          sj.append(self.getCoveredText())
          integratedThisCoveredText = True

        sj.append(gov.getGovernedPhrase())

      if(not integratedThisCoveredText):
        sj.append(self.getCoveredText())
        integratedThisCoveredText = True

      return ' '.join(sj)

  '''/**
   * Gets all governed leafs (including this one) in a list ordered by position
   * @return List of transitively governed leafs
   */'''
  def getAllGoverned(self):
    result = []
    if(not self.governed):
      result.append(self)

    else:
      integratedThisCoveredText = False
      for gov in self.governed:
        if(not integratedThisCoveredText and gov.getPosition() > self.getPosition()):
          result.append(self)
          integratedThisCoveredText = True

        result.extend(gov.getAllGoverned())

      if(not integratedThisCoveredText):
        result.append(self)
        integratedThisCoveredText = True

    return result


  '''/**
   * Identify if this node directly or transitively governing all given leaf nodes
   * @param others List of leaf nodes, where the governance is to be determined
   * @return True, if all given leaf nodes are governed by this leaf node
   */'''
  def isGoverningAllLeafs(self, others):
    for other in others:
      if(not self.isGoverningLeaf(other)):
        return False

    return True

  '''/**
   * Determine, whether a given leaf node is directly or transitively governed by this node
   * @param other The leaf node, where the governance is to be determined
   * @return True, if the given leaf node is governed by this leaf node
   */'''
  def isGoverningLeaf(self, other):
    for gov in self.governed:
      if(gov == other):
        return True
      else:
        if(gov != other):
          if(gov.isGoverningLeaf(other)):
            return True

        else:
          return False

    return False

  '''/**
   * Determine, how many governed leaf nodes of the governor of the current node have the same
   * dependency relation with the shared governor as this node. This may be necessary to specify
   * this node
   * @return
   */'''
  def getNumberOfDependencyRelationOccurrencesBeforeThis(self):
    result = 0

    for gov in self.governor.getGoverned():
      if(gov == self):
        break

      else:
        if(gov.getDependencyRelationType() == self.dependencyRelationType):
          result += 1

    return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getRootGovernor(self):
    '''if(self.dependencyRelationType.equals(Constants.DEPENDENCY_RELATION_TYPE_ROOT)) :
      return self'''

    if(self.dependencyRelationType == 'ROOT') :
      return self

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getChildren(self):
    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getAllLeafs(self):
    result = []
    result.append(self)
    return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getLeafByBeginIndex(self, beginIndex):
    if(self.position == beginIndex):
      return self

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getLeafByAbsPos(self, apos):
    if(self.abs_pos == apos):
      return self

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def isParenting(self, other):
    return False

  '''/**
   * Calculate the degree of relation from this leaf node to any other given fragment by counting
   * how many nodes lie between this node and the other
   * @param other The fragment to which the relation is to be calculated
   * @return Quantification of relatedness between this node and the other
   */'''
  def getDegreeOfRelation(self, other):
    degree = 0
    while(not other.isParenting(self)):
      degree += 1
      other = other.getParent()

    return degree

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def split(self):
    #CELogger.log().error("Trying to invoke a 'split'-command on a leaf node");
    print("Trying to invoke a 'split'-command on a leaf node");
    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def select(self, byType, indicator, selected):
    if(byType and self.getTag() == indicator):
      selected.append(self)
    elif(not byType and self.getCoveredText() == indicator):
      selected.append(self)

    return selected


  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getBy(self, byType, indicator, selected):
    return self.select(byType, indicator, selected)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getLeafs(self, byType, indicator, selected):
    if(byType and self.getTag() == indicator):
      selected.append(self)
    elif(not byType and self.getCoveredText() == indicator):
      selected.append(self)

    return selected

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getParentOf(self, child):
    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getDirectParentOf(self, child):
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

    return False
  
  '''def checkSimilarityByWord(self, text, nlp):
    if(self.getTag() == text):
      return True
    
    w1 = text
    w2 = self.getCoveredText()
    
    ip = w1 + ' ' + w2
  
    tokens = nlp(ip)
    tk1, tk2 = tokens[0], tokens[1]
    
    sm = tk1.similarity(tk2)
    if sm >= 0.75:
      #print(sm)
      return True

    return False'''

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  #@dispatch(object, Fragment)
  def contains(self, fragment):
    if(self == fragment):
      return True

    return False

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getCompositionFor(self, expression):
    container = []
    if(expression.contains(self.getCoveredText())):
      container.append(self)

    return container

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch()
  def toString(self):
    if(self.position == 0):
      return self.getCoveredText()
    else:
      if(self.dependencyRelationType != "punct"):
        return " " + self.getCoveredText()
      else:
        return self.getCoveredText()

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch(bool, bool)
  def toString(self, structurized, dependencies):
    result = self.getCoveredText()

    if(structurized):
      result = result + " (" + self.getTag() + ") "

    if(dependencies):
      if(self.dependencyRelationType != None and self.governor != None):
        result = result + " [--" + self.dependencyRelationType + "-> " + self.governor.getCoveredText() + "]"
      else:
        if(self.dependencyRelationType == "ROOT"):
          result = result + " [--> ROOT]"
        else:
          result = result + " [no dependency]"

    return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch(int, bool)
  def toString(self, indent, showConstituentText):
    result = Globals.getInstance().getIndentation("  ", indent)   #??
    if(self.isRoot()):
      result = result + " (" + self.getTag()+ ") " + self.getCoveredText() + " [" + self.getDependencyRelationType() + "]"
    else:
      result = result + " (" + self.getTag()+ ") " + self.getCoveredText() + " [--" + self.getDependencyRelationType() + "--> " + self.getGovernor().getCoveredText() + "]"

    return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #@overload
  @dispatch(list)
  def toString(self, highlights):
    if(highlights.contains(self)):
      return "*" + self.getCoveredText() + "*"
    else:
      return self.getCoveredText()

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def structureToString(self, constituent):
    if(constituent):
      return None
    
    else:
      result = " (" + self.dependencyRelationType + ") "
      sj = [""]
      
      for child in self.governed:
        childStructure = child.structureToString(constituent)
        sj.append(childStructure)

      childStructure = ' '.join(sj)
      if(childStructure is not None):
        result = result + " { " + childStructure + "}"

      return result

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def size(self):
    return 1
