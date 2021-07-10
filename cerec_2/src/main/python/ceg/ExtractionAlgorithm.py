'''package jfr.cerec.ceg;

import jfr.cerec.genetics.ICommand;
import jfr.cerec.sentence.Fragment;
import jfr.cerec.util.CELogger;

/**
 *
 * @author Julian Frattini
 * Applies an extraction algorithm to the root fragment of a sentence
 */'''

class ExtractionAlgorithm:
  #private ICommand command;
  def __init__(self, command):
    self.command = command

  def getCommand(self):
    return self.command


  '''/**
   * Applies the extraction-algorithm to a sentence in internal representation
   * @param fragment grammatical root of a sentence
   * @return the specific extracted phrase
   */'''
  def generateCEElement(self, fragment):
    if self.command is None:
      print("Command is not defined (object is null)!")
      return None

    try:
      return self.command.generateOutput(fragment).strip()

    except Exception:
      print('Value error')

    return None


  #@Override
  def toString(self):
    return self.command.toString()
