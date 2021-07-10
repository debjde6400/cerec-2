#package jfr.cerec.genetics;

class NavigationStep:
  #private String tag;
  #private int index;

  def __init__(self, tag, index):
    #super();
    self.tag = tag
    self.index = index

  def getTag(self):
    return self.tag

  def setTag(self, tag):
    self.tag = tag

  def getIndex(self):
    return self.index

  def setIndex(self, index):
    self.index = index

