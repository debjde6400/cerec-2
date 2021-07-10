from abc import ABC, abstractmethod
from typing import overload
#from multipledispatch import dispatch
'''package jfr.cerec.sentence;

import java.util.ArrayList;

/**
 *
 * @author Julian Frattini
 *
 * Superclass of nodes for the internal representation. Subclasses are nodes (for inner nodes)
 * and leafs (for leaf nodes), where the latter also contain information of the dependency parser.
 */'''

#public abstract class Fragment {
class Fragment(ABC):

  '''private Fragment parent;

  private String tag;
  private String coveredText;

  private int index;'''

  #public Fragment(String tag, String coveredText, int index) {
  def __init__(self, tag, coveredText, index):
    self.parent = None
    self.tag = tag
    self.coveredText = coveredText
    self.index = index

  '''/**
   * Gets the parenting fragment of the current fragment
   * @return The parenting fragment, if it exists
   */'''
  def getParent(self):
    return self.parent

  '''/**
   * Sets the parenting fragment
   * @param parent The parent fragment of this fragment
   */'''
  def setParent(self, parent):
    self.parent = parent

  '''/**
   * Gets the type of this fragment, which is either the part-of-speech-tag (for leaf nodes)
   * or the constituency tag (for inner nodes)
   * @return Type of this fragment
   */'''
  def getTag(self):
    return self.tag

  '''/**
   * Sets the type of this fragment
   * @param tag The new type of this fragment
   */'''
  def setTag(self, tag):
    self.tag = tag

  '''/**
   * Gets the text covered by this fragment, which is either the word (for leaf nodes) or the
   * combination of all words of the leaf nodes which are parented by this fragment (for inner nodes)
   * @return The text covered by this fragment
   */'''
  def getCoveredText(self):
    return self.coveredText

  '''/**
   * Sets the covered text of this fragment
   * @param coveredText Text that is be covered by this fragment
   */'''

  def setCoveredText(self, coveredText):
    self.coveredText = coveredText

  def getIndex(self):
    return self.index

  def setIndex(self, index):
    self.index = index

  #public abstract int getDepth();
  @abstractmethod
  def getDepth(self):
    pass

  '''/**
   * Returns the begin index of the first leaf node within this fragment
   * @return Position of the first leaf in this fragment
   */'''
  #public abstract int getPosition();
  @abstractmethod
  def getPosition(self):
    pass

  '''/**
   * Selects a child according to its index position
   * @param index The position of the child among its parents children
   * @return The child node at the given index position
   */'''
  #public abstract Fragment getChildByIndex(int index);
  @abstractmethod
  def getChildByIndex(self, index):
    pass

  '''/**
   * Returns all child nodes of the current fragment
   * @return Child nodes of this fragment
   */'''
  #public abstract ArrayList<Fragment> getChildren();
  @abstractmethod
  def getChildren(self):
    pass

  '''/**
   * Checks, if the given fragment is either a direct or a transitive child of this fragment
   * @param other The assumed child fragment
   * @return True, if the other fragment is parented euther directly or transitively by this fragment
   */'''
  #public abstract boolean isParenting(Fragment other);
  @abstractmethod
  def isParenting(self, other):
    pass

  '''/**
   * Gathers all leaf nodes directly or transitively associated with this fragment
   * @return All leaf nodes related to this fragment
   */'''
  #public abstract ArrayList<Leaf> getAllLeafs();
  @abstractmethod
  def getAllLeafs(self):
    pass

  '''/**
   * Searches for a leaf node specified by its lexical index in the sentence. This allows for the most
   * specific search for a token
   * @param beginIndex Index, at what position the covered text of the leaf starts in the sentence
   * @return The leaf node, where the covered text starts at position beginIndex
   */'''
  #public abstract Leaf getLeafByBeginIndex(int beginIndex);
  @abstractmethod
  def getLeafByBeginIndex(self, beginIndex):
    pass

  '''/**
   * Searches for the leaf node, which is the root governor in the dependency relation tree
   * @return Leaf node with dependency relation type ROOT
   */'''
  #public abstract Leaf getRootGovernor();
  @abstractmethod
  def getRootGovernor(self):
    pass

  '''/**
   * Splits the fragment and yields all child nodes of this fragment
   * @return All child nodes of this fragment
   */'''
  #public abstract ArrayList<Fragment> split();
  @abstractmethod
  def split(self):
    pass

  '''/**
   * Gathers all direct or transitive child nodes of the fragment that comply to the search criteria
   * @param byType True, if the desired nodes shall be searched for by tag, false if by word
   * @param indicator Either the tag or the word, which the nodes have to contain
   * @param selected The (initially) empty list in which the results will be stored
   * @return The selected-list filled with all child nodes that comply to the search criteria
   */'''
  #public abstract ArrayList<Fragment> getBy(boolean byType, String indicator, ArrayList<Fragment> selected);
  @abstractmethod
  def getBy(self, byType, indicator, selected):
    pass

  '''/**
   * Gathers all leaf nodes of the fragment that comply to the search criteria
   * @param byType True, if the desired nodes shall be searched for by tag, false if by word
   * @param indicator Either the tag or the word, which the nodes have to contain
   * @param selected The (initially) empty list in which the results will be stored
   * @return The selected-list filled with all leaf nodes that comply to the search criteria
   */'''
  #public abstract ArrayList<Leaf> getLeafs(boolean byType, String indicator, ArrayList<Leaf> selected);
  @abstractmethod
  def getLeafs(self, byType, indicator, selected):
    pass

  '''/**
   * Checks, whether one of the child nodes of this fragment parents the given node
   * @param child The node, where the parent node is of interest
   * @return The child node which parents the given node, if it does so
   */'''
  #public abstract Fragment getParentOf(Fragment child);
  @abstractmethod
  def getParentOf(self, child):
    pass

  '''/**
   * Checks, whether one of the child nodes of this fragment directly parents the given node
   * @param child The node, where the parent node is of interest
   * @return The child node which directly parents the given node, if it does so
   */'''
  #public abstract Fragment getDirectParentOf(Fragment child);
  @abstractmethod
  def getDirectParentOf(self, child):
    pass

  '''/**
   * Gathers all direct or transitive child nodes of the fragment that comply to the search criteria.
   * This method only takes into account the first node of one branch which complies to the criteria and
   * will disregard all following potential nodes of the branch.
   * @param byType True, if the desired nodes shall be searched for by tag, false if by word
   * @param indicator Either the tag or the word, which the nodes have to contain
   * @param selected The (initially) empty list in which the results will be stored
   * @return The selected-list filled with all child nodes that comply to the search criteria
   */'''
  #public abstract ArrayList<Fragment> select(boolean byType, String indicator, ArrayList<Fragment> selected);
  @abstractmethod
  def select(self, byType, indicator, selected):
    pass

  '''/**
   * Checks whether either this node or any of its child nodes complies to the specified criteria
   * @param byType True, if the desired nodes shall be searched for by tag, false if by word
   * @param indicator Either the tag or the word, which the nodes have to contain
   * @return True, if the specified node is contained within the branch spanned from this fragment
   */'''
  #public abstract boolean contains(boolean byType, String indicator);
  @abstractmethod
  def containsByInd(self, byType, indicator):
    pass

  '''/**
   * Checks whether either this node or any of its child nodes complies to the given fragment
   * @param fragment The fragment, which is inspected to be contained
   * @return True, if the specified node is contained within the branch spanned from this fragment
   */'''
  #public abstract boolean contains(Fragment fragment);
  @abstractmethod
  #@overload
  def contains(self, fragment):
    pass

  '''/**
   * Gathers all fragments, where the combination of their covered texts composes the expression
   * @param expression The desired expression
   * @return List of Fragments that together compose the expression
   */'''
  #public abstract ArrayList<Fragment> getCompositionFor(String expression);
  @abstractmethod
  def getCompositionFor(self, expression):
    pass

  '''/**
   * Formats the fragment structure into human-readable output
   * @param structurized True, if the syntactical structure (constituents) shall be displayed
   * @param dependencies True, if the semantical structure (dependencies) shall be displayed
   * @return The fragments content in human-readable form
   */'''
  #public abstract String toString(boolean structurized, boolean dependencies);
  @abstractmethod
  @overload
  def toString(self, structurized, dependencies):
    pass

  '''/**
   * Formats the fragment structure into a human readable output with line breaks and indentation
   * @param indent Indentation of the current line, usually 0 to begin with
   * @param showConstituentText True, if the covered text of consitutents shall be displayed
   * @return The fragment structure (with constituents and dependencies) in a multi-line form
   */'''
  #public abstract String toString(int indent, boolean showConstituentText);
  @abstractmethod
  @overload
  def toString(self, indent, showConstituentText):
    pass

  '''/**
   * Formats the fragment structure into human-readable output
   * @param highlights List of words, which will be highlighted in the sentence output
   * @return The fragments content in human-readable form
   */'''
  @abstractmethod
  #public abstract String toString(ArrayList<Fragment> highlights);
  def toString(self, highlights):
    pass

  '''/**
   * Formats the fragments structure disregarding leaf nodes into human-readable output
   * @param constituent True for constituent structure, false for dependency structure
   * @return The sentence structure of the fragment
   */'''
  #public abstract String structureToString(boolean constituent);
  @abstractmethod
  def structureToString(self, constituent):
    pass

  '''/**
   * Counts the number of nodes of the tree spanned from this node
   * @return The number of nodes parented by this node
   */'''
  #public abstract int size();
  @abstractmethod
  def size(self):
    pass
