from python.sentence.Sentence import Sentence

class ConstituentStructure: #implements IStructure {
  #private ConstituentStructureElement root;

  def __init__(self, root):
    self.root = root

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def getRoot(self):
    return self.root

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public boolean equals(IStructure other) {
  def __eq__(self, other):
    if(not isinstance(other, ConstituentStructure)):
      return False
    return self.root == other.getRoot()

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def compliedBy(self, candidate):
    if(isinstance(candidate, Sentence)):
      sentence = candidate
      return self.root.isCompliedBy(sentence.getRootConstituent())

    return False


  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> differentiate(ArrayList<ISentence> accepted, ISentence intruder, ArrayList<IConstraintGenerator> constraintGenerators) {
  def differentiate(self, accepted, intruder, constraintGenerators):
    acceptedFragments = self.getRootConstituents(accepted)
    intrudingFragment = intruder.getRootConstituent()
    specificationProposals = self.root.detectEligibleDifferentiator(acceptedFragments, intrudingFragment, constraintGenerators)
    #specificationProposals.sort((sp1, sp2) -> ((int) (sp2.getPrecision()-sp1.getPrecision()))) #?
    specificationProposals.sort(key= lambda sp: sp.getPrecision(), reverse=True)

    return specificationProposals

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def toString(self):
    return self.root.toString()

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def clone(self):
    #return new ConstituentStructure((ConstituentStructureElement) root.clone());
    return ConstituentStructure(self.root.clone())

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def size(self):
    return self.root.size()

  def getRootConstituents(self, accepted):
    acceptedRoots = []
    for sentence in accepted:
      acceptedRoots.append(sentence.getRootConstituent())

    return acceptedRoots


  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> specifySoftVersus(ArrayList<ISentence> accepted, ISentence intruder) {
  def specifySoftVersus(self, accepted, intruder):
    specificationProposals = [] #new ArrayList<SpecificationProposal>();
    success = self.root.specifySoftVersus(self.getRootConstituents(accepted), intruder.getRootConstituent(), specificationProposals)

    if(success):
      #print([s.toString() for s in specificationProposals])
      return specificationProposals

    return None


  '''/**
   * {@inheritDoc}
   */
  @Override
  public ArrayList<SpecificationProposal> specifyHardVersus(ISentence prime, ArrayList<ISentence> otherAccepted,
      ISentence intruder) {'''
  def specifyHardVersus(self, prime, otherAccepted, intruder):
    success = False
    primeFragment = prime.getRootConstituent()
    otherAcceptedFragments = self.getRootConstituents(otherAccepted)
    intruderFragment = intruder.getRootConstituent()
    specificationProposals = []    #new ArrayList<SpecificationProposal>()

    # perform the specification
    success = self.root.specifyHardVersus(primeFragment, otherAcceptedFragments, intruderFragment, specificationProposals)

    if(success):
      return specificationProposals

    return None


  #@Override
  def reevaluateConstraints(self, accepted):
    self.root.reevaluateConstraintPosition(self.getRootConstituents(accepted))

  #@Override
  def getWidth(self):
    return self.getMaxWidth(False);

  '''/**
   * Calculates, on which level the tree structure has the most nodes
   * @param getLevel Determines the return value
   * @return if getLevel == true, the level of the maximum width, else the number of nodes on that level
   */'''
  def getMaxWidth(self, getLevel):
    max = 0
    level = 0
    for i in range(self.root.getDepth()):
      current = self.root.getWidthAtLevel(i)
      if(current > max):
        max = current
        level = i

    return level if getLevel else max #(getLevel ? level : max)

  def getElementsAtLevel(self, level):
    return self.root.getElementsAtLevel(level)
