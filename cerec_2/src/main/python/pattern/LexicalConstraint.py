from python.pattern.IConstraint import IConstraint

class LexicalConstraint(IConstraint): #extends IConstraint {

  '''private String word;

  /**
   * True, if the given word must appear, false if the given word must not appear
   */
  private boolean positive;'''

  def __init__(self, word, positive):
    self.word = word
    self.positive = positive

  def getWord(self):
    return self.word

  def setWord(self, word):
    self.word = word

  def isPositive(self):
    return self.positive

  def setPositive(self, positive):
    self.positive = positive

  #@Override
  def isFulfilledBy(self, fragment):    
    result = fragment.containsByInd(False, self.word)
    #return self.word in fragment.getCoveredText()            
    return result if self.positive else not result

  #@Override
  def generateProposal(self, fragment):
    from python.pattern.LexicalSpecificationProposal import LexicalSpecificationProposal
    return LexicalSpecificationProposal(fragment, self)

  #@Override
  def toString(self):
    return " |" + ("+" if self.positive else "-") + " " + self.word + "| "

  #@Override
  def clone(self):
    return LexicalConstraint(self.word, self.positive)

  #@Override
  def __eq__(self, other):
    if isinstance(other, LexicalConstraint):
      lc = other
      if(lc.getWord() == self.word) and (lc.isPositive() == self.positive):
        return True

    return False

