'''package jfr.cerec.genetics;

import java.util.ArrayList;
import java.util.StringJoiner;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.util.CELogger;

/**
 *
 * @author Julian Frattini
 *
 * Command for vertical selection. Given a sentence in the form of a tree of syntactical nodes
 * select one of a specific type/content.
 */'''
from python.genetics.ConstituentCommand import ConstituentCommand

class ConstituentCommandSelect(ConstituentCommand):

  '''/**
   * Simple selection of the current node;
   */
  private boolean take;

  /**
   * Simple selection byType of the tag / word indicator
   */
  private boolean byType;
  private String indicator;

  /**
   * Sometimes a fragment tree contains multiple nodes with identical attributes
   * (same text and type). In order to identify which fragment to chose, the selector
   * can be extended with an index.
   */
  private int index;

  /**
   * Sometimes the content of a CEElement (cause/effect) are not all grouped in
   * one exclusive branch of the constituency-tree. In this case, a governing parent
   * leaf is chosen which has a reference on all other leaf nodes relevant for the
   * CEElement.
   */
  private ArrayList<ConstituentCommandPick> horizontalSelection;

  /**
   * The positionOfSelectedBetweenHorizontalSelection is the index, at which position
   * the governing parent leaf is located between its governed references. Set this
   * value to -1 if the selected fragment should not appear at all in the chain of words
   * (applicable if the selector has to find a governor outside of the leaf chain)
   */
  private int positionOfSelectedBetweenHorizontalSelection;'''
  
  '''
  @overload
  def __init__(self):
    super();
    self.take = True
    index = 0;
    horizontalSelection = [] #new ArrayList<ConstituentCommandPick>();
  
  @overload
  def __init__(self, byType, indicator):
    super().__init__()
    self.byType = byType
    self.indicator = indicator
    self.index = 0
    self.horizontalSelection = [] # new ArrayList<ConstituentCommandPick>();
  
  @overload
  def __init__(self, byType, indicator, index):
    super().__init__()
    self.byType = byType;
    self.indicator = indicator;
    self.index = index;
  '''  
  def __init__(self, byType=False, indicator=None, index=0):
    super().__init__()
    self.horizontalSelection = []
    self.index = index
    self.byType = byType
    self.indicator = indicator
    self.positionOfSelectedBetweenHorizontalSelection = -1
    
    if(not byType and indicator is None and index == 0):
      self.take = True
      
    else:
      self.take = False

    #horizontalSelection = new ArrayList<ConstituentCommandPick>()

  #public void addHorizontalSelection(ConstituentCommandPick picker) {
  def addHorizontalSelection(self, picker):
    self.horizontalSelection.append(picker)

  def setPositionOfSelectedBetweenHorizontalSelection(self, pos):
    self.positionOfSelectedBetweenHorizontalSelection = pos
  
  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def generateOutput(self, fragment):
    selection = None

    if(self.take):
      # directly take the current fragment
      selection = fragment
      #print('Sele :  ', selection.toString(True, False))
    
    else:
      # select a certain fragment from the children of the current
      selected = []
      fragment.select(self.byType, self.indicator, selected)

      if(len(selected) > 0):
        selection = selected[self.index]
      
      elif(len(selected) == 0):
        print("CommandSelect did not identify an eligible result");
        print("Sentence under test: " + fragment.toString(False, False))
        print("  Checking for " + ("type" if self.byType else "word") + " " + self.indicator + " yielded no result")
      else:
        print("ERROR: CommandSelect yielded an unknown selection error")

    if(selection is not None):
      if(self.successor is None):
        # construct the cause-/effect-expression
        return self.constructResult(selection)
      
      else:
        # continue processing recursively
        return self.successor.generateOutput(selection)
      
    else:
      return None

  '''/**
   * Construct the cause-/effect-expression
   * @param selection fragment identified by this select command
   * @return cause-/effect-expression
   */'''
  def constructResult(self, selection):
    if(not self.horizontalSelection):
      # no horizontal selection, simply use the text covered by the selected fragment node
      return selection.getCoveredText()
    
    else:
      sj = [""] #new StringJoiner(" ");
      
      if(self.positionOfSelectedBetweenHorizontalSelection > -1):
        # horizontal selection is active and CommandPick's have to be resolved
        #print('Len : ', self.positionOfSelectedBetweenHorizontalSelection)
        result = [ None for _ in range(len(self.horizontalSelection) + 1) ]
        #print(len(result))

        # resolve all pick commands, order them in an array and place the content of the selected
        # fragment node in the according position
        for i in range(len(result)):
          if(i < self.positionOfSelectedBetweenHorizontalSelection):
            #print('Ting')
            result[i] = self.horizontalSelection[i].generateOutput(selection)
          
          elif(i == self.positionOfSelectedBetweenHorizontalSelection):
            result[i] = selection.getCoveredText()
          
          elif(i > self.positionOfSelectedBetweenHorizontalSelection):
            result[i] = self.horizontalSelection[i-1].generateOutput(selection)

        for s in result:
          # ignore all empty picker-results
          if(len(s) > 0):
            sj.append(s)
        
      else:
        for hs in self.horizontalSelection:
          sj.append(hs.generateOutput(selection))
      
      s = ' '.join(sj)
      #print('Leaf picking result: ', s)
      return s

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def toString(self):
    sb = []

    if(self.take):
      sb.append("SELECT")
      
    else:
      sb.append("SELECT " + ("<type>" if self.byType else "<word>") + " " + self.indicator)

    if(len(self.horizontalSelection) > 0):
      sj = ["& "]
      
      for picker in self.horizontalSelection:
        sj.append(picker.toString() if picker is not None else '')
        
      sb.append(" (" + ''.join(sj) + ")")

    if(self.successor is not None):
      sb.append(" --> " + self.successor.toString())

    return ''.join(sb)
  

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getFinal(self):
    if(self.successor is None):
      return self
    
    else:
      return self.successor.getFinal()
