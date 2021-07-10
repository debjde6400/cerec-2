import os, sys
#os.chdir('..' + os.path.sep + '..')
sys.path.append(os.getcwd())

import re
import python.data.DataPaths as DataPaths
from tqdm import tqdm
#import spacy as sc
from nltk.tree import ParentedTree
from python.sentence.StanfordCoreNLP_ann import CoreNLPAnnotator
from python.sentence.Node import Node
from python.sentence.Leaf import Leaf
from python.sentence.Sentence import Sentence
import python.data.DataPaths as DataPaths
from python.io.JSONCausalityDataReader import JSONCausalityDataReader
from python.util.Utils import Utils
from nltk.parse import CoreNLPParser
from python.data.DataSet import DataSet
from python.genetics.ConstituentCommandGenerator import ConstituentCommandGenerator
from python.pattern.ConstituentStructureGenerator import ConstituentStructureGenerator
from python.pattern.Pattern import Pattern
from python.main.Differentiator import Differentiator
from python.main.PatternDatabase import PatternDatabase
from python.pattern.LexicalConstraintGenerator import LexicalConstraintGenerator
from python.pattern.ConstituentStructure import ConstituentStructure
from python.pattern.ConstituentStructureElement import ConstituentStructureElement

def get_tree(se):
  #if '<' in se and '>' in se:
  #  se = Utils.resolvePunctuations(se, True)
  
  parser = CoreNLPParser(url='http://localhost:9000/')
  parse = parser.raw_parse(se)
  tokenized_sent = list(parser.tokenize(se))
  print(tokenized_sent)
  
  return parse

  #return anno
  
def readSetFromJSON(file):
  if type(file).__name__ != 'list':
    file = [file]
    
  set = DataSet()
  for f in file:
    reader = JSONCausalityDataReader()
    reader.initialize(f)
    set.addSet(reader.readExamples())

  return set

set1 = readSetFromJSON(DataPaths.PURE_PEPPOL)
#print([str(s) for s in set1.set][44])

def clone(ob):
  ## PROBLEM!!
  cl = ConstituentStructureElement(ob.tag, ob.index)

  for constraint in ob.constraints:
    cl.addConstraint(constraint.clone())

  for child in ob.children:
    print('Cl1: ', cl.toString())
    print('chl : ', str([p.toString() for p in cl.children]))
    cl.children.append(child.clone())
    cl.children[-1].setParent(cl)
    print('Cl2: ', cl.toString())
  
  print('Cl3: ', cl.toString())
  return cl

st = [s for s in set1.set]
sentu = st[317]
#print(sentu.sentence)
#print(Utils.resolvePunctuations(Utils.resolvePunctuations(st[18].sentence, True), False))
#print(re.sub("\s\<([^\>]+\s[^\>]*)\>\s?", r" < \1 > ", sentu.sentence).strip())
s2 = 'E.g. If there is a local Information Phone-number but no local email of the airl5.'
an = CoreNLPAnnotator(url='http://localhost:9000/')
sent = an.create_sentence(sentu.sentence, debug=True)
print(sent.getRootConstituent().toString(True, True))
#s = sent.getRootConstituent().children[0].children[1].getCoveredText()
'''for s in sent.getRootConstituent().children:
  print(s.getIndex())
print([s.position for s in sent.getRootConstituent().getAllLeafs()])
print('effort' in sent.getRootConstituent().getCoveredText())'''
#root = ConstituentStructureElement('S', 0)
#el1 = ConstituentStructure(root)
#print(el1.root.toString())
#el1.root.addChild(ConstituentStructureElement('NP', 0))
#el1.root.addChild(ConstituentStructureElement('VP', 1))
#print('A  ' + el1.root.toString())
#print('B  ' + el1.clone().getRoot().toString())
#el1.root.getChildAtIndex(0).addChild(ConstituentStructureElement('DT', 0))
#el1.root.getChildAtIndex(1).addChild(ConstituentStructureElement('BT', 0))
#print('A  ' + el1.root.toString())
#print('B  ' + el1.root.clone().toString())
'''print(el1.root.getStructureElementByIndexChain([0,0]).toString())
nc = ConstituentStructureElement('NP', 0)
nc.addChild(ConstituentStructureElement('DT', 0))
el1.root.addChild(nc)
print(print('C  ' + el1.root.toString()))'''
ceg = sentu.ceg
print(ceg.getCause())
print(ceg.getEffect())
#r1 = Utils.resolvePrefix(ceg.getCause(), Utils.punctuationsPrefix, True)
#print(r1)
#print(re.sub("(\S)\s\.", r"\1.", r1))
#print(s)
'''processedExpression1 = ceg.getCause()
processedExpression1 = Utils.resolveContractions(processedExpression1, True)
processedExpression1 = Utils.resolvePunctuations(processedExpression1, True)
processedExpression2 = ceg.getEffect()
#print(processedExpression1)
processedExpression2 = Utils.resolveContractions(processedExpression2, True)
processedExpression2 = Utils.resolvePunctuations(processedExpression2, True)
print(processedExpression2)
#print(re.sub("(\S*)\s?(\<)+(\S*)(\>)+\s?(\S*)", r"\1 \2 \3 \4 \5", ceg.getEffect()))
print('\n\n')'''
'''s1 = 'Should a subsystem fail (e. g. one detector, one instrument)'
print(re.sub("(\W\w)\.\Z", r"\1 .", s1).strip())'''
ccg = ConstituentCommandGenerator()
ccg.setOPFParser(None, an)
cmd = ccg.generateCommandPatterns(sent, ceg)
if cmd is not None:
  print(cmd.getCommandStrings())
  print(cmd.generateGraphFromSentence(sent))
  print(ceg)
  #print(processedExpression1 + ' --> ' + processedExpression2)
  if cmd.isApplicable(sent, ceg):
    print('YES!')
  else:
    print('PO')

