#package jfr.cerec.ceg;

class ICausalRelation: #extends ICausalElement {

  def __init__(self, target):
    self.target = target

  def getTarget(self):
    return self.target

  def setTarget(self, target):
    self.target = target
