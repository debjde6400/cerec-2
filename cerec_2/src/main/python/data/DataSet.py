import random
'''package jfr.cerec.data;

import java.util.ArrayList;

/**
 *
 * @author Julian Frattini
 *
 * Container class for a list of CausalityExamples. The main purpose of this class is to
 * manage the list of examples and especially provide support for evaluation methods like
 * a cross-validation.
 */'''

class DataSet:

  def __init__(self):
    self.set = []

  def getSet(self):
    return self.set

  def setSet(self, set):
    self.set = set

  def addSet(self, set):
    self.set.extend(set)

  def __len__(self):
    return len(self.set)

  def sizeCausal(self):
    count = 0

    for c in self.set:
      if(c.isCausal()):
        count += 1

    return count

  '''
   Returns a randomly selected portion of the full set
    @param percentage Relative size of the portion given in the range of 0 to 1 (=100%)
    @return A percentage of the set of examples
   '''
  #@SuppressWarnings("unchecked")

  def getPortion(self, percentage):
    portion = []
    copy = self.set.copy()

    if(percentage == 1):
      return copy

    n = int(percentage * len(self.set))

    #for(int i = 0; i < n; i++) {
    for i in range(n):
      index = int(random.random() * len(copy))
      index = min(index, len(self.set))

      portion.append(copy.remove(index))

    return portion

  '''
   * Randomly splits the example set into two exclusive sets
   * @param ratio Relative size of set one given in the range of 0 to 1 (=100%)
   * @param one Resulting first set
   * @param two Resulting second set
   '''

  #@SuppressWarnings("unchecked")
  def split(self, ratio, one, two):
    portion = []
    copy = self.set.copy()

    n = int(ratio * len(self.set))

    for i in range(n):
      index = int(random.random() * len(copy))
      index = min(index, len(self.set))

      portion.add(copy.remove(index))

    one.setSet(portion)
    two.setSet(copy)
