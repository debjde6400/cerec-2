#from python.sentence.Node import Node
#from python.sentence.Leaf import Leaf
from python.sentence.Sentence import Sentence

'''package jfr.cerec.pattern;

import java.util.ArrayList;

import jfr.cerec.sentence.Fragment;
import jfr.cerec.sentence.ISentence;
import jfr.cerec.sentence.Sentence;'''

class DependencyStructure: #implements IStructure {

  #private DependencyStructureElement root;

  def __init__(self, root):
    #super()
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
  def equals(self, other):
    if(not isinstance(other, DependencyStructure)):
      return False
    return self.root.equals(other.getRoot())

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def compliedBy(self, candidate):
    if isinstance(candidate, Sentence):
      sentence = candidate
      return self.root.isCompliedBy(sentence.getRootConstituent().getRootGovernor())

    return False


  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> differentiate(ArrayList<ISentence> accepted, ISentence intruder, ArrayList<IConstraintGenerator> constraintGenerators) {
  def differentiate(self, accepted, intruder, constraintGenerators):
    acceptedFragments = self.getRootGovernors(accepted)
    intrudingFragment = intruder.getRootDependency()
    specificationProposals = self.root.detectEligibleDifferentiator(acceptedFragments, intrudingFragment, constraintGenerators)
    #specificationProposals.sort((sp1, sp2) -> ((int) (sp2.getPrecision()-sp1.getPrecision())))
    specificationProposals.sort(key= lambda sp1, sp2: sp2.getPrecision() - sp1.getPrecision())

    return specificationProposals


  '''/**
   * {@inheritDoc}
   */
  /*@Override
  public boolean deflectIntruder(ArrayList<ISentence> accepted, ISentence intruder) {
    // attempt to find a structure node where a white- or blacklist entry would differentiate the accepted sentences from the intruder
    EligibleDifferentiator differentiator = getDifferentiator(accepted, intruder);

    if(differentiator is not None) {
      // determine whether the differentiating word is a white- or blacklist candidate for the original structure
      if(differentiator.getWhitelistCandidate() is not None) {
        differentiator.getCorrespondingElement().addKeyword(differentiator.getWhitelistCandidate(), true);
      } else {
        differentiator.getCorrespondingElement().addKeyword(differentiator.getBlacklistCandidate(), false);
      }
      return true;
    } else {
      // no eligible differentiator was found and the deflection failed
      return false;
    }
  }*/

  /**
   * {@inheritDoc}
   */
  /*@Override
  public IStructure differentiateSimilar(ArrayList<ISentence> accepted, ISentence intruder) {
    // attempt to find a structure node where a white- or blacklist entry would differentiate the accepted sentences from the intruder
    EligibleDifferentiator differentiator = getDifferentiator(accepted, intruder);

    if(differentiator is not None) {
      // determine whether the differentiating word is a white- or blacklist candidate for the original structure
      boolean whitelistcandidate = (differentiator.getWhitelistCandidate() is not None);
      String differentiatingWord = differentiator.getListCandidate(whitelistcandidate);
      differentiator.getCorrespondingElement().addProposedKeywords(differentiatingWord);

      // generate a clone of this structure which will in future take care of the intruding structure
      IStructure differentiatingStructureCompliantToIntruder = this.clone();

      // add the proposed keyword to the respective white- and blacklist
      root.listAllProposed(whitelistcandidate);
      differentiatingStructureCompliantToIntruder.getRoot().listAllProposed(!whitelistcandidate);

      return differentiatingStructureCompliantToIntruder;
    } else {
      // no eligible differentiator was found and the differentiation failed
      return None;
    }
  }*/

  /**
   * Identify a differentiating element in the structure, that differs the accepted sentences from the intruding
   * by determining a keyword, that appears in one group but not the other
   * @param accepted List of already accepted sentences
   * @param intruder Sentence, that is erroneously compliant to the structure
   * @return The most suitable differentiating element of the structure
   */
  /*private EligibleDifferentiator getDifferentiator(ArrayList<ISentence> accepted, ISentence intruder) {
    // prepare detection algorithm
    ArrayList<Fragment> acceptedRoots = new ArrayList<Fragment>();
    for(ISentence sentence : accepted) {
      acceptedRoots.add(sentence.getRootConstituent().getRootGovernor());
    }
    Fragment intruderRoot = intruder.getRootConstituent().getRootGovernor();
    // detect an eligible differentiating node
    ArrayList<EligibleDifferentiator> eligibleDifferentiators = new ArrayList<EligibleDifferentiator>();
    root.detectEligibleDifferentiator(eligibleDifferentiators, acceptedRoots, intruderRoot);

    // determine, which tag set is used to order the eligibility of differentiating elements
    String[] differentiatingTags = None;
    if(GlobalConfiguration.useDependencyTagsForEligibilityCheck) {
      differentiatingTags = Configuration.differentiatingDependencyTags;
    } else {
      differentiatingTags = Configuration.differentiatingConstituencyTags;
    }

    // try to identify an eligible differentiator, that uses a recommended differentiating word
    for(String tag : differentiatingTags) {
      List<EligibleDifferentiator> differentiatorsOfTag = eligibleDifferentiators.stream().filter(d -> d.getTag().contentEquals(tag)).collect(Collectors.toList());

      for(String word : Configuration.recommendedDifferentiatingWords) {
        for(EligibleDifferentiator eligible : differentiatorsOfTag) {
          if(eligible.getWhitelistCandidate().contains(word))
            return eligible;
        }
      }
    }

    // use any differentiator of the preferred tags
    for(String tag : differentiatingTags) {
      for(EligibleDifferentiator eligible : eligibleDifferentiators) {
        if(eligible.getTag().contentEquals(tag)) {
          if(eligible.getWhitelistCandidate() is not None || eligible.getBlacklistCandidate() is not None)
            return eligible;
        }
      }
    }

    // use any differentiator available
    for(EligibleDifferentiator eligible : eligibleDifferentiators) {
      if(eligible.getWhitelistCandidate() is not None || eligible.getBlacklistCandidate() is not None)
        return eligible;
    }

    return None;
  }*/'''

  def getRootGovernors(self, accepted):
    acceptedRoots = []
    for sentence in accepted:
      acceptedRoots.append(sentence.getRootDependency())

    return acceptedRoots

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> specifySoftVersus(ArrayList<ISentence> accepted, ISentence intruder) {
  def specifySoftVersus(self, accepted, intruder):
    specificationProposals = []
    success = self.root.specifySoftVersus(self.getRootGovernors(accepted), intruder.getRootDependency(), specificationProposals)

    if(success):
      return specificationProposals

    return None

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  #public ArrayList<SpecificationProposal> specifyHardVersus(ISentence prime, ArrayList<ISentence> otherAccepted, ISentence intruder) {
  def specifyHardVersus(self, prime, otherAccepted, intruder):
    success = False
    primeFragment = prime.getRootDependency()
    otherAcceptedFragments = self.getRootGovernors(otherAccepted)
    intruderFragment = intruder.getRootDependency()
    specificationProposals = []

    # perform the specification
    success = self.root.specifyHardVersus(primeFragment, otherAcceptedFragments, intruderFragment, specificationProposals)

    if(success):
      return specificationProposals

    return None

  #@Override
  def reevaluateConstraints(self, accepted):
    self.root.reevaluateConstraintPosition(self.getRootGovernors(accepted))

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def toString(self):
    return self.root.toString();

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def clone(self):
    #return DependencyStructure((DependencyStructureElement) root.clone());
    return self.root.clone()

  '''/**
   * {@inheritDoc}
   */
  @Override'''
  def size(self):
    return self.root.size()

  def getWidth(self):
    return self.root.size()
