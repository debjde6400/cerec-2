'''
/**
 *
 * @author Julian Frattini
 *
 * Main component distributing input, managing the knowledge database of causality patterns
 * and preparing results of computation.
 */'''
 
from python.sentence.StanfordCoreNLP_ann import CoreNLPAnnotator
from python.main.CerecResult import CerecResult
from python.pattern.Pattern import Pattern
from python.main.PatternDatabase import PatternDatabase
from python.main.Differentiator import Differentiator
from python.util.Globals import Globals
#import spacy as sc

class CauseEffectRecognition: #implements ICauseEffectRecognition{

  '''/**
   * Reference to the a NLP sentence parser, that translates the given natural language
   * sentence into a formalized sentence complying the ISentence interface
   */
  private DKProParser annotator;

  /**
   * List of existing patterns
   */
  private PatternDatabase patterns;
  private PatternDatabase patterns_backup;

  /**
   * List of non-causal sentences
   */
  private ArrayList<ISentence> noncausals;
  private ArrayList<ISentence> noncausals_backup;

  /**
   * Generator in charge of creating an extraction algorithm based on a sentence and
   * a given phrase to extract
   */
  private ICommandGenerator commandGenerator;

  /**
   * Generator in charge of identifying the grammatical structure of a sentence, which
   * in turn will be used to determine grammatical equivalence between two sentences
   */
  private IStructureGenerator structureGenerator;

  /**
   * Differentiator in charge of differentiating existing patterns from erroneously
   * compliant intruding sentences
   */
  private Differentiator differentiator;

  /**
   * Creates a new cause-effect-recognition pipeline. All elements, that can be interchanged
   * via parameters need to be set here
   * @param commandGenerator The generator of extraction-algorithms
   * @param structureGenerator The extractor of sentence structures
   */'''
  #public CauseEffectRecognition(ICommandGenerator commandGenerator, IStructureGenerator structureGenerator) {
  def __init__(self, commandGenerator, structureGenerator, url):
    from python.pattern.LexicalConstraintGenerator import LexicalConstraintGenerator
    self.patterns =  PatternDatabase()
    self.patterns_backup = PatternDatabase()
    self.opfile = None
    self.noncausals = [] #new ArrayList<ISentence>();
    self.url = url
    
    self.annotator = CoreNLPAnnotator(url)
    self.commandGenerator = commandGenerator
    self.structureGenerator = structureGenerator

    # setup the differentiator
    self.differentiator = Differentiator(self.patterns, self.commandGenerator)
    self.differentiator.addConstraintGenerator(LexicalConstraintGenerator())
    #self.nlp = sc.load('en_core_web_md')

  #@Override
  def getPatterns(self):
    return self.patterns.getPatterns()

  #@Override
  def snapshot(self):
    # snapshot all patterns
    self.patterns_backup = PatternDatabase()
    for pattern in self.patterns.getPatterns():
      self.patterns_backup.addPattern(pattern.clone())

    # snapshot all noncausals
    self.noncausals_backup = [] #new ArrayList<ISentence>();
    for noncausal in self.noncausals:
      self.noncausals_backup.append(noncausal)

  #@Override
  def restore(self):
    self.patterns.reset()
    for pattern in self.patterns_backup.getPatterns():
      self.patterns.addPattern(pattern.clone())

    self.noncausals = [] #new ArrayList<ISentence>()
    for noncausal in self.noncausals_backup:
      self.noncausals.append(noncausal)

  #@Override
  def reset(self):
    self.noncausals = [] #new ArrayList<ISentence>()
    Globals.getInstance().reset()
    self.patterns.reset()

  #@Override
  def formalizeSentence(self, sentence):
    #sen = annotator.createSentence(sentence, Language.en);
    sen = self.annotator.create_sentence(sentence)
    return sen
  
  def setOPFile(self, opfile):
    self.opfile = opfile
    self.commandGenerator.setOPFParser(self.opfile, self.annotator)
    self.differentiator.setOPFile(self.opfile)
    self.patterns.setOPFile(self.opfile)
    
  '''/**
   * Attempt to generate a cause-effect-graph from a given sentence. This will work when
   * the system already knows a causality pattern associated with the sentence's
   * grammatical structure
   * @param input The sentence under test
   * @return A cause-effect-graph, if the sentence is identified by a causality pattern
   */
  @Override'''
  def getCEG(self, input):
    print("---------------------------------");
    # preprocess the sentence with NLP techniques
    sentence = self.formalizeSentence(input)

    # try to find a causality pattern in the database of patterns
    patternFound = self.patterns.getMostPrecisePattern(self.patterns.getPatterns(), sentence)

    if(patternFound is not None):
      # pattern found: attempt to generate a cause-effect-graph from the sentence with the given causality pattern
      print("Sentence '" + input + "' is compliant to the structure of pattern #" + patternFound.getIndex())
      ceg = patternFound.generateCauseEffectGraph(sentence)

      if(ceg is not None):
        print("The pattern is able to extract a cause-effect-graph from the sentence")
        return ceg
      else:
        # unable to generate a cause-effect, possibly because the sentence was compliant to the pattern due to lack of training
        print("The pattern's generation algorithm does not create a cause-effect-graph!")
        return None
      
    else:
      # no pattern found: the sentence is assumed to be non-causal
      print("Sentence '" + input + "' is not accepted by any pattern")
      return None
    
  #@Override
  def getCompliantPattern(self, input):
    sentence = self.formalizeSentence(input)
    patternFound = self.patterns.getMostPrecisePattern(self.patterns.getPatterns(), sentence)
    return patternFound

  '''/**
   * Provide the system with a causality example containing a sentence and its causality portion.
   * The system will then attempt to generate a new causality pattern, which in turn will be able to
   * recognize grammatically similar sentences and extract the cause- and effect-expressions from it
   * @param input CausalityExample containing a sentence and its causality portion
   * @return CerecResult evaluating the training process
   */
  @Override'''
  def train(self, input):
    result = None

    self.opfile.writeToAll("Sentence : " + input.getSentence())
    if(input.isCausal()):
      self.opfile.writeToAll("Cause : " + input.getCause())
      self.opfile.writeToAll("Effect : " + input.getEffect())

    #// check if the CausalityExample is actually valid: the cause- and effect-expression must be a valid substring of the sentence
    if(not self.isExampleValid(input)):
      result = CerecResult.CREATION_IMPOSSIBLE
      print("The sentence cannot be analyzed, because cause and/or effect are not substrings of the sentence.")
      return result
    
    try:
      sentence = self.annotator.create_sentence(input.getSentence())
    except:
      result = CerecResult.CREATION_IMPOSSIBLE
      print("Sentence could not be parsed by the parser.")
      return result
    
    ceg = input.getCEG()
    #self.opfile.writeToF1("\n " + sentence.getRootConstituent().structureToString(True)+"\n")
    #self.opfile.writeToF1(sentence.getRootConstituent().structureToString(False)+"\n")
    self.opfile.writeToF2("\n" + sentence.getRootConstituent().toString(True, False)+"\n")
    self.opfile.writeToF2(sentence.getRootConstituent().toString(False, True)+"\n")

    # verify if there already exists a pattern complying to the sentence's structure in the database
    self.opfile.writeToAll("Searching for a pattern complying to the sentence's structure...")
    patternFound = self.patterns.getMostPrecisePattern(self.patterns.getPatterns(), sentence)

    if(patternFound is None):
      self.opfile.writeToAll("No pattern found.")
      
      #// no existing pattern found, creating a new one
      if(input.isCausal()):

        self.opfile.writeToAll("Generating a new one!") #info

        applicableCausalityExtractor = self.commandGenerator.generateCommandPatterns(sentence, ceg)

        if(applicableCausalityExtractor is not None):
          '''// check if the new pattern does generate the desired cause-effect-graph of the CausalityExample
          //if(checkPatternCompliance(sen, newPattern, ceg)) {
          // CELogger.log().print("\n Extractor: "+applicableCausalityExtractor.toString());'''
          #print('Causality extractor obtained. Floof.')
          if(applicableCausalityExtractor.isApplicable(sentence, ceg, self.url) == 3):
            self.opfile.writeToAll("The new pattern creates the desired expressions accordingly.")
            self.opfile.writeToF2("-- Sentence Structure -- \n" + sentence.getRootConstituent().toString(True, True))
            self.opfile.writeToF2( applicableCausalityExtractor.getCommandStrings() + "\n")

            structure = self.structureGenerator.generateStructure(sentence)
            compliantPattern = Pattern(Globals.getInstance().getNewPatternCounter(), structure, applicableCausalityExtractor)      
            compliantPattern.addSentence(sentence)
            
            result = self.differentiator.deflectFromNoncausal(compliantPattern, self.noncausals)
            self.opfile.writeToAll("-- Generated pattern -- \n" + compliantPattern.toString())
            
            if(result == CerecResult.DEFLECTION_SUCCESSFUL):
              self.patterns.addPattern(compliantPattern)
              result = CerecResult.CREATION_SUCCESSFUL
            
          else:
            self.opfile.writeToF1("The new cause effect pattern does not generate the correct CEG") #warn
            result = CerecResult.CREATION_FAILED
          
        else:
          # creation failed due to an unknown reason
          self.opfile.writeToF1("The cause-effect-generator did not generate a new pattern!") #warn
          result = CerecResult.CREATION_FAILED
        
      else:
        # non-causal sentence correctly discarded
        self.opfile.writeToF1("The sentence was discarded correctly.")  #//info
        self.noncausals.append(sentence)
        result = CerecResult.DISCARDING_SUCCESSFUL
      
    else:
      #// existing pattern found
      self.opfile.writeToAll("Found a complying pattern:")  #//info
      self.opfile.writeToAll(patternFound.toString())    #//info

      if(input.isCausal()):
        #// check compliance
        
        # new!
        res = patternFound.isApplicable(sentence, ceg, self.url)
        if(res == 3):  # completely successful
          self.opfile.writeToAll("The complying pattern generates the correct expressions!")
          patternFound.addSentence(sentence)
          result = CerecResult.RECOGNITION_SUCCESSFUL
          
        else:
          
          #// the sentence erroneously complies with the pattern
          self.opfile.writeToAll("The found pattern does not generate the right cause-effect-graph!")  #//warn
          
          if res == 2:
            # new algo required for cause part
            self.opfile.writeToAll("This pattern could not generate the cause part, so new alcommands required for it.")
            patternFound.addExtractor(sentence, ceg, self.commandGenerator)
            self.opfile.writeToAll("Pattern after adding new commands: ")
            self.opfile.writeToAll(patternFound.toString())
            result = CerecResult.SPECIFICATION_SUCCESSFUL
            
          elif res == 1:
            # new algo required for effect part
            self.opfile.writeToAll("This pattern could not generate the effect part, so new alcommands required for it.")
            patternFound.addExtractor(sentence, ceg, self.commandGenerator, effect = True)
            self.opfile.writeToAll("Pattern after adding new commands: ")
            self.opfile.writeToAll(patternFound.toString())
            result = CerecResult.SPECIFICATION_SUCCESSFUL
            
          else:
            # differentiate only when neither phrase have been extracted
            result = self.differentiator.differentiate(patternFound, sentence, ceg, True)
        
      else:
        #// a pattern was found for a non-causal sentence, which requires deflection
        self.opfile.writeToAll("The non-causal sentence was erroneously compliant to a pattern, which requires the pattern to be more specific")  #//warn
        self.noncausals.append(sentence)

        noncausal = [] #new ArrayList<ISentence>();
        noncausal.append(sentence)
        result = self.differentiator.deflectFromNoncausal(patternFound, noncausal)
      
    self.opfile.writeToAll("---------------------------------\n")   #//info

    return result

  '''/**
   * Checks, whether the cause- and effect-expression of a causal example are valid substrings of the sentence
   * @param example Causal or non-causal sentence
   * @return True, if the example is possibly analyzable
   */'''
  def isExampleValid(self, example):
    if(example.isCausal()):
      sentence = example.getSentence()
      cause = example.getCause()
      effect = example.getEffect()
      #if(sentence.contains(cause) and sentence.contains(effect)
      if(cause in sentence and effect in sentence and self.isPhraseContainedCompletely(sentence, cause) and self.isPhraseContainedCompletely(sentence, effect)):
        #// an example is only valid, if the cause- and effect-expression is a substring of the sentence
        return True
      else:
        #// there is no possibility to extract the expressions
        return False
      
    else:
      #// non-causal sentences just have to be discarded
      return True

  def isPhraseContainedCompletely(self, sentence, phrase):
    beginOfPhrase = sentence.index(phrase)
    if(beginOfPhrase > 0):
      #prefix = sentence.substring(0, beginOfPhrase)
      prefix = sentence[:beginOfPhrase]
      #if(Character.isLetter(prefix.charAt(beginOfPhrase-1)))
      if prefix[beginOfPhrase-1].isalpha():
        return False

    endOfPhrase = sentence.index(phrase) + len(phrase)
    if(endOfPhrase < len(sentence)):
      #suffix = sentence.substring(endOfPhrase)
      suffix = sentence[endOfPhrase:]
      #if(Character.isLetter(suffix.charAt(0))) {
      if suffix[0].isalpha():
        return False

    return True
