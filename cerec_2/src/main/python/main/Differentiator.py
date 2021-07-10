from python.main.CerecResult import CerecResult
from python.pattern.Pattern import Pattern
from python.util.Globals import Globals
from python.util.GlobalConfiguration import GlobalConfiguration

class Differentiator:
  
  '''/**
   * Reference to the database of patterns, to which a set of differentiated patterns can be added
   */
  private PatternDatabase patterns;
  
  /**
   * Reference to the command generator, which will generate a new extraction algorithm for a
   * causal intruder. Causal intruders need a new extraction algorithm because them being 
   * not applicable to the extraction algorithm of a compliant pattern triggered the differentiation
   * in the first place
   */
  private ICommandGenerator extractionAlgorithmGenerator;
  
  /**
   * List of constraint generators which the differentiator can utilize in order to imply
   * constraints to differentiate patterns from intruding sentences
   */
  private ArrayList<IConstraintGenerator> constraintGenerators;
  
  /**
   * Generates a differentiator class dedicated to differentiate existing patterns from intruders
   * @param patterns Reference to the database of patterns
   * @param extractionAlgorithmGenerator Reference to the command generator
   */'''
  #public Differentiator(PatternDatabase patterns, ICommandGenerator extractionAlgorithmGenerator) {
  def __init__(self, patterns, extractionAlgorithmGenerator):
    self.patterns = patterns
    self.extractionAlgorithmGenerator = extractionAlgorithmGenerator
    self.constraintGenerators = [] #new ArrayList<IConstraintGenerator>();  
  
  def setOPFile(self, opfile):
    self.opfile = opfile
  
  '''/**
   * Subscribe a new type of constraints to the differentiator
   * @param generator New constraint generator
   */'''
  def addConstraintGenerator(self, generator):
    self.constraintGenerators.append(generator)
  
  '''/**
   * Attempts to differentiate the given pattern from the intruder and adapts the patterns
   * @param currentPattern Pattern, to which the intruder is erroneously compliant 
   * @param intruder Sentence, which is compliant to but not applicable by the given pattern
   * @param intruderCEG Desired cause-effect-graph representing the intruders causal relation, if existing
   * @param maintainIntruder True, if the intruder is causal itself
   * @return CerecResult depending on the success of the differentiation
   */'''
  def differentiate(self, currentPattern, intruder, intruderCEG, maintainIntruder):
    # generate specification proposals based on whether the intruder shall be maintained or not
    specificationProposals = [] #new ArrayList<SpecificationProposal>();
    if(GlobalConfiguration.incrementalSentenceStructure):
      structuralSpecification = currentPattern.specifyVersus(intruder, maintainIntruder)
      if(structuralSpecification is not None):
        specificationProposals.extend(structuralSpecification)

    # find all variants for specification via constraints
    constraintSpecification = currentPattern.differentiate(intruder, self.constraintGenerators)
    if(constraintSpecification is not None):
      specificationProposals.extend(constraintSpecification)
      
    #print([s.toString() for s in specificationProposals])
    
    # if no specifications could be generated at all, the differentiation failed
    if(not specificationProposals):
      return CerecResult.SPECIFICATION_FAILED
    
    else:
      # if specifications could be generated, get the most eligible one
      #specificationProposals.sort((sp1, sp2) -> ((int) (sp2.getPrecision()-sp1.getPrecision())));
      #print([s.getPrecision() for s in specificationProposals])
      
      specificationProposals.sort(key= lambda sp: sp.getPrecision(), reverse=True)
      
      #self.opfile.writeToF2([s.toString() for s in specificationProposals])
      
      mostEligible = specificationProposals[0]
      specificationProposals = [] #new ArrayList<SpecificationProposal>();
      specificationProposals.append(mostEligible)
      
      if(maintainIntruder):
        # if the intruder is also causal, establish a counterpart specification for it
        specificationProposals.append(mostEligible.getCounterpart())

    # resolve specification proposals and retrieve potential patterns
    resultingPatterns = self.resolveSpecificationProposals(currentPattern, specificationProposals)
    
    # gather sentences for redistribution
    sentencesForRedistribution = currentPattern.getAccepted()
    if(maintainIntruder):
      sentencesForRedistribution.append(intruder)
    
    # redistribute sentences
    for sentence in sentencesForRedistribution:
      eligiblePattern = self.patterns.getMostPrecisePattern(resultingPatterns, sentence)
      if(eligiblePattern is not None):
        eligiblePattern.addSentence(sentence)
      
      else:
        if(maintainIntruder):
          sentencesForRedistribution.remove(intruder)
        
        #return (CerecResult.SPECIFICATION_FAILED, currentPattern)
        return CerecResult.SPECIFICATION_FAILED
      
    # check if the sentences have all been redistributed
    sentencesRedistributed = self.checkPatternDistribution(resultingPatterns, sentencesForRedistribution)
    
    if(not sentencesRedistributed):
      if(maintainIntruder):
        sentencesForRedistribution.remove(intruder)
      
      #return (CerecResult.SPECIFICATION_FAILED,  currentPattern)
      return CerecResult.SPECIFICATION_FAILED
    
    # check if the intruder is now isolated in his own pattern
    if(maintainIntruder):
      intruderIsolated = self.checkIntruderIsolation(resultingPatterns, intruder)
      if(not intruderIsolated):
        if(maintainIntruder):
          sentencesForRedistribution.remove(intruder)
        
        #return (CerecResult.SPECIFICATION_FAILED, currentPattern)
        return CerecResult.SPECIFICATION_FAILED
      
      intruderHandled = self.handleIntruderPattern(resultingPatterns, intruder, maintainIntruder, intruderCEG)
      if(not intruderHandled):
        # this might be due to the fact that no extraction algorithm could be generated for the intruder
        if(maintainIntruder):
          sentencesForRedistribution.remove(intruder)
        
        #return (CerecResult.SPECIFICATION_FAILED, currentPattern)
        
        return CerecResult.SPECIFICATION_FAILED
      

    if(GlobalConfiguration.incrementalSentenceStructure):
      # reevaluate the constraint positions in each pattern
      for pattern in resultingPatterns:
        pattern.reevaluateConstraints()
        
    #self.opfile.writeToF2('Resulting pat str - ' + str([p.getStructure().toString() for p in resultingPatterns]))
    
    # replace the prime pattern with its substitute from the list of generated patterns
    self.overridePrime(currentPattern, resultingPatterns)
    
    # add all generated patterns to the pattern database
    for p in resultingPatterns:
      self.patterns.addPattern(p)
    
    return CerecResult.SPECIFICATION_SUCCESSFUL
  
  '''/**
   * Attempts to differentiate a given pattern from a list of non-causal sentences
   * @param currentPattern Given pattern, that shall be non-compliant to the non-causal sentences
   * @param noncausals List of non-causal sentences
   * @return CerecResult depending on the success of the deflection
   */'''
  def deflectFromNoncausal(self, currentPattern, noncausals):
    undeflectables = [] #new ArrayList<ISentence>();
    
    for sentence in noncausals:
      self.opfile.writeToF2("\nNon causal: " + sentence.getRootConstituent().toString(True, True))
      self.opfile.writeToF2("\nCurrent pattern: " + currentPattern.getStructure().toString())
      deflectionResult = self.differentiate(currentPattern, sentence, None, False)
      #self.opfile.writeToF2("Result: " + str(deflectionResult))
      
      if(deflectionResult == CerecResult.DEFLECTION_FAILED or currentPattern.isCompliant(sentence)):
        undeflectables.append(sentence)
    
    if(not undeflectables):
      return CerecResult.DEFLECTION_SUCCESSFUL
    
    else:
      self.opfile.writeToF2("The deflection from noncausal sentences failed for the following sentences:")
      for s in undeflectables:
        self.opfile.writeToF2(" - " + s.getSentenceText())
      return CerecResult.DEFLECTION_FAILED
  
  '''/**
   * Resolves a list of specification proposals by generating a list of new patterns
   * @param currentPattern Given pattern on which the specification shall be performed
   * @param specificationProposals List of specification proposals
   * @return A list of patterns (clones of the given pattern) with the specification proposals applied
   */'''
  def resolveSpecificationProposals(self, currentPattern, specificationProposals):
    resultingPatterns = [] #new ArrayList<IPattern>();
    
    sentenceStructure = currentPattern.getStructure()
    extractionAlgorithm = currentPattern.getGenerationPattern()
    #print('Present st : ', sentenceStructure.toString())
    for sp in specificationProposals:
      # generate sentence structures for each specification proposal
      resultingStructures = sp.resolveSpecificationProposal(sentenceStructure)
      
      # add each resulting pattern to the list
      for resultingStructure in resultingStructures:
        #// clean up the resulting structure by removing all temporal structure elements
        resultingStructure.getRoot().cleanTemporal()
        #// create a pattern with the cleaned structure, assuming that the extraction algrithm is still applicable (this is taken care of later)
        patternIndex = Globals.getInstance().getNewPatternCounter()
        pattern = Pattern(patternIndex, resultingStructure, extractionAlgorithm)
        #self.opfile.writeToF2("One resulting structure:")
        #self.opfile.writeToF2(resultingStructure.toString())
        resultingPatterns.append(pattern)
    
    return resultingPatterns
  
  '''/**
   * Check whether a given set of sentences has been distributed over all given patterns
   * @param currentPatterns List of patterns which should contain the sentences
   * @param sentences List of sentences which were distributed
   * @return True, if each of the patterns contains at least one sentence and all sentences are contained in exactly one pattern
   */'''
  def checkPatternDistribution(self, currentPatterns, sentences):
    # check if all sentences are distributed among the patterns
    undistributed = [] #new ArrayList<ISentence>();
    for sentence in sentences:
      sentenceDistributed = False
      for pattern in currentPatterns:
        if(sentence in pattern.getAccepted()):
          sentenceDistributed = True
          break

      if(not sentenceDistributed):
        undistributed.append(sentence)
      
    
    if(len(undistributed) > 0):
      self.opfile.writeToF2("Differentiation process left some sentences undistributed:")
      for s in undistributed:
        self.opfile.writeToF2(" - " + s.toString())
    
    
    #// check if all patterns are used, meaning that they contain at least one accepted sentence
    unused = [] #new ArrayList<IPattern>();
    for pattern in currentPatterns:
      if(not pattern.getAccepted()):
        unused.append(pattern)
    
    if(len(unused) > 0):
      #CELogger.log().warn("Differentiation process generated some unused patterns:");
      #unused.forEach(p -> CELogger.log().warn(" - Pattern " + p.getIndex()));
      for p in unused:
        currentPatterns.remove(p)
    
    return not undistributed and not unused
  
  
  '''/**
   * Checks if the intruding sentence has been isolated in his own pattern, as he should not be compliant to other sentences
   * @param currentPatterns List of patterns generated by the specification or differentiation
   * @param intruder Sentence, that should not be compliant to patterns containing other sentences
   * @return True, if the given intruding sentence is the only accepted sentence of one pattern
   */'''
  def checkIntruderIsolation(self, currentPatterns, intruder):
    for pattern in currentPatterns:
      if(intruder in pattern.getAccepted()):
        if(len(pattern.getAccepted()) == 1):
          return True
      
        else:
          self.opfile.writeToF2("The pattern covering the intruder after a differentiation is not isolated. Following sentences are contained by the pattern #" + str(pattern.getIndex()) + ":")
          for s in pattern.getAccepted():
            self.opfile.writeToF2(" - " + s.toString())
          return False

    
    print("None of the patterns generated by the differentiation process contained the intruder");
    return False
  
  '''/**
   * Handles the pattern, which isolates the intruder, according to whether the intruding sentence is to be maintained or not:
   *  - intruder maintained: deletes the extraction algorithm (which is not applicable to the intruder, hence the differentiation)
   *  - intruder discarded: deletes the pattern isolating the intruder
   * @param currentPatterns List of patterns generated by the specification or differentiation
   * @param intruder Sentence, that should not be compliant to patterns containing other sentences
   * @param maintainIntruder True, if the intruding sentence is causal itself and deserves an own pattern
   */'''
  def handleIntruderPattern(self, currentPatterns, intruder, maintainIntruder, graph):
    intruderPattern = None
    for pattern in currentPatterns:
      if(intruder in pattern.getAccepted()):
        intruderPattern = pattern
        break

    if(maintainIntruder):
      extractionAlgorithm = self.extractionAlgorithmGenerator.generateCommandPatterns(intruder, graph)
      if(extractionAlgorithm is not None):
        intruderPattern.setGenerationPattern(extractionAlgorithm)
        self.opfile.writeToAll('New complying pattern for this sentence : ' + intruderPattern.toString())
        return True
      else:
        return False
      
    else:
      currentPatterns.remove(intruderPattern)
      return True
  
  def overridePrime(self, primePattern, generatedPatterns):
    substitutePrimePattern = None
    primeSentence = primePattern.getPrime()
    
    for pattern in generatedPatterns:
      if(primeSentence in pattern.getAccepted()):
        #print('Accepted : True' )
        substitutePrimePattern = pattern
        break
    
    primePattern.setStructure(substitutePrimePattern.getStructure())
    primePattern.setAccepted(substitutePrimePattern.getAccepted())
    
    generatedPatterns.remove(substitutePrimePattern)
