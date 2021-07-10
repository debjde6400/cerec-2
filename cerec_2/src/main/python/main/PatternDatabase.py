'''package jfr.cerec.main;

import java.util.ArrayList;

import jfr.cerec.pattern.IPattern;
import jfr.cerec.sentence.ISentence;'''
#from typing import overload
from multipledispatch import dispatch
from python.sentence.Sentence import Sentence

class PatternDatabase:

  '''/**
   * List of all patterns, that have been trained, where each pattern represents one
   * grammatical structure and a corresponding cause- and effect-extraction algorithm
   */
  private ArrayList<IPattern> patterns;

  public PatternDatabase() {
    patterns = new ArrayList<IPattern>();
  }'''
  
  def __init__(self, patterns=None):
    #super();
    if patterns is None:
      self.patterns = []
    else:
      self.patterns = patterns
  
  def setOPFile(self, opfile):
    self.opfile = opfile

  def getPatterns(self):
    return self.patterns
  
  def addPattern(self, pattern):
    self.patterns.append(pattern)
  
  def reset(self):
    self.patterns = []
  
  '''/**
   * Get the pattern, to which the sentence complies, with the maximal precision score
   * @param sentence The sentence, for which a complying pattern is searched
   * @return The complying pattern with the highest precision score from the existing patterns
   */'''
  #@overload
  @dispatch(Sentence)
  def getMostPrecisePattern(self, sentence):
    return self.getMostPrecisePattern(self.patterns, sentence)
  
  '''/**
   * Get the pattern, to which the sentence complies, with the maximal precision score
   * @param sentence The sentence, for which a complying pattern is searched
   * @return The complying pattern with the highest precision score
   */'''
  #@overload
  @dispatch(list, Sentence)
  def getMostPrecisePattern(self, eligiblePatterns, sentence):
    complying = [] #new ArrayList<IPattern>();
    # find all complying patterns
    if not eligiblePatterns:
      #sprint('No pattern present')
      return None
      
    for pattern in eligiblePatterns:
      if(pattern.isCompliant(sentence)):
        complying.append(pattern)
    
    # identify the pattern with the highest precision score
    maxPrecision = 0.0
    eligiblePattern = None
    for pattern in complying:
      if(pattern.getPrecisionScore() > maxPrecision):
        maxPrecision = pattern.getPrecisionScore()
        eligiblePattern = pattern
    
    if eligiblePattern is not None:
      self.opfile.writeToF2("Result: " + eligiblePattern.toString())
    return eligiblePattern
