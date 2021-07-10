import re
from nltk.tree import ParentedTree
from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from python.sentence.Node import Node
from python.sentence.Leaf import Leaf
from python.sentence.Sentence import Sentence
from python.util.Globals import Globals
#from python.util.Utils import Utils
#from nltk.parse import stanford

class CoreNLPAnnotator:
  def __init__(self, url):
    self.url = url
    self.parser = CoreNLPParser(url=self.url)
    self.dep_parser = CoreNLPDependencyParser(url=self.url)
  
  def get_len_before(self, arr, pos):
    lent = -1
    for i in range(pos):
      lent += len(arr[i]) + 1    # 1 for space
  
    return lent + 1
  
  def convert_leaves(self, tr):
    for leafPos in tr.treepositions('leaves'):
      if tr[leafPos] == '-LRB-':
        tr[leafPos] = '('
      elif tr[leafPos] == '-RRB-':
        tr[leafPos] = ')'
      
    if tr[tr.treepositions('leaves')[-1]] == '.' and re.search(r"[A-Z]*\.\B", tr[tr.treepositions('leaves')[-2]]) is not None:
      tr[tr.treepositions('leaves')[-2]] = re.sub(r"([A-Z]*)\.\B", r"\1",  tr[tr.treepositions('leaves')[-2]])
        
    return tr
  
  def leaf_actual_occurrance_count(self, sent):
    all_leaves = self.tokenize_sent(sent)
    leaf_counts = dict()
    for i, l in enumerate(all_leaves):
      if l in leaf_counts:
        leaf_counts[l].append(max(all_leaves.index(l), i))
      else:
        leaf_counts[l] = [i]
  
    return leaf_counts
  
  
  def get_from_actual(self, leaf_counts, word):
    pos = leaf_counts[word].pop(0)
    return pos
  
  def parseFeatureStructure(self, top, index, leaf_counts, tr):
    f = None
    #tr = top
  
    if len(top) == 1 and type(top[0]) is str:
      #print(top[0])
      # tokens represent leaf nodes
      POStag = top.label() #token.getPos().getPosValue();
      #print(top[0], tr.leaves().index(top[0]))
      actual_pos = self.get_from_actual(leaf_counts, top[0])
      f = Leaf(POStag, top[0], self.get_len_before(tr.leaves(), actual_pos), actual_pos, index)
      
    elif top.label() == 'ADD':
      POStag = top.label()
      actual_pos = self.get_from_actual(leaf_counts, ' '.join(top))
      f = Leaf(POStag, ' '.join(top), self.get_len_before(tr.leaves(), actual_pos), actual_pos, index)
  
    elif type(top) == ParentedTree:
      # constituents represent inner nodes
      #f = Node(constituent.getConstituentType(), constituent.getCoveredText(), index);
      f = Node(top.label(), " ".join(top.leaves()), index)
  
      # recursively traverse child nodes and add the full tree
      #if(constituent.getChildren() != null) {
      #FSArray children = constituent.getChildren();
      #for(int i = 0; i < children.size(); i++) {
  
      for i in range(len(top)):
        child = top[i]
        f.addChild(self.parseFeatureStructure(child, i, leaf_counts, tr))
    
    return f
  
  def create_sentence(self, sentence, debug=False):
    '''nlp = StanfordCoreNLP(r"D:/PFNSp/stanford-corenlp-latest/stanford-corenlp-4.2.0")
    sentence = re.sub("(\d+\.)\s", r"\1", sentence)
    #parsed = nlp.parse(sentence)
    dep_parsed = nlp.dependency_parse(sentence)
    nlp.close()
    
    jar_path = "D:/PFNSp/stanford-corenlp-latest/stanford-corenlp-4.2.0/stanford-corenlp-4.2.0.jar"
    model_path = "D:/PFNSp/stanford-corenlp-latest/stanford-corenlp-4.2.0/stanford-corenlp-4.2.0-models.jar"
    parser = stanford.StanfordParser(path_to_jar=jar_path, path_to_models_jar=model_path)'''
    
    #sentence = re.sub("\s\<([^\>]+\s[^\>]*)\>\s?", r" < \1 > ", sentence).strip()
    #sentence = re.sub("\s\'([^\']+\S)\'\s", r" ' \1 ' ", sentence)
    #sentence = re.sub("(\w)\.\s+(\w)\.(\s?)", r"\1.\2.\3", sentence).strip()
    #sentence = re.sub("(.*[^\.]\S)\.$", r"\1 .", sentence).strip()
    #if ('<' in sentence and '>' in sentence) or '-' in sentence:
      #sentence = Utils.resolvePunctuations(sentence, True)
    sentence = re.sub("\&amp\;", r"&", sentence).strip()
    sentence = re.sub("(\W\w)\.\Z", r"\1 .", sentence).strip()
    parsed = self.parser.raw_parse(sentence)
    parses, = self.dep_parser.raw_parse(sentence)
    dep_parsed = []
    l = parses.to_conll(4).split('\n')
    for i, p in enumerate(l[:-1]):
      t = p.split('\t')
      dep_parsed.append((t[3], int(t[2]), i+1))
    #print('Done')
    tr = self.convert_leaves(ParentedTree.fromstring(str(list(parsed)[0][0])))
    if debug:
      tr.pretty_print()
      print(tr.leaves())
      #print(list(self.parser.tokenize(sentence)))
    
    #opfile.writeToF1(str(tr))
    #tr = ParentedTree.fromstring(parsed)
    #converted_leaves = convert_leaves(tr.leaves())
    leaf_counts = self.leaf_actual_occurrance_count(sentence)
    #print(leaf_counts)
    tre = self.parseFeatureStructure(tr, 0, leaf_counts, tr)
    #lfs = tre.getAllLeafs()
  
    for tag in dep_parsed:
      #print(tag)
      if tag[0].upper() == 'ROOT':
        #l = [s for s in lfs if s.abs_pos == (tag[2] - 1) ]
        l = tre.getLeafByAbsPos(tag[2] - 1)
        #print(l[0].toString(), l[0].abs_pos)
        l.setDependencyRelationType('ROOT')
  
      else:
        p = tre.getLeafByAbsPos(tag[1] - 1)#[s for s in lfs if s.abs_pos == (tag[1] - 1) ]
        c = tre.getLeafByAbsPos(tag[2] - 1)#[s for s in lfs if s.abs_pos == (tag[2] - 1) ]
        #print('P :', p.toString())
        #print('C :', c.toString())
        c.setGovernor(p, tag[0])
  
    s_tre = Sentence(Globals.getInstance().getNewSentenceCounter(), tre)
    return s_tre
  
  def tokenize_sent(self, sent):
    sent = re.sub("(\setc\.)\)\Z", r"\1 )", sent).strip()
    l = list(self.parser.tokenize(sent))
    if l[0] == 'E.g':
      l[0] = 'E.g.'
    return l

#sent = "The text can span multiple sentences, and can contain arbitrary whitespace."
#create_sentence(sent)