'''package jfr.cerec.pattern

import java.util.ArrayList

import jfr.cerec.sentence.Fragment
import jfr.cerec.sentence.Leaf'''
#from typing import overload

class LexicalConstraintGenerator: #implements IConstraintGenerator

  topLexicalConstraintTags = ["IN", "JJ"]
  topLexicalConstraintWords = ["because", "cause", "due", "if", "when", "hence", "therefore", "after"]

  #@Override
  def differentiates(self, herd, intruder):
    wordsUsed = self.getWordsUsed(herd)
    
    for word in wordsUsed:
      if(self.isWordUniversallyUsed(herd, word) and not intruder.containsByInd(False, word)):
        return True

    return False


  #@Override
  def generateConstraints(self, herd, intruder):
    from python.pattern.LexicalConstraint import LexicalConstraint
    possibleConstraints = []   #new ArrayList<IConstraint>()
    wordsUsed = self.getWordsUsed(herd)

    # find positive constraints (words that must be used)
    for word in wordsUsed:
      candidate = LexicalConstraint(word, True)
      if(candidate.isFulilledBy(herd) and not candidate.isFulfilledBy(intruder)):
        possibleConstraints.append(candidate)

      '''/*if(isWordUniversallyUsed(herd, word) && !intruder.contains(false, word)) {
        LexicalConstraint constraint = new LexicalConstraint(word, true)
        possibleConstraints.add(constraint)
      }*/'''

    # find negative constraints (words that must not be used)
    for word in self.getWordsUsed(intruder):
      candidate = LexicalConstraint(word, False)
      if(candidate.isFulilledByNone(herd) and candidate.isFulfilledBy(intruder)):
        possibleConstraints.append(candidate)

      '''/*if(!wordsUsed.contains(word)) {
        LexicalConstraint constraint = new LexicalConstraint(word, false)
        possibleConstraints.add(constraint)
      }*/'''


    return possibleConstraints

  #@overload
  def getWordsUsed(self, lst):
    words = []  #new ArrayList<String>()
    if type(lst).__name__ != 'list':
      lst = [lst]

    for item in lst:
      for leaf in item.getAllLeafs():
        word = leaf.getCoveredText()
        if(word not in words):
          words.append(word)
    
    #print(words)
    return words


  def isWordUniversallyUsed(self, lst, word):
    for item in lst:
      if(not item.containsByInd(False, word)):
        return False

    return True
