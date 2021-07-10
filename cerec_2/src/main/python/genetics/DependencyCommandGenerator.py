'''package jfr.cerec.genetics;

import java.util.ArrayList;
import java.util.Arrays;

import jfr.cerec.sentence.ISentence;
import jfr.cerec.sentence.Leaf;
import jfr.cerec.util.CELogger;
import jfr.cerec.util.Utils;'''
from python.genetics.ICommandGenerator import ICommandGenerator
from python.genetics.DependencyCommandSelect import DependencyCommandSelect
from python.genetics.DependencyCommandMultiSelect import DependencyCommandMultiSelect
from python.genetics.DependencyCommandNavigate import DependencyCommandNavigate
from python.genetics.DependencyCommandGeneratorPhrase import DependencyCommandGeneratorPhrase
from python.genetics.PhraseExtractor import PhraseExtractor
from python.util.Utils import Utils

class DependencyCommandGenerator(ICommandGenerator):
  '''/**
   * Generates a command that extracts the given phrase from the given sentence
   * @param sentence The sentence, from which the phrase is extracted
   * @param phrase The phrase that is to be extracted
   * @return A command extracting the phrase from the sentence, null if no such command is possible
   */'''
  
  def generateCommandPattern(self, sentence, phrase):
    command = None
    root = sentence.getRootDependency()
    phrase = ' '.join(self.annotator.tokenize_sent(phrase))
    print(phrase)

    # check if the phrase is maybe governed by exactly one node
    phraseGovernor = self.getLeafGoverningPhrase(root, phrase)
    if phraseGovernor is not None:
      command = self.generatePathToLeaf(root, phraseGovernor)
      command.setSuccessor(DependencyCommandSelect(True))
      
    else:
      # if the phrase is not governed by exactly one leaf node, attempt to find a node that governs at least the phrase
      governor = self.getGenerousLeafGoverningPhrase(root, phrase)
      #System.out.println("Generous governor: " + governor.getCoveredText());

      if governor is not None:
        command = self.generatePathToLeaf(root, governor)

        s = sentence.getSentenceText()
        print(s)
        print(phrase)
        beginPositionOfPhrase = s.index(phrase)
        # every contraction in the sentence will result in shifting the begin of the phrase back
        if(beginPositionOfPhrase > 0):
          beginPositionOfPhrase = beginPositionOfPhrase - (Utils.numberOfOccurrences(s[:beginPositionOfPhrase], Utils.contractions))
        endPositionOfPhrase = beginPositionOfPhrase + len(phrase)
        multiselect = self.generateMultiSelect(governor, phrase, beginPositionOfPhrase, endPositionOfPhrase)
        command.setSuccessor(multiselect)
      else:
       print("DependencyCommandGenerator was unable to find a leaf node that governs the desired phrase.")

    if(command is not None):
      # wrap command with a PhraseExtractor, which complies to the desired interface, obtains the root governor and combines the leaf texts accordingly
      return PhraseExtractor(command)
    else:
      print("DependencyCommandGenerator was unable to generate a command for the following extraction:");
      print(" Sentence: " + sentence.toString())
      print(" Sentence Structure: " + sentence.structureToString(False))
      print(" Desired phrase: " + phrase)
      return None

  '''/**
   * Get the leaf that is governing exactly the given phrase
   * @param current Current node, from where the given phrase is to be found
   * @param phrase Phrase that is to be found
   * @return The leaf, that governs exactly the given phrase or null, if no such leaf exists
   */'''
  def getLeafGoverningPhrase(self, current, phrase):
    if(current.getGovernedPhrase() == phrase):
      return current
    else:
      for governed in current.getGoverned():
        result = self.getLeafGoverningPhrase(governed, phrase)
        if(result is not None):
          return result

    return None
  

  '''/**
   * Get the most precise leaf that is governing the given phrase
   * @param current Current node, from where the given phrase is to be found
   * @param phrase Phrase that is to be found
   * @return The leaf, that governs the phrase and as little other leafs as possible
   */'''
  def getGenerousLeafGoverningPhrase(self, current, phrase):
    moreSpecificGovernor = None

    # attempt to find a child node that still governs all words of the phrase
    for child in current.getGoverned():
      wordsOfPhrase = phrase.split(" ") #new ArrayList<String>(Arrays.asList(phrase.split(" ")));
      if(child.isGoverningAllPhrases(wordsOfPhrase)):
        # this child is a more specific governor
        moreSpecificGovernor = child
        break

    if(moreSpecificGovernor is None):
      # this is the most specific governor, no child node governs all phrases
      return current
    else:
      return self.getGenerousLeafGoverningPhrase(moreSpecificGovernor, phrase)

  '''/**
   * Generates a navigate command, that leads from the given root node to the destination node
   * @param root The leaf node in which to start
   * @param destination The leaf node in which to end
   * @return Command leading from the root to the destination
   */'''
  def generatePathToLeaf(self, root, destination):
    selector = DependencyCommandNavigate()

    current = root
    while(not current == destination):
      for next in current.getGoverned():
        if(next.isGoverningLeaf(destination) or next == destination):
          tag = next.getDependencyRelationType()
          index = next.getNumberOfDependencyRelationOccurrencesBeforeThis()
          selector.addTag(tag, index)
          current = next
          break

    return selector

  '''/**
   * Generates a command that extracts a phrase which is not exclusively governed by one single node
   * @param governor The root node from where the selections shall originate
   * @param phrase The phrase to extract
   * @param beginIndex The index, at which position the phrase begins in the sentence
   * @return A multi select command that extracts the phrase or null if not possible
   */'''
  def generateMultiSelect(self, governor, phrase, beginIndex, endIndex):
    #phrase = Utils.resolvePunctuations(phrase, True)
    #phrase = Utils.resolveContractions(phrase, True)
    multiselect = DependencyCommandMultiSelect()

    # identify all leafs that compose the phrase
    leafsGoverningPhrase = [] #ArrayList<DependencyCommandGeneratorPhrase>();
    beginIndexOfWord = beginIndex
    print(phrase.split(" "))
    print(governor.getCoveredText())
    for word in phrase.split(" "):
      eligible = governor.getGoverned(word, True, beginIndexOfWord, endIndex)
      if(eligible is not None):
        leafsGoverningPhrase.append(DependencyCommandGeneratorPhrase(eligible, False))
        beginIndexOfWord = eligible.getPosition() + len(word) + 1
      else:
        print("Could not determine word '" + word + "' in phrase '" + phrase + "'");
        return None
      
      beginIndexOfWord = beginIndexOfWord + len(word) + 1
    
    # attempt to reduce the number of partial phrases by identifying full branches
    self.identifyBranchesCoveringPhrase(governor, phrase, leafsGoverningPhrase, beginIndex, endIndex)

    # construct a multi select for each phrase remaining in the list that constructs the phrase
    for leafPhrase in leafsGoverningPhrase:
      fullBranch = leafPhrase.isAll()
      if(governor == leafPhrase.getReference()):
        multiselect.addSelector(DependencyCommandSelect(fullBranch))
      else:
        selector = self.generatePathToLeaf(governor, leafPhrase.getReference())
        selector.setSuccessor(DependencyCommandSelect(fullBranch))
        multiselect.addSelector(selector)

    return multiselect

  '''/**
   * Traverses the current set of leafs, that construct the phrase, and reduces leafs by identifying other leafs that govern their covered text
   * @param root Current root node
   * @param phrase Phrase that needs to be extracted
   * @param governingLeafs Original list of phrases that need to be extracted, which will be optimized
   */'''
  def identifyBranchesCoveringPhrase(self, root, phrase, governingLeafs, beginIndex, endIndex):
    if(" " in root.getGovernedPhrase()):
      if(root.getGovernedPhrase() in phrase and root.getPosition() >= beginIndex):
        self.getCorrespondingPhrase(governingLeafs, root).setAll(True)

        # remove all words from the list of leafs that are now contained by the governing leaf
        for word in root.getGovernedPhrase().split(" "):
          if(not word == root.getCoveredText()):
            coveredLeaf = root.getGoverned(word, True, beginIndex, endIndex)
            coveredPhrase = self.getCorrespondingPhrase(governingLeafs, coveredLeaf)
            governingLeafs.remove(coveredPhrase)

      else:
        for governed in root.getGoverned():
          if(governed.getPosition() >= beginIndex and governed.getPosition()+len(governed.getCoveredText()) <= endIndex):
            self.identifyBranchesCoveringPhrase(governed, phrase, governingLeafs, beginIndex, endIndex)

    return

  '''/**
   * Get the corresponding phrase object to a leaf
   * @param leafs The list of phrases
   * @param desired The desired leaf
   * @return The phrase that is referencing the given leaf
   */'''
  def getCorrespondingPhrase(self, leafs, desired):
    detectionFault = None
    for leaf in leafs:
      if(leaf.getReference().getCoveredText() == desired.getCoveredText()):
        if(leaf.getReference() == desired):
          return leaf
        else:
          detectionFault = leaf;

    # if the desired leaf was not found, but only a leaf with similar text content, a detection fault might have occurred
    if(detectionFault is not None):
      print("Identified a leaf-detection-fault: mixed up two leafs with the same covered text:")
      print("  Leaf in the phrase list: " + detectionFault.getReference().getCoveredText() + " (" + str(detectionFault.getReference().getPosition()) + ")")
      print("  Desired here: " + desired.getCoveredText() + " (" + str(desired.getPosition()) + ")")
    
    return None
