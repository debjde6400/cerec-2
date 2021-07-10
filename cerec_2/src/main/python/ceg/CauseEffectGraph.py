#package jfr.cerec.ceg;

class CauseEffectGraph: #implements ICauseEffectGraph {

  #private ICausalElement root;

  def __init__(self, root=None):
    self.root = root
    
  def getRoot(self):
    return self.root

  #@Override
  def getCause(self):
    cause = self.root.getOrigin()
    if cause is not None:
      return cause.phrase
    else:
      return ""

  #@Override
  def getEffect(self):
    effect = self.root.getTarget()
    if effect is not None:
      return effect.phrase
    else:
      return ""

  #@Override
  def __eq__(self, other):
    #print("1st: "+ str(self))
    #print("2nd: "+ str(other))
    return self.root == other.getRoot()

  #@Override
  def __str__(self):
    return str(self.root)
  
  def matchResolved(self, other, url):
     return self.root.matchResolved(other.getRoot(), url)