from python.trainer.EvaluationStatistics import EvaluationStatistics
from tqdm import tqdm

class CauseEffectTrainer:

  def __init__(self, subject):
    self.subject = subject    #ICauseEffectRecognition subject;
    self.statistics = EvaluationStatistics(False)   #EvaluationStatistics statistics;

    #CELogger.log().initialize(System.out);

  '''
   * Execute training procedure with the given source
   * @param reader Reader that outputs a list of causality examples
  '''
  '''def train(self, reader):
    self.train(reader.readExamples())

  /**
   * Execute training procedure with the given set of examples
   * @param set Set of causality examples
   */

  def train(DataSet set) {
    train(set.getSet());
  }

  /**
   * Perform the training procedure with the given set of examples
   * @param examples Set of examples
   */
   '''

  def train(self, examples):
    #examples = reader.readExamples()
    #CELogger.log().print("============INITIALIZING TRAINING===============");
    print("\n============INITIALIZING TRAINING===============\n")
    i = 1

    for example in tqdm(examples):
      self.subject.opfile.writeToAll("\n\nSentence : " + str(i) + " ID: " + str(example.index) + "\n")
      result = self.subject.train(example)
      self.statistics.add(example, result)
      i += 1

    #CELogger.log().print("==============ENDING TRAINING================");
    print("\n==============ENDING TRAINING================\n")

  '''/**
   * Reset the statistics
   */'''

  def resetStatistics(self):
    self.statistics = EvaluationStatistics(False)

  def getStatistics(self):
    return self.statistics
