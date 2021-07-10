class Sentence:
  #private int index;
  #private Fragment root;

  #public Sentence(int index, Fragment root) {
  def __init__(self, index, root):
    self.index = index
    self.root = root

  def getIndex(self):
    return self.index

  '''
   * {@inheritDoc}
  '''
  #@Override
  def getRootConstituent(self):
    return self.root
  #}

  #public void setRoot(Fragment root) {
  def setRoot(self, root):
    self.root = root
  #}

  '''
   * {@inheritDoc}
   */
  @Override'''
  def getRootDependency(self):
    return self.root.getRootGovernor()
  
  def getSentenceText(self):
    return self.getRootConstituent().getCoveredText()

  '''
   * {@inheritDoc}

  @Override'''
  #public String toString() {
  def toString(self):
    return self.root.toString()

  #@Override
  #public String structureToString(boolean constituent) {
  def structureToString(self, constituent):
    if constituent:
      return self.root.structureToString(True)
    else:
      return self.root.getRootGovernor().structureToString(False)
