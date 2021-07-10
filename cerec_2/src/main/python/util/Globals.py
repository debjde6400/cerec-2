#package jfr.cerec.util;

'''/**
 *
 * @author Julian Frattini
 *
 * Class for global operations like distribution of sentence indices
 */'''

class Globals:
  instance = None

  '''public static Globals getInstance() {
    if(instance == null) {
      instance = new Globals();
    }
    return instance;
  }

  /**
   * index of the annotated sentences
   */
  private int sentenceCounter;

  private int patternCounter;'''

  #private Globals() {
  def __init__(self):
    self.sentenceCounter = 0
    self.patternCounter = 0

  @staticmethod
  def getInstance():
    if(Globals.instance is None):
      Globals.instance = Globals()

    return Globals.instance

  def reset(self): #{
    self.sentenceCounter = 0
    self.patternCounter = 0

  def getCurrentSentenceCounter(self):
    return self.sentenceCounter

  def getNewSentenceCounter(self):
    current = self.sentenceCounter
    self.sentenceCounter += 1
    return current

  def getNewPatternCounter(self):
    current = self.patternCounter
    self.patternCounter += 1
    return current

  def getIndentation(self, indent, times):
    result = ""

    #for(int i = 0; i < times; i++) {
    for _ in range(times):
      result = result + indent

    return result

