class Pattern: # implements IPattern {

  '''private int index;

  /**
   * structure of the sentence: constituency tree of the sentence
   * stripped of the leaf nodes containing only words
   */
  private IStructure sentenceStructure;

  /**
   * genetic algorithm extracting the cause and effect from the
   * sentence of a specific structure
   */
  private Extractor causalityExtraction;

  /**
   * Collection of all sentences complying the sentenceStructure
   */
  private ArrayList<ISentence> accepted;'''

  #public Pattern(int index, IStructure sentenceStructure, Extractor cePattern) {
  def __init__(self, index, sentenceStructure, cePattern):
    self.index = index
    self.sentenceStructure = sentenceStructure
    self.causalityExtraction = cePattern
    self.accepted = []

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getIndex(self):
    return self.index

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getStructure(self):
    return self.sentenceStructure

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def setStructure(self, structure):
    self.sentenceStructure = structure

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getGenerationPattern(self):
    return self.causalityExtraction

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def setGenerationPattern(self, extractor):
    self.causalityExtraction = extractor

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getAccepted(self):
    return self.accepted

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def setAccepted(self, accepted):
    self.accepted = accepted

  '''/**
   * {@inheritDoc}
   */'
  @Override'''
  def getPrecisionScore(self):
    minSize = 9999
    for sentence in self.accepted:
      size = sentence.getRootConstituent().size()
      if(size < minSize):
        minSize = size

    structureSize = self.sentenceStructure.size()

    return structureSize / minSize

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def isCompliant(self, candidate):
    return self.sentenceStructure.compliedBy(candidate)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public boolean isApplicable(ISentence candidate, ICauseEffectGraph ceg) {
  def isApplicable(self, candidate, ceg, url):
    return self.causalityExtraction.isApplicable(candidate, ceg, url)
  
  def addExtractor(self, candidate, ceg, extractionAlgorithmGenerator, effect=False):
    self.causalityExtraction.addExtractor(candidate, ceg, extractionAlgorithmGenerator, effect)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public boolean matches(ISentence candidate, ICauseEffectGraph ceg) {
  def matches(self, candidate, ceg):
    return self.isCompliant(candidate) and self.isApplicable(candidate, ceg) == 3

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def addSentence(self, candidate):
    self.accepted.append(candidate)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ICauseEffectGraph generateCauseEffectGraph(ISentence sentence) {
  def generateCauseEffectGraph(self, sentence):
    return self.causalityExtraction.generateGraphFromSentence(sentence)

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> differentiate(ISentence intruder, ArrayList<IConstraintGenerator> constraintGenerators) {
  def differentiate(self, intruder, constraintGenerators):
    specificationProposals = self.sentenceStructure.differentiate(self.accepted, intruder, constraintGenerators)
    return specificationProposals

  '''/**
   * {@inheritDoc}
   */
  /*@Override
  public boolean deflectIntruder(ISentence intruder) {'''
  def deflectIntruder(self, intruder):
    deflectionSuccessful = self.sentenceStructure.deflectIntruder(self.accepted, intruder)

    if(deflectionSuccessful):
      return True

    else:
      print("Unable to deflect intruding sentence in pattern #" + str(self.index) + ":")
      print("  Intruder: " + intruder.toString())
      print("  Pattern Structure: " + self.sentenceStructure.toString())
      return False


  '''/**
   * {@inheritDoc}
   */
  /*@Override'''
  def differentiateSimilar(self, intruder):
    differentiatingStructureCompliantToIntruder = self.sentenceStructure.differentiateSimilar(self.accepted, intruder)

    if(differentiatingStructureCompliantToIntruder is not None):
      return differentiatingStructureCompliantToIntruder

    else:
      print("Unable to split pattern #" + int(self.index) + ":");
      print("  Intruder: " + intruder.toString());
      print("  Pattern Structure: " + self.sentenceStructure.toString())
      return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> specifyVersus(ISentence intruder, boolean maintainIntruder) {
  def specifyVersus(self, intruder, maintainIntruder):
    # attempt a soft specification, where the compliance of all accepted patterns is maintained
    # print(type(self.sentenceStructure).__name__)
    specificationProposals = self.sentenceStructure.specifySoftVersus(self.accepted, intruder)
    if(specificationProposals is not None and len(specificationProposals) > 0):
      return specificationProposals

    # attempt a hard specification, where only the compliance of the prime accepted sentence is maintained
    specificationProposals = self.sentenceStructure.specifyHardVersus(self.getPrime(), self.getAcceptedSentencesWithoutPrime(), intruder)
    if(specificationProposals is not None and len(specificationProposals) > 0):
      return specificationProposals

    return None

  #@Override
  def reevaluateConstraints(self):
    self.sentenceStructure.reevaluateConstraints(self.accepted)

  '''/**
   * {@inheritDoc}
   */
  /*@Override
  public ArrayList<IPattern> specifyVersus(ISentence intruder, boolean maintainIntruder) {
    // attempt a soft specification, where the compliance of all accepted patterns is maintained
    ArrayList<SpecificationProposal> specificationProposalsSoft = sentenceStructure.specifySoftVersus(accepted, intruder);
    if(specificationProposalsSoft   is not None) {
      CELogger.log().info("Soft specification succeeded!");

      ArrayList<ISentence> sentencesForDistribution = accepted;
      if(maintainIntruder)
        sentencesForDistribution.add(intruder);
      ArrayList<IPattern> resultingPatterns = resolveSpecificationProposals(specificationProposalsSoft, sentencesForDistribution);
      checkResultingPatterns(resultingPatterns, intruder, maintainIntruder);

      return resultingPatterns;
    } else {
      CELogger.log().info("Soft specification did not succeed!");
    }

    // attempt a hard specification, where only the compliance of the prime accepted sentence is maintained
    ArrayList<SpecificationProposal> specificationProposalsHard = sentenceStructure.specifyHardVersus(getPrime(), getAcceptedSentencesWithoutPrime(), intruder);
    if(specificationProposalsHard   is not None) {
      CELogger.log().info("Hard specification succeeded!");

      ArrayList<ISentence> sentencesForDistribution = accepted;
      if(maintainIntruder)
        sentencesForDistribution.add(intruder);
      ArrayList<IPattern> resultingPatterns = resolveSpecificationProposals(specificationProposalsHard, sentencesForDistribution);
      checkResultingPatterns(resultingPatterns, intruder, maintainIntruder);

      return resultingPatterns;
    } else {
      CELogger.log().info("Hard specification did not succeed!");
    }

    return None;
  }*/'''

  '''/**
   * Resolves a set of specification proposals by specifying the structure of this pattern and redistributing all relevant sentences among the new patterns
   * @param specificationProposals List of specification proposals
   * @param sentencesForDistribution List of all sentences that need to be redistributed onto the resulting patterins
   * @return A list of patterns, one for each specification proposal, with its compliant sentences and, if still applicable, the extraction algorithm
   */
  /*@SuppressWarnings("unchecked")'''
  '''private ArrayList<IPattern> resolveSpecificationProposals(ArrayList<SpecificationProposal> specificationProposals, ArrayList<ISentence> sentencesForDistribution) {
  def resolveSpecificationProposals(specificationProposals,  sentencesForDistribution):
    ArrayList<IPattern> resultingPatterns = new ArrayList<IPattern>();
    ArrayList<ISentence> remainingSentencesForDistribution = (ArrayList<ISentence>) sentencesForDistribution.clone();
    resultingPatterns = []
    remainingSentencesForDistribution = sentencesForDistribution.copy()
    for sp in specificationProposals:
      # generate one sentence structure for each specification proposal
      specifiedStructure = sentenceStructure.copy();
      sp.resolveSpecificationProposal(specifiedStructure.getRoot())

    return resultingPatterns
    sentenceStructureOfPrimePattern = None
    acceptedSentencesOfPrimePattern = None

    resultingPatterns = []
    remainingSentencesForDistribution = sentencesForDistribution.copy()

    for sp in specificationProposals:
      # generate one sentence structure for each specification proposal
      specifiedStructure = sentenceStructure.copy()
      if(not sp.getSpecificationTag().contentEquals(SpecificationProposal.NO_TAG_APPLICABLE)) :
        # first resolve all specification proposals with dedicated tags - otherwise all sentences would be compliant to the variant with no tag applicable
        sp.resolveSpecificationProposal(specifiedStructure.getRoot())

        # identify which of the currently accepted sentences are compliant to the new structure
        acceptedIndices = []
        for i in range(remainingSentencesForDistribution.size()):
          candidate = remainingSentencesForDistribution[i]
          if(specifiedStructure.compliedBy(candidate)):
            acceptedIndices.append(i)

          acceptedSentencesBySpecification = []

        for index in acceptedIndices:
          candidate = remainingSentencesForDistribution[int(index)]
          acceptedSentencesBySpecification.append(candidate)

        #for(int j = ; j >= 0; j--) {
        for j in range(acceptedIndices.size()-1, -1, -1):
          indexForRemoval = acceptedIndices[j]
          remainingSentencesForDistribution.pop(indexForRemoval)


        # if the prime sentence is part of the accepted sentences, rather transform this pattern than creating a new one
        if(acceptedSentencesBySpecification.contains(getPrime())):
          sentenceStructureOfPrimePattern = specifiedStructure
          acceptedSentencesOfPrimePattern = acceptedSentencesBySpecification

        else:
          patternForSpecification = createSpecification(specifiedStructure, acceptedSentencesBySpecification)
          resultingPatterns.append(patternForSpecification)

    # check if there is a specification proposal with no tag
    for sp in specificationProposals:
      if sp.getSpecificationTag().contentEquals(SpecificationProposal.NO_TAG_APPLICABLE):
        specifiedStructure = sentenceStructure.copy()
        patternForSpecification = createSpecification(specifiedStructure, remainingSentencesForDistribution)
        remainingSentencesForDistribution = []
        resultingPatterns.append(patternForSpecification)

    if(sentenceStructureOfPrimePattern == None or acceptedSentencesOfPrimePattern == None):
      print("While resolving specification proposals, the prime pattern did not contain a sentence structure of accepted sentences")
    else:
      self.sentenceStructure = sentenceStructureOfPrimePattern
      self.accepted = acceptedSentencesOfPrimePattern

    if(not remainingSentencesForDistribution.isEmpty()):
      print("While resolving specification proposals, some accepted sentences from the original pattern were not compliant to any pattern anymore:")
      for orphan in remainingSentencesForDistribution:
        print(" - " + orphan.toString())

    return resultingPatterns
  }*/

  /*private Pattern createSpecification(IStructure specifiedStructure, ArrayList<ISentence> acceptedSentences) {
    boolean allAcceptedAreAcceptedOfThisPattern = true;;
    for(ISentence sentence : acceptedSentences) {
      if(!accepted.contains(sentence)) {
        allAcceptedAreAcceptedOfThisPattern = false;
      }
    }

    ICauseEffectPattern cep = None;
    if(allAcceptedAreAcceptedOfThisPattern) {
      cep = this.cePattern;
    }

    Pattern patternForSpecification = new Pattern(Globals.getInstance().getNewPatternCounter(), specifiedStructure, cep);
    for(ISentence candidate : acceptedSentences) {
      patternForSpecification.addSentence(candidate);
    }

    return patternForSpecification;
  }*/

  /**
   * Performs checks on the resulting patterns of a specification process, which contains:
   *  - checks if the intruding sentence is isolated in a generated pattern
   *  - removes the pattern compliant to the intruding sentence (in the scenario of a deflection)
   * @param patterns List of patterns generated in a specification process
   * @param intruder Intruding sentence initiating the specification process
   * @param maintainIntruder False, if the specification happened in the process of a deflection, such that the intruder should not get a pattern
   */
  /*private void checkResultingPatterns(ArrayList<IPattern> patterns, ISentence intruder, boolean maintainIntruder) {
    int indexOfPatternForIntruder = -1;
    /*for(IPattern pattern : patterns) {
      // check if the intruding sentence is isolated in his new pattern
      if(pattern.getAccepted().contains(intruder)) {
        indexOfPatternForIntruder = pattern.getIndex();
        if(pattern.getAccepted().size() > 1) {
          // the intruding sentence is not isolated even though it should be, since the extraction algorithms cannot be applicable to all sentences of this pattern
          CELogger.log().warn("The resulting pattern #" + indexOfPatternForIntruder + " contains the intruder, but the intruder is not isolated.");
          for(ISentence sentence : pattern.getAccepted()) {
            CELogger.log().warn(" - " + sentence.toString());
          }
        }
      }
    }*/
    /*for(IPattern pattern : patterns) {
      // check if the intruding sentence is isolated in his new pattern
      if(pattern.getAccepted().isEmpty()) {
        indexOfPatternForIntruder = pattern.getIndex();
      }
    }

    // if the resulting patterns were generated during deflection, remove the pattern of the intruder
    if(!maintainIntruder) {
      final int indexForRemoval = indexOfPatternForIntruder;
      if(indexOfPatternForIntruder > -1) {
        patterns.removeIf(p -> (p.getIndex() == indexForRemoval));
      } else {
        CELogger.log().error("Trying to remove the generated pattern containing the intruding sentence, but there was no pattern identified.");
      }
    }
  }*/'''

  #@Override
  def getPrime(self):
    return self.accepted[0]

  def getAcceptedSentencesWithoutPrime(self):
    other = []

    #for(int i = 1; i < accepted.size(); i++) {
    for i in range(1, len(self.accepted)):
      other.append(self.accepted[i])

    return other


  #@Override
  def clone(self):
    clone = Pattern(self.index, self.sentenceStructure.clone(), self.causalityExtraction)
    clone.setAccepted(self.accepted)
    return clone

  #@Override
  def toString(self):
    sb = []

    sb.append("Pattern #" + str(self.index) + ":\n")
    sb.append(" Structure: " + self.sentenceStructure.toString() + "\n")
    sb.append(self.causalityExtraction.getCommandStrings() + "\n")
    sb.append(" Accepted sentences:\n")
    for sentence in self.accepted:
      sb.append("  " + sentence.getRootConstituent().getCoveredText() + "\n")

    return ' '.join(sb)
