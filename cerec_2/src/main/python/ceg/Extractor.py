'''
/**
 *
 * @author Julian Frattini
 *
 * Interface of cause-effect-patterns. The purpose of a pattern is to store the two genetic algorithms,
 * which are capable of extracting the cause-/effect-expression of a sentence
 */'''

from python.ceg.CauseEffectGraph import CauseEffectGraph
class Extractor:

	#protected ICausalElement causeEffectPatternRoot;

	def __init__(self, causeEffectPatternRoot):
		self.causeEffectPatternRoot = causeEffectPatternRoot

	'''/**
	 * Executes the genetic algorithms on a given sentence in order to extract the cause-effect-graph
	 * @param sentence Sentence, where the cause- and effect-expression is to be extracted
	 * @return Cause-effect-graph representing the causal relation of the sentence
	 */'''
	def generateGraphFromSentence(self, sentence):
		causeEffectGraphRoot = self.causeEffectPatternRoot.resolvePattern(sentence.getRootConstituent())
		result = CauseEffectGraph(causeEffectGraphRoot)

		return result


	'''/**
	 * Checks, if the given cause-effect-pattern generates the desired cause-effect-graph
	 * @param sentence The sentence, from which the causality is to be extracted
	 * @param ceg The cause-effect-graph, that has to result from the extraction algorithm
	 * @return True, if the algorithms generate the desired ceg from the sentence
	 */'''

	def isApplicable(self, sentence, ceg, url):
    #TODO problem mostly attended but new changes are made
		generated = self.generateGraphFromSentence(sentence)
		return generated.matchResolved(ceg, url)
  
	def addExtractor(self, candidate, ceg, extractionAlgorithmGenerator, effect=False):
		self.causeEffectPatternRoot.addExtractor(candidate, ceg, extractionAlgorithmGenerator, effect)

	'''/**
	 * Gets all genetic algorithms in human-readable form
	 * @return The extraction algorithms of for the causal phrases in human-readable form
	 */'''
	def getCommandStrings(self):
		sb = []

		sb.append("Cause-effect graph pattern:\n" + self.causeEffectPatternRoot.toString(True, "  "))

		return ''.join(sb)