'''ptd = PatternDatabase()
sample_noncausal = [SNLP.create_sentence(s.sentence) for s in st[:2]]
csg = ConstituentStructureGenerator()
print(csg.generateStructure(sent).toString())
pta = Pattern(1, csg.generateStructure(sent), cmd)
pta.addSentence(sent)

diffu = Differentiator(ptd, ccg)
diffu.addConstraintGenerator(LexicalConstraintGenerator())
print(pta.toString())
print([s.getSentenceText() for s in sample_noncausal])
result = diffu.deflectFromNoncausal(pta, sample_noncausal)
print(result)
print(pta.toString())
#print(sent.getSentenceText())
#print(sent.getRootConstituent().toString(False, True))
#print(sent.getRootConstituent().toString(True, False))
#print(sent.getRootConstituent().structureToString(False))
#sent1 = st[60].sentence
#sent1 = "The user record shall inherit all specified role(s) settings in the template when the user record is created from the user template."
#tr = get_tree(st[109].sentence)
for leafPos in tr.treepositions('leaves'):
  if tr[leafPos] == '-LRB-':
    tr[leafPos] = '('
  elif tr[leafPos] == '-RRB-':
    tr[leafPos] = ')' '''

#print(tr.getRootConstituent().getCoveredText())
#t = st[19].sentence #"172.18.10. etc."
#t = re.sub("\s\((\S[^\)]+)\)\s", r" ( \1 ) ", t).strip()
#t = re.sub("(.*[^\.]\S)\.$", r"\1 .", t).strip()
#t = Utils.resolveHyphen(t)
#print(t)
#s2 = re.sub("(\setc\.)\)\Z", r"\1 )", s2).strip()
tr = get_tree(s2)
#print(tr)
tr = ParentedTree.fromstring(str(list(tr)[0][0]))
tr.pretty_print()
#print(tr.leaves())

#sent2 = Utils.resolveContractions(sent1, False)
#sent2 = Utils.resolvePunctuations(sent1, True)
#print(sent2)
#if sent1 == sent2:
#  print(True)

'''from nltk.parse.corenlp import CoreNLPDependencyParser
dep_parser = CoreNLPDependencyParser(url='https://corenlp.run')
parses, = dep_parser.raw_parse(st[139].sentence)
#print([[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses])
dep = []
l = parses.to_conll(4).split('\n')
for i, p in enumerate(l[:-1]):
  t = p.split('\t')
  #print(type(t[2]))
  dep.append((t[3], int(t[2]), i+1))
  
print(dep)'''

# [('ROOT', 0, 9), ('det', 4, 1), ('amod', 3, 2), ('compound', 4, 3), ('nsubj:pass', 9, 4), ('punct', 4, 5), ('dep', 4, 6), ('punct', 9, 7), ('aux:pass', 9, 8), ('mark', 11, 10), ('xcomp', 9, 11), ('det', 13, 12), ('obj', 11, 13), ('case', 15, 14), ('nmod', 13, 15), ('nsubj', 18, 16), ('aux', 18, 17), ('acl:relcl', 13, 18), ('case', 22, 19), ('punct', 22, 20), ('compound', 22, 21), ('compound', 25, 22), ('punct', 22, 23), ('amod', 25, 24), ('obj', 18, 25), ('punct', 25, 26), ('nsubj', 29, 27), ('cop', 29, 28), ('acl:relcl', 25, 29), ('case', 34, 30), ('det', 34, 31), ('compound', 33, 32), ('compound', 34, 33), ('nmod', 29, 34), ('punct', 9, 35)]

'''import spacy

from nltk.stem import WordNetLemmatizer
nlp = spacy.load('en_core_web_md')

lemmatzr = WordNetLemmatizer()
lemma1 = lemmatzr.lemmatize('If')
lemma2 = lemmatzr.lemmatize('When')
words = lemma1 + ' ' + lemma2

tokens = nlp(words)
  
token1, token2 = tokens[0], tokens[1]
  
print("Similarity:", token1.similarity(token2))'''