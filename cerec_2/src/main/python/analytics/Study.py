from python.trainer.CauseEffectTester import CauseEffectTester
from python.trainer.CauseEffectTrainer import CauseEffectTrainer
from python.trainer.EvaluationStatistics import EvaluationStatistics
from python.io.OPFile import OPFile
from python.main.CerecResult import CerecResult
from python.data.DataSet import DataSet
from python.util.Utils import Utils
import random

class Study:

  def __init__(self, cerec, label, prev_patts=[], non_causals_all=[], folderName=None):
    self.label = label
    self.opfile = OPFile('./resources/output/', self.label, folderName)
    self.cerec = cerec
    self.trainer = CauseEffectTrainer(self.cerec)
    self.tester = CauseEffectTester(self.cerec)
    self.set1 = None
    self.set2 = None
    self.train_Portion = 1.0
    self.iterations = 0
    self.prev_patts = prev_patts
    self.non_causals_all = non_causals_all
    
  def __del__(self):
    del self.opfile

  def getSet1(self):
    return self.set1

  def setSet1(self, set1):
    """

    :param set1: 

    """
    self.set1 = set1

  def getSet2(self):
    """ """
    return self.set2

  def setSet2(self, set2):
    """

    :param set2: 

    """
    self.set2 = set2

  def getIterations(self):
    return self.iterations

  def setIterations(self, iterations):
    """

    :param iterations: 

    """
    self.iterations = iterations

  def getTrainPortion(self):
    return self.trainPortion

  def setTrainPortion(self, trainPortion):
    """

    :param trainPortion: 

    """
    self.trainPortion = trainPortion

  def reset(self):
    self.cerec.reset()
    self.trainer.resetStatistics()
    self.tester.resetStatistics()

  def perform(self):
    self.cerec.setOPFile(self.opfile)
    results = [[None for _ in range(self.iterations+3)] for _ in range(len(CerecResult) + 3)]
    iterativeResults = dict()
    for type in CerecResult:
      iterativeResults[type] = []

    evaluatedSet = None
    if(self.set2 is None):
      if not self.prev_patts:
        #RQ 1
        evaluatedSet = self.set1
        for i in range(self.iterations):
          self.cerec.opfile.writeToAll(f"ITERATION :: {i+1}\n")
          print(f"ITERATION :: {i+1}\n")
          self.reset()
          trainingResult = self.train(self.set1, 1)
          for type in CerecResult:
            occurrences = trainingResult.getOccurrencesOf(type)
            iterativeResults[type].append(occurrences)
      else:
        # RQ3
        evaluatedSet = self.set1
        for i in range(self.iterations):
          self.reset()
          self.cerec.patterns.patterns = self.prev_patts
          self.cerec.noncausals = self.non_causals_all
          self.cerec.opfile.writeToAll(f"ITERATION :: {i+1}\n")
          print(f"ITERATION :: {i+1}\n")
          trainingResult = self.train(self.set1, 1)
          for type in CerecResult:
            occurrences = trainingResult.getOccurrencesOf(type)
            iterativeResults[type].append(occurrences)


    else:
      # RQ 2, two-set study: with previous training
      evaluatedSet = self.set2
      self.cerec.reset()
      
      # train CEREC with the training set
      self.cerec.opfile.writeToF1("Previous training on other sets...\n")
      self.train(self.set1, 1)
      
      # snapshot the current database of patterns
      self.cerec.snapshot()
      
      for i in range(self.iterations):
        # reset CEREC to the initial training status
        self.trainer.resetStatistics()
        self.tester.resetStatistics()
        self.cerec.restore()

        # test CEREC with the test set
        self.cerec.opfile.writeToF1("\n\nStudy on the concerned dataset...\n")
        trainingResult = self.train(self.set2, 1)
        for type in CerecResult:
          occurrences = trainingResult.getOccurrencesOf(type)
          iterativeResults[type].append(occurrences)


    # Create output overview
    # header row
    for i in range(self.iterations):
      results[0][i+1] = str(i)

    results[0][self.iterations+1] = "mean"
    results[0][self.iterations+2] = "percent"
    meanOccurrence = dict()

    # value rows
    row = 1
    for type in CerecResult:
      results[row][0] = type.value

      allOccurrences = 0.0
      for i in range(self.iterations):
        occurrencesInIteration = iterativeResults[type][i]
        allOccurrences += occurrencesInIteration
        results[row][i+1] = str(occurrencesInIteration)

      meanOccurrences = allOccurrences / self.iterations
      meanOccurrence[type] = meanOccurrences
      results[row][1+ self.iterations] = meanOccurrences
      results[row][2+ self.iterations] = str(Utils.divMayBe0(meanOccurrences, len(evaluatedSet)) * 100) + "%"
      row +=1

    # measure rows
    results[row][0] = "successrate"
    overallSuccess = 0.0
    for i in range(self.iterations):
      successInIteration = self.getSuccessCount(iterativeResults, i)
      overallSuccess += successInIteration
      results[row][1+i] = str(successInIteration)

    meanSuccess = overallSuccess/ self.iterations
    results[row][1+self.iterations] = str(meanSuccess)
    results[row][2+self.iterations] = str(Utils.divMayBe0(meanSuccess, len(evaluatedSet)) * 100) + "%"
    row += 1

    results[row][0] = "recognitionrate"
    overalRecognition = 0
    for i in range(self.iterations):
      recognitionInIteration = self.getRecognitionCount(iterativeResults, i)
      overalRecognition += recognitionInIteration
      results[row][1+i] = str(recognitionInIteration)

    meanRecognition = overalRecognition/ self.iterations
    results[row][1+self.iterations] = str(meanRecognition)
    results[row][2+self.iterations] = str(Utils.divMayBe0(meanRecognition, evaluatedSet.sizeCausal()) * 100) + "%"

    self.cerec.opfile.writeToF1("\n" + str(results))

    # Create LaTeX-conform table output
    # general information: artifact name, number of sentences, number of causal sentences
    name = self.label
    n = len(evaluatedSet)
    n_causal = evaluatedSet.sizeCausal()

    # measure 1: classification of a sentence as causal measures
    truePositives1 = meanOccurrence[CerecResult.RECOGNITION_SUCCESSFUL] + meanOccurrence[CerecResult.SPECIFICATION_SUCCESSFUL] +meanOccurrence[CerecResult.SPECIFICATION_FAILED]
    selectedElements1 = truePositives1 + meanOccurrence[CerecResult.DEFLECTION_SUCCESSFUL] + meanOccurrence[CerecResult.DEFLECTION_FAILED]
    relevantElements1 = n_causal

    # precision, recall, f-score
    precision1 = Utils.divMayBe0(truePositives1, selectedElements1) * 100
    recall1 = Utils.divMayBe0(truePositives1, relevantElements1) * 100
    fscore1 = Utils.divMayBe0(2 * (precision1 * recall1), (precision1 + recall1))

    # measure 2: correct extraction of a sentence's causality measures
    truePositives2 = meanOccurrence[CerecResult.RECOGNITION_SUCCESSFUL]
    selectedElements2 = meanOccurrence[CerecResult.RECOGNITION_SUCCESSFUL] + meanOccurrence[CerecResult.DEFLECTION_SUCCESSFUL] +         meanOccurrence[CerecResult.DEFLECTION_FAILED]
    relevantElements2 = n_causal
    
    # precision, recall, f-score
    precision2 = Utils.divMayBe0(truePositives2, selectedElements2) * 100
    recall2 = Utils.divMayBe0(truePositives2, relevantElements2) * 100
    fscore2 = Utils.divMayBe0(2 * (precision2 * recall2), (precision2 + recall2))

    tablerow = name + " | " + str(n) + " & " + str(n_causal) + " & " + str(precision1) + " & " + str(recall1) + " & " + str(fscore1) + " & " + str(precision2) + " & " + str(recall2) + " & " + str(fscore2)
    self.cerec.opfile.writeToF1("\n -----------------------------")
    self.cerec.opfile.writeToF1("Total sentences: " + str(n))
    self.cerec.opfile.writeToF1("Causal sentences: " + str(n_causal))
    self.cerec.opfile.writeToF1("\nDetection --")
    self.cerec.opfile.writeToF1("Precision: " + str(precision1) + "%")
    self.cerec.opfile.writeToF1("Recall: " + str(recall1) + "%")
    self.cerec.opfile.writeToF1("F1 score: " + str(fscore1) + "%")
    self.cerec.opfile.writeToF1("\nExtraction --")
    self.cerec.opfile.writeToF1("Precision: " + str(precision2) + "%")
    self.cerec.opfile.writeToF1("Recall: " + str(recall2) + "%")
    self.cerec.opfile.writeToF1("F1 score: " + str(fscore2) + "%")
    return tablerow

  def getSuccessCount(self, iterativeResults, iteration):
    """

    :param iterativeResults: 
    :param iteration: 

    """
    success = 0

    for type in CerecResult:
      if(EvaluationStatistics.isCERecResultPositive(type)):
        success += iterativeResults[type][iteration]

    return success

  def getRecognitionCount(self, iterativeResults, iteration):
    """

    :param iterativeResults: 
    :param iteration: 

    """
    success = 0
    success += iterativeResults[CerecResult.RECOGNITION_SUCCESSFUL][iteration]
    return success

  def train(self, set, portion):
    """Train the database of pattern with a set of training files.

    :param set: Dataset
    :param portion: float
    :returns: Statistics related to training

    """
    
    trainingData = set.getPortion(portion)
    random.shuffle(trainingData)
    self.trainer.train(trainingData)
    statistics = self.trainer.getStatistics()
    self.outputStatistics(statistics)
    return statistics

  def test(self, set):
    """Automatically testing all provided test data sets.

    :param set: Dataset
    :returns: Statistics related to testing

    """
    self.tester.test(set)
    statistics = self.tester.getStatistics()
    self.outputStatistics(statistics)
    return statistics

  '''**
   * Splits the training data into two parts, trains with one and tests with the other
   * @param segment Percentage [0, 1.0] of testing data
   *
  def trainAndTestRandomPortion(self, set, segment):
    """

    :param set: 
    :param segment: 

    """
    # split the set
    trainingData = DataSet()
    testingData = DataSet()
    set.split(segment, testingData, trainingData)

    # perform training
    self.trainer.train(trainingData)
    self.outputStatistics(self.trainer.getStatistics())

    # perform testing
    self.tester.test(testingData)
    statistics = self.tester.getStatistics()
    self.outputStatistics(statistics)
    return statistics
  '''

  def trainAndTestRandomPortion(self, set, segment, evolution=None):
    """Trains the system and with a portion of the training data.

    :param segment: Percentage
    :param evolution: Percentage (Default value = None)
    :param set: 

    """
    if evolution is not None:
      set.setSet(set.getPortion(evolution))

    # split the set
    trainingData = DataSet()
    testingData = DataSet()
    set.split(segment, testingData, trainingData)

    # perform training
    self.trainer.train(trainingData)
    self.outputStatistics(self.trainer.getStatistics())

    # perform testing
    self.tester.test(testingData)
    statistics = self.tester.getStatistics()
    self.outputStatistics(statistics)
    return statistics

  def outputStatistics(self, statistics):
    """

    :param statistics: 

    """
    statistics.setPrintOnlyOccurringCategories(True)
    statistics.setPrintOnlyFailingExamples(True)
    statistics.print_details(self.cerec.opfile)
    
  def savePatterns(self):
    ''' Patterns are saved in binary files for future use '''
    self.opfile.savePatterns(self.cerec.patterns)
    
  def saveNonCausals(self):
    ''' Non causals are saved in binary files for future use '''
    self.opfile.saveNonCausals(self.cerec.noncausals)