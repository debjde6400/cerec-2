'''
/**
 *
 * @author Julian Frattini
 *
 * Interface for command generators, which are responsible for creating the genetic algorithm
 * to extract a phrase from a sentence
 */'''
from abc import ABC, abstractmethod
from python.ceg.Extractor import Extractor

class ICommandGenerator(ABC):
  
  def setOPFParser(self, opfile, annotator):
    self.opfile = opfile
    self.annotator = annotator

  '''/**
   * Genetic algorithm generating a succession of commands, which extracts the
   * given graph from the given sentence. The return value is an object containing
   * these commands and, when given a sentence of similar structure, can generate
   * the correct cause-effect-graph for its specific instance of this sentence
   * structure.
   * @param sentence The sentence, based on which a extraction algorithm is to be generated
   * @param graph Cause-effect-relation, which shall be extracted from the given sentence
   * @return Pattern containing the extraction algorithms to extract the graph from the sentence
   */'''
  def generateCommandPatterns(self, sentence, graph):
    patternRoot = graph.getRoot().createPattern(sentence, self)

    if(patternRoot.isComplete()):
      extractor = Extractor(patternRoot)
      return extractor
    else:
      # the pattern generation failed
      return None

  '''/**
   * Generates a command that extracts the given phrase from the given sentence
   * @param sentence The sentence, from which the phrase is extracted
   * @param phrase The phrase that is to be extracted
   * @return A command extracting the phrase from the sentence, null if no such command is possible
   */'''

  @abstractmethod
  def generateCommandPattern(self, sentence, phrase):
    pass