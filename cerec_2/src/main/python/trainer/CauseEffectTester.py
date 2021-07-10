from python.trainer.EvaluationStatistics import EvaluationStatistics
from python.main.CerecResult import CerecResult
'''package jfr.cerec.trainer;

import java.util.ArrayList;

import jfr.cerec.ceg.ICauseEffectGraph;
import jfr.cerec.data.CausalityData;
import jfr.cerec.data.DataSet;
import jfr.cerec.io.ICausalityDataReader;
import jfr.cerec.main.CerecResult;
import jfr.cerec.main.ICauseEffectRecognition;
import jfr.cerec.util.CELogger;

/**
 *
 * @author Julian Frattini
 *
 * Analyzer class mainly introduced for the purpose of the author's master thesis.
 * A set of CausalityExamples are put to test in the cause-effect-recognition-system
 * and the tester evaluates, how many examples are successfully recognized
 */'''

class CauseEffectTester:
  #private ICauseEffectRecognition subject;
  #private EvaluationStatistics statistics;

  def __init__(self, subject):
    self.subject = subject
    self.statistics = EvaluationStatistics(False)
    self.statistics.setPrintOnlyOccurringCategories(True)
    #CELogger.log().initializeIfNeccessary(System.out);

  '''/**
   * Reset the statistics
   */'''
  def resetStatistics(self):
    self.statistics = EvaluationStatistics(False)
    self.statistics.setPrintOnlyOccurringCategories(True)

  def getStatistics(self):
    return self.statistics

  '''/**
   * Execute test procedure with the given source
   * @param reader Reader that outputs a list of causality examples
   */

  public void test(ICausalityDataReader reader) {
    test(reader.readExamples());
  }

  /**
   * Execute test procedure with the given set of examples
   * @param set Set of causality examples
   */
  public void test(DataSet set) {
    test(set.getSet());
  }

  /**
   * Perform the test procedure with the given set of examples
   * @param examples Set of examples
   */'''

  def test(self, reader):
    examples = reader.readExamples()
    #CELogger.log().info("============INITIALIZING TESTING===============");
    print("============INITIALIZING TESTING===============")

    for example in examples:
      result = None

      # initially check if the example is actually valid (cause-/effect-phrase a valid substring of the sentence)
      if self.subject.isExampleValid(example):
        # test the causality example on the system and catch the resulting cause-effect-graph
        ceg = self.subject.getCEG(example.getSentence());

        # evaluate the result
        if example.isCausal():
          if ceg is not None:
            if ceg == example.getCEG():
              result = CerecResult.RECOGNITION_SUCCESSFUL
            else:
              result = CerecResult.RECOGNITION_FAILED

          else:
            result = CerecResult.RECOGNITION_FAILED

        else:
          if ceg is None:
            result = CerecResult.DISCARDING_SUCCESSFUL
          else:
            result = CerecResult.DISCARDING_FAILED

      else:
        # invalid example
        result = CerecResult.RECOGNITION_IMPOSSIBLE

      self.statistics.add(example, result)

    #CELogger.log().info("==============ENDING TESTING================")
    print("==============ENDING TESTING================")
