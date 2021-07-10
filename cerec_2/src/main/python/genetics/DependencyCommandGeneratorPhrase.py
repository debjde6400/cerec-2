#package jfr.cerec.genetics;

#import jfr.cerec.sentence.Leaf;

class DependencyCommandGeneratorPhrase:

  def __init__(self, reference, all):
    super().__init__()
    self.reference = reference
    self.all = all
  
  def getReference(self):
    return self.reference
  
  def setReference(self, reference):
    self.reference = reference
  
  def isAll(self):
    return self.all
  
  def setAll(self, all):
    self.all = all

