from python.genetics.ICommandGenerator import ICommandGenerator
from python.genetics.ConstituentCommandSelect import ConstituentCommandSelect
from python.genetics.ConstituentCommandMultiselect import ConstituentCommandMultiselect
from python.genetics.ConstituentCommandNavigate import ConstituentCommandNavigate
from python.genetics.ConstituentCommandPick import ConstituentCommandPick
from python.genetics.NavigationStep import NavigationStep
from python.sentence.Leaf import Leaf
from python.util.Utils import Utils
#from python.sentence.Fragment import Fragment
#from typing import overload
from multipledispatch import dispatch

class ConstituentCommandGenerator(ICommandGenerator):

  '''/**
   * Creates a generator, which extracts the given cause-/effect-expression from the sentence
   * @param sentence The sentence under analysis
   * @param expression The cause-/effect-expression
   * @param index The begin index of the word (optionally used when a sentence contains multiple identical leafs (same text and type) in order to differentiate them)
   * @return
   */'''
   
  def generateCommandPattern(self, sentence, expression):
    command = None

    # attempt single root extraction
    command = self.generateVerticalSelectionByType(sentence, expression)
    if(command is not None):
      return command

    # attempt same level conglomerate selection
    command = self.generateMultiSelection(sentence, expression)
    if(command is not None):
      return command

    # attempt a horizontal selection by leafs
    command = self.generateHorizontalSelectionByLeafs(sentence.getRootConstituent(), expression)
    if(command is not None):
      return command

    # attempt a horizontal selection by words
    command = self.generateHorizontalSelectionByWords(sentence.getRootConstituent(), expression)
    if(command is not None):
      return command

    #self.opfile.writeToF2("Unable to generate extraction command")
    print("Unable to generate extraction command")

  '''/**
   * Attempts to find a single node within the structural tree of the sentence, that has the desired expression as covered text
   * @param sentence Internal representation of the sentence
   * @param expression Desired expression, which is to be extracted from the sentence
   * @return A constituent command that is able to extract a node covering the desired expression - if possible
   */'''
  def generateVerticalSelectionByType(self, sentence, expression):
    #ArrayList<Fragment> eligibleByExpression = new ArrayList<Fragment>();
    #tokenized_sent = list(self.parser.tokenize(expression))
    processedExpression = ' '.join(self.annotator.tokenize_sent(expression))
    #processedExpression = Utils.resolveContractions(processedExpression, True)
    #processedExpression = Utils.resolvePunctuations(processedExpression, True)
    
    eligibleByExpression = []
    eligibleByExpression = sentence.getRootConstituent().select(False, processedExpression, eligibleByExpression)
    #print("By vertical selection : ", [e.getCoveredText() for e in eligibleByExpression])

    if(len(eligibleByExpression) == 1):
      target = eligibleByExpression[0]

      command = self.getSelectorFor(sentence.getRootConstituent(), target)
      return command

    return None


  def generateMultiSelection(self, sentence, expression):
    command = None
    root = sentence.getRootConstituent()

    conglomerateChildren = []
    leafChain = self.findLeafChain(root, expression)

    if(leafChain is None):
      #print('Dinka chika')
      return None

    #print([p.toString(True, True) for p in leafChain])
    for l in leafChain:
      conglomerateChildren.append(l)

    if(not conglomerateChildren):
      return None

    # substitute encompassed child fragments by their encompassing parent fragment
    encompassingParent = self.getEncompassingParent(conglomerateChildren)
    while(encompassingParent is not None):
      # remember at which position the encompassed fragment was placed
      index = conglomerateChildren.index(encompassingParent.getChildren()[0])
      # remove encompassed child fragments
      for child in encompassingParent.getChildren():
        conglomerateChildren.remove(child)

      # add the encompassing parent fragment at the position of the child fragments
      conglomerateChildren.insert(index, encompassingParent)

      # check, if another encompassing parent exist
      encompassingParent = self.getEncompassingParent(conglomerateChildren)


    # abort if the conglomerate process is not successful enough
    # TODO rework evaluation of the conglomerate process
    if(len(conglomerateChildren) >= len(leafChain)):
      return None

    selectors = []
    for child in conglomerateChildren:
      selectors.append(self.getSelectorFor(root, child))

    command = ConstituentCommandMultiselect(selectors)

    generatedResult = command.generateOutput(root).strip()
    processedExpression = ' '.join(self.annotator.tokenize_sent(expression))
    if(generatedResult == processedExpression):
      return command

    else:
      self.printDirectOrFile("The multiselection generated the following opposed to the desired:")
      self.printDirectOrFile(" - des: " + expression + " (" + processedExpression + ")")
      self.printDirectOrFile(" - gen: " + generatedResult)
      return None

    return None

  '''/**
   * Identifies a fragment, where all children are contained in the current list of fragments
   * @param list List of current fragments
   * @return The first fragment, where all children are contained in the current list, or null, if this does not exist
   */'''
  def getEncompassingParent(self, lst):
    for fragment in lst:
      parent = fragment.getParent()

      if(parent is not None):
        allChildrenOfParentInList = True

        for child in parent.getChildren():
          #if(not lst.contains(child)):
          if child not in lst:
            allChildrenOfParentInList = False
            break

        if(allChildrenOfParentInList):
          return parent

    return None

  '''/**
   * Generates a selection from the root to the target, regardless of whether the search is unique yet or not
   * @param rootConstituent Root node of the sentence
   * @param target Targeted node within the structure
   * @return Constituent command that yields the target fragment when executed on the root fragment
   */'''
  def getSelectorFor(self, rootConstituent, target):
    eligibleByType = []
    rootConstituent.getBy(True, target.getTag(), eligibleByType)

    if(len(eligibleByType) == 1):
      return ConstituentCommandSelect(byType=True, indicator=target.getTag())

    else:
      return self.getUniqueSelector(rootConstituent, target)


  '''/**
   * Generates a navigation to a point, from where on a selection by type will yield a unique result
   * @param rootConstituent Root fragment in the constituency tree from where the search will start
   * @param target Desired target fragment, which shall be selected via its tag
   * @return A constituent command that yields the target fragment
   */'''
  def getUniqueSelector(self, rootConstituent, target):
    navigationToUniqueSelector = []
    selectorFound = False

    current = rootConstituent
    while(not selectorFound):
      if(current == target):
        selectorFound = True
        break

      eligibleByTag = []
      current.getBy(True, target.getTag(), eligibleByTag)

      if(len(eligibleByTag) == 1):
        selectorFound = True

      else:
        for child in current.getChildren():
          if(child.contains(target)):
            navigationToUniqueSelector.append(self.generateNavigationStepToChild(current, child))
            current = child
            break

    selector = ConstituentCommandNavigate(navigationToUniqueSelector)
    if(current == target):
      selector.chainCommand(ConstituentCommandSelect())

    else:
      selector.chainCommand(ConstituentCommandSelect(byType=True, indicator=target.getTag()))
    return selector

  '''/**
   * Attempt to generate a selector for a governing leaf within the expression, which uses horizontal selection to find the remaining words of the expression
   * @param root The root fragment of the sentence
   * @param phrase The phrase to be extracted
   * @return Command, which extracts the given phrase from a sentence structure
   */'''
  def generateHorizontalSelectionByLeafs(self, root, phrase):
    # find the chain of leafs, that represent the phrase in the sentence
    leafChain = self.findLeafChain(root, phrase)
    #print("Horizontal selection's leaf chain: ", str(leafChain))

    if(leafChain is not None):
      governor = None
      outsiderGovernor = False

      # find the one leaf within the chain, which governs all other leafs
      others = None
      for leaf in leafChain:
        others = Utils.generateListWithout(leafChain, leaf)
        if(leaf.isGoverningAllLeafs(others)):
          governor = leaf
          #print('Found inside gov. : ', governor.toString(True, True))
          break

      if(governor is None):
        # no governor found within the leafChain, try finding one outside
        outsiders = root.getAllLeafs()
        for outsider in outsiders:
          if(outsider not in leafChain):
            if(outsider.isGoverningAllLeafs(leafChain)):
              governor = outsider
              outsiderGovernor = True
              #print('Found outside gov. : ', governor.toString(True, True))
              break

      if(governor is not None):
        # generate a selector picking the governing leaf
        selectEligible = self.generateNavigationCommand(root, governor)

        if(not outsiderGovernor):
          # add horizontal selection for all other leafs
          for other in others:
            picker = self.generateCommandPickFor(governor, other)
            selectEligible.getFinal().addHorizontalSelection(picker)

          # place the governor within the horizontal selections
          # TODO probable problems may be here and needs solving
          positionOfGovernorWithin = Utils.getPositionOfWordInExpression(phrase, governor.getCoveredText())
          #print(governor.getCoveredText())
          #print(positionOfGovernorWithin)
          indexOfGovernorWithin = phrase.index(governor.getCoveredText())
          if(indexOfGovernorWithin > 0):
            substringUntilGovernor = phrase[:indexOfGovernorWithin]
            #print(Utils.numberOfOccurrences(substringUntilGovernor, Utils.contractions))
            positionOfGovernorWithin += Utils.numberOfOccurrences(substringUntilGovernor, Utils.contractions)

          selectEligible.getFinal().setPositionOfSelectedBetweenHorizontalSelection(positionOfGovernorWithin)

        else:
          # add horizontal selection for all other leafs
          for other in leafChain:
            picker = self.generateCommandPickFor(governor, other)
            selectEligible.getFinal().addHorizontalSelection(picker)

          # do not place the governor within the horizontal selections, as it is an outside governor
          selectEligible.getFinal().setPositionOfSelectedBetweenHorizontalSelection(-1)

        return selectEligible
      else:
        # unable to find a governing leaf in the leaf chain
        #self.opfile.writeToF2("Unable to find a governor")
        self.printDirectOrFile("Unable to find a governor")
        return None

    else:
      # unable to find a chain of leafs representing the phrase
      self.printDirectOrFile("Unable to find the leaf chain for the following sentence:")
      self.printDirectOrFile(" - sentence: " + root.getCoveredText())
      self.printDirectOrFile(" - expression: " + phrase)
      return None

  '''/**
   * If possible, find the chain of leafs that represent the phrase in the internal representation of the sentence
   * @param root Root fragment of the internal representation of the sentence
   * @param phrase Expression, that shall be found in the sentence
   * @return The chain of leafs in the sentence, that cover the phrase
   */'''

  def findLeafChain(self, root, phrase):
    all = root.getAllLeafs()
    phraseAsLeafs = []
    #phrase = Utils.breakWordsAccToParsing(phrase)
    #phrase = Utils.resolvePunctuations(phrase, True)
    #phrase = Utils.resolveContractions(phrase, True)
    #tokenized_sent = list(self.parser.tokenize(expression))
    #processedExpression = ' '.join(tokenized_sent)
    phraseWords = self.annotator.tokenize_sent(phrase) #phrase.split(" ")
    #print(phraseWords)
    leafChainFound = False
    phraseIndex = 0

    for leaf in all:
      #print('Comparing: ', phraseWords[phraseIndex], ' with : ', leaf.getCoveredText())
      if(phraseWords[phraseIndex] == leaf.getCoveredText()):
        phraseAsLeafs.append(leaf)
        phraseIndex += 1

        if(phraseIndex == len(phraseWords)):
          leafChainFound = True
          break

    if(leafChainFound):
      return phraseAsLeafs

    else:
      return None

  '''/**
   * Attempt to generate a selector for a governing leaf within the expression, which uses horizontal selection to find the remaining words of the expression
   * @param root The root fragment of the sentence
   * @param phrase The phrase to be extracted
   * @return Command, which extracts the given phrase from a sentence structure
   */'''

  def generateHorizontalSelectionByWords(self, root, phrase):
    wordsOfExpression = phrase.split(" ")
    for word in wordsOfExpression:
      # for each word of the expression: check if all other words have a reference to this word
      st = []
      root.getLeafs(False, word, st)

      # words used in the expression can appear multiple times, but only the one belonging to the expression is possibly governing
      for eligibleFragment in st:
        remainingWordsOfExpression = Utils.generateListWithout(wordsOfExpression, word)

        governor = eligibleFragment
        if(governor.isGoverningAllPhrases(remainingWordsOfExpression)):
          # create a command that selects the governing leaf node
          selectEligible = self.generateNavigationCommand(root, governor)

          for other in remainingWordsOfExpression:
            picker = self.generateCommandPickFor(root, governor, other)
            selectEligible.getFinal().addHorizontalSelection(picker)

          selectEligible.getFinal().setPositionOfSelectedBetweenHorizontalSelection(Utils.getPositionOfWordInExpression(phrase, governor.getCoveredText()))

          return selectEligible


    # unable to generate a command extracting the phrase
    return None


  '''/**
   * Generates a navigation command that, when executed on the given root node, will yield the target node
   * @param root The initial fragment, on which the command will be executed
   * @param target The desired outcome of the command
   * @return A command which, when executed on the root fragment, yields the target fragment
   */'''
  def generateNavigationCommand(self, root, target):
    navigationFromRootToLeaf = []

    current = target
    # iterate upwards until the root is reached
    while(current != root):
      parent = current.getParent()

      # add the corresponding navigation step information
      stepFromParentToCurrent = self.generateNavigationStepToChild(parent, current)
      navigationFromRootToLeaf.insert(0, stepFromParentToCurrent)
      current = parent


    # chain a selection command to the navigation
    command = ConstituentCommandNavigate(navigationFromRootToLeaf)
    command.chainCommand(ConstituentCommandSelect())
    return command

  '''/**
   * Generates a navigation step from the given parent fragment to the child fragment
   * @param parent The parenting fragment
   * @param child Child fragment of the parenting fragment
   * @return A navigation step that leads from the parent fragment to the child fragment
   */'''
  def generateNavigationStepToChild(self, parent, child):
    #if(parent.getChildren().contains(child)):
    if child in parent.getChildren():
      tag = child.getTag()

      # calculate how many children of the given type appear before the desired
      index = 0
      for parentsChild in parent.getChildren():
        if(parentsChild.getTag() == tag):
          if(parentsChild == child):
            break
          else:
            index += 1

      stepFromParentToChild = NavigationStep(tag, index)
      return stepFromParentToChild

    else:
      return None

  '''/**
   * Generates a horizontal selection via dependency parser relations
   * @param root The fragment, on which the pick command will be executed on
   * @param governor The leaf fragment which governs the desired fragment
   * @param governed The text of the desired fragment
   * @return Chain of commands which, when executed on the root fragment, yields the governed fragment
   */'''
  #@overload
  @dispatch(object, Leaf, str)
  def generateCommandPickFor(self, root, governor, governed):
    # find out how many leaf nodes under the root contain the text of the parameter governed
    eligible = []
    root.getLeafs(False, governed, eligible)

    if(len(eligible) > 0):
      if(len(eligible) == 1):
        # only one result: generate a pick-command for this leaf fragment
        return self.generateCommandPickFor(governor, eligible[0])

      else:
        # more than one result: find the most leaf node most closely related to the governing node
        closest = None
        closestDegreeOfRelation = 9999

        for elig in eligible:
          # calculate the degree of relation between the governor and the potential fragment
          degreeOfRelation = governor.getDegreeOfRelation(elig)

          if(degreeOfRelation < closestDegreeOfRelation):
            closestDegreeOfRelation = degreeOfRelation
            closest = elig

        # generate a pick-command for the most clsely related leaf fragment
        command = self.generateCommandPickFor(governor, closest)
        return command

    else:
      self.printDirectOrFile("Unable to generate a Pick-Command")
      self.printDirectOrFile("  Sentence: " + root.toString())
      self.printDirectOrFile("  Governor: " + governor.toString())
      self.printDirectOrFile("  Governed: " + governed)
      '''print("Unable to generate a Pick-Command")
      print("  Sentence: " + root.toString())
      print("  Governor: " + governor.toString())
      print("  Governed: " + governed)'''
      return None

  '''/**
   * Generates a horizontal selection via dependency parser relations
   * @param governor The leaf fragment which governs the desired fragment
   * @param governed The leaf fragment which shall be selected
   * @return Chain of commands which, when executed on the root fragment, yields the governed fragment
   */'''
  #@overload
  @dispatch(Leaf, Leaf)
  def generateCommandPickFor(self, governor, governed):
    # traverse all directly governed leaf nodes of the governor
    for gov in governor.getGoverned():
      # try to identify the desired leaf node
      if(gov == governed):
        # if found, generate a pick command via the dependency relation
        dependencyRelationType = gov.getDependencyRelationType()
        # identify, whether the dependency relation occurs more often
        # if so, find out at which index the desired governed leaf node is placed
        index = gov.getNumberOfDependencyRelationOccurrencesBeforeThis()

        return ConstituentCommandPick(dependencyRelationType, index)

    # transitive approach, as the current node does not directly govern the relevant node
    for gov in governor.getGoverned():
      transitiveSearchResult = self.generateCommandPickFor(gov, governed)
      if(transitiveSearchResult is not None):
        # create a selector for the transitively eligible leaf  fragment
        dependencyRelationType = gov.getDependencyRelationType()
        index = gov.getNumberOfDependencyRelationOccurrencesBeforeThis()

        initialize = ConstituentCommandPick(dependencyRelationType, index)
        initialize.chainCommand(transitiveSearchResult)
        return initialize

    return None
  
  def printDirectOrFile(self, st, debug=False):
    if debug:
      print(st)
    else:
      self.opfile.writeToF2(st)
