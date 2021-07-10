'''package jfr.cerec.util;

import java.util.ArrayList;

import jfr.cerec.sentence.Leaf;

/**
 *
 * @author Julian Frattini
 *
 * Utility class with universally applicable operations which may be used in multiple instances
 */'''
#from typing import overload
#from multipledispatch import dispatch
import re

class Utils:

  '''/**
   * Generates a list from an array without a given exception
   * @param list The array of strings, where one string shall be removed
   * @param except The exception, which has to be removed
   * @return List of String where the exception has been removed
   */'''
  #@overload
  @staticmethod
  #@dispatch(list, str)
  def generateListWithout(lst, excpt):
    st = []

    for item in lst:
      if(not item == excpt):
        st.append(item)

    return st

  '''/**
   * Generates a new list of leafs from an existing one with the exception of one leaf
   * @param leafs The list of leaf nodes, where one leaf shall be removed
   * @param except The exception, which has to be removed
   * @return List of leaf nodes where the exception has been removed
   */
  @overload
  @staticmethod
  def generateListWithout(leafs, excpt):
    st = []

    for leaf in leafs:
      if(not leaf.equals(excpt)):
        st.append(leaf)

    return st'''

  '''/**
   * Get the index of a word within an expression
   * @param expression The expression covering the word
   * @param word The word, where the index is of interest
   * @return The index of the word within the expression
   */'''
  @staticmethod
  def getPositionOfWordInExpression(expression, word):
    splt = expression.split(" ")

    for i in range(len(splt)):
      if(splt[i] == word):
        return i

    return 0


  contractions = ["'s", "n't"]
  punctuationsPrefix =[",", ";", ":", "]", "/"]
  punctuationsSuffix = ["[", "/"] # "'"

  @staticmethod
  def resolveContractions(phrase, add):
    return Utils.resolvePrefix(phrase, Utils.contractions, add)

  @staticmethod
  def resolvePunctuations(phrase, add):
    phrase = re.sub("\s\((\S[^)]+)\)(\s?)", r" ( \1 )\2", phrase).strip()
    phrase = re.sub("\s\<([^\>]+\s[^\>]*)\>\s?", r" < \1 > ", phrase).strip()
    phrase = re.sub("(\S*)\s?(\"|\/)\s?(\S*)", r"\1 \2 \3", phrase).strip()
    phrase = re.sub("(\w)\.\s+(\w)\.(\s?)", r"\1.\2.\3", phrase).strip()
    phrase = Utils.resolveHyphen(phrase)
    return Utils.resolveSuffix(Utils.resolvePrefix(phrase, Utils.punctuationsPrefix, add), Utils.punctuationsSuffix, add)

  @staticmethod
  def resolvePrefix(phrase, lst, add):
    result = phrase
    for item in lst:      
      if(add):
        result = result.replace(item, " " + item) if " " + item not in result else result
      
      else:
        result = result.replace(" " + item, item)
        
      #if item == '.':
      #  result = re.sub("(\w)\s\.\B", r"\1.", result)

    return result

  @staticmethod
  def resolveSuffix(phrase, lst, add):
    result = phrase
    
    for item in lst:
      if(add):
        if item == '(':
          if 'role(' in result:
            result = result.replace('role(', 'role (')
            
        result = result.replace(item, item + " ") if item + " " not in result else result
        
        #if 'etc .' in result:
        #  result = result.replace('etc .', 'etc. .')
        
      else:
        if item == '(':
          if 'role (' in result:
            result = result.replace('role (', 'role(')
        
        result = result.replace(item + " ", item)
        
        #if 'etc..' in result:
        #  result = result.replace('etc..', 'etc.')

    return result
  
  @staticmethod
  def resolveHyphen(phrase):
    l1 = phrase.split(' ')
    i = 0
    while i in range(len(l1)):
      if '-' in l1[i]:
        if len(l1[i].strip()) == 1:
          l1[i] = l1[i].strip()
          i += 1
          continue
      
        pts = l1[i].split('-')
        
        if pts[0].lower() not in ['non', 'anti', 'e', 're', 'pre', 'multi', ' ']:
          l1[i] = pts[0]
          l1.insert(i+1, '-')
          l1.insert(i+2, pts[1])
          i += 2
      i += 1
          
    return ' '.join(l1)
      
  @staticmethod
  def breakWordsAccToParsing(phrase):
    # There are some words which have been parsed differently by parser, so leaf chain cannot be generated. They are handled.
    words = phrase.split(' ')
    for i, w in enumerate(words):
      if w == 'cannot':
        words[i] = 'can'
        words.insert(i+1, 'not')
    
    return ' '.join(words)
    

  @staticmethod
  def numberOfOccurrences(sentence, phrase_s):
    count = 0
    if type(phrase_s).__name__ == 'list':
      for phrase in phrase_s:
        count = count + Utils.numberOfOccurrences(sentence, phrase)

      return count

  #public static int numberOfOccurrences(String sentence, String phrase) {
    else:
      lastIndex = 0
      count = 0

      while(lastIndex > -1):
        lastIndex = sentence.find(phrase_s, lastIndex)

        if(lastIndex != -1):
            count += 1
            lastIndex += len(phrase)
    return count

  '''@staticmethod
  def cutDouble(d):
    if(d != d):
      intermediate = int(d*10000)
      return intermediate/100.0
    return 0'''
  
  @staticmethod
  def divMayBe0(num, den):
    if den == 0:
      return 0
    return num / den