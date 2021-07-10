from python.main.CerecResult import CerecResult
from python.util.Utils import Utils
'''
/**
 *
 * @author Julian Frattini
 *
 * This class was introduced for evaluation purposes, mainly considering the author's master thesis.
 * Its main purpose is to store the results of training- and testing-procedures and output these in
 * a human-readable way.
 */
'''

class EvaluationStatistics:

  #private HashMap<CerecResult, ArrayList<CausalityData>> results;

  def __init__(self, printOnlyFailingExamples):
    '''
    Storage for results, where each type of result (CerecResult) is
    associated with a list of CausalityExamples, which produced the respective result
    '''
    self.results = dict()

    '''
    True if only causality examples, which produce a negative result, shall be printed
    '''
    self.printOnlyFailingExamples = printOnlyFailingExamples

    '''
    True, if only categories, that actually occur, shall be printed
    '''
    self.printOnlyOccurringCategories = False

    #results = new HashMap<CerecResult, ArrayList<CausalityData>>();
    #for(CerecResult type : CerecResult.values()) {
    for type in CerecResult:
      self.results[type] = []


  def setPrintOnlyOccurringCategories(self, printOnlyOccurringCategories):
    self.printOnlyOccurringCategories = printOnlyOccurringCategories

  def setPrintOnlyFailingExamples(self, printOnlyFailingExamples):
    self.printOnlyFailingExamples = printOnlyFailingExamples

  def add(self, example, resultType):
    self.results[resultType].append(example)

  def getOccurrencesOf(self, type):
    return len(self.results[type])

  '''
   * Output the evaluation results as a SV-compatible String
  '''
  def getOverviewAsSeperatedValueList(self, separator):
    result = "type" + separator + "occurrences" + separator + "percentile\n"

    examples = self.getNumberOfExamples(False)

    for type in CerecResult:
      typeOccurrence = len(self.results[type])

      result = result + type.value + separator + typeOccurrence + separator + self.getPercentile(typeOccurrence, examples) + "%" + "\n";

    return result

  '''
   * Calculates the percentage of successfully processed data entries
   * @return Percentage of successfully processed data entries
  '''
  def getPercentageOfSuccessfullyProcessed(self):
    successful = self.getNumberOfExamples(True)
    examples = self.getNumberOfExamples(False)
    return self.getPercentile(successful, examples)

  '''
   * Count the number of evaluated causality examples that produced a specific result
   * @param onlySuccessful True, if only positive results shall be counted
   * @return The number of (either all or only the positive) results
  '''
  def getNumberOfExamples(self, onlySuccessful):
    result = 0
    for type in CerecResult:
      if(onlySuccessful):
        if(self.isCERecResultPositive(type)):
          result = result + len(self.results[type])

      else:
        result = result + len(self.results[type])

    return result

  '''
   * Determines, whether a specific CerecResult is considered positive or not
   * @param type The CerecResult to be evaluated
   * @return True, if the type is considered positive
  '''
  @staticmethod
  def isCERecResultPositive(type):
    if type in [CerecResult.CREATION_SUCCESSFUL, CerecResult.DISCARDING_SUCCESSFUL, CerecResult.RECOGNITION_SUCCESSFUL, CerecResult.DEFLECTION_SUCCESSFUL, CerecResult.SPECIFICATION_SUCCESSFUL]:
      return True

    return False

  '''
   * Calculates the devision between two integers and formats it with two positions after the decimal point
   * @param z Numerator
   * @param n Denominator
   * @return Division z/n
   '''
  def getPercentile(self, z, n):
    percentile = Utils.divMayBe0(z, n)
    return percentile * 100.0

  '''
   * Output the evaluation results in a human-readable form
  '''
  def print_details(self, opfile):
    #CELogger.log().print("================================================");

    opfile.writeToF1("================================================")
    successful = self.getNumberOfExamples(True)
    examples = self.getNumberOfExamples(False)
    #CELogger.log().print("Successfully processed " + successful + "/" + examples + " (" + getPercentile(successful, examples) + "%)")
    opfile.writeToF1("Successfully processed " + str(successful) + "/" + str(examples) + " (" + str(self.getPercentile(successful, examples)) + "%)")

    for type in CerecResult:
      typeOccurrence = len(self.results[type])

      if self.printOnlyOccurringCategories and typeOccurrence == 0:
        continue

      #CELogger.log().print("Examples processed with result type " + type.toString() + " (" + typeOccurrence + " times, " + getPercentile(typeOccurrence, examples) + "%): ");
      opfile.writeToF1("Examples processed with result type " + type.value + " (" + str(typeOccurrence) + " times, " + str(self.getPercentile(typeOccurrence, examples)) + "%): ")

      if(self.printOnlyFailingExamples and self.isCERecResultPositive(type)):
        # skip listing all sentences of this category if not specified to do so
        continue

      for obj in self.results[type]:
        #CELogger.log().print(" - " + obj.toString())
        opfile.writeToF1(" - " + str(obj))

    #CELogger.log().print("================================================")
    opfile.writeToF1("================================================")
