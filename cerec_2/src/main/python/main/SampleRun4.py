import pandas as pd
import re
from bs4 import BeautifulSoup as BSHTML

def get_sentences_from_file_with_annotations(file_path):
  fl = open(file_path, 'r')
  flc = fl.read().split('\n\n')
  dictEnt = {}
  for st in flc[:1000]:
    lines = st.split('\n')
    dictEnt.update({re.sub('"', '', lines[0].split('\t')[1]) : lines[1]})

  for (key, value) in dictEnt.items():
    if value.find('Cause-Effect(e1,e2)') > -1:
        dictEnt[key] = 1
    elif value.find('Cause-Effect(e2,e1)') > -1:
        dictEnt[key] = 2
    elif value.find('(e1,e2)') > -1:
        dictEnt[key] = 0
    else:
        dictEnt[key] = -1

  df = pd.DataFrame(dictEnt.items(), columns=['sent', 'label'])
  return df

file_path = "./resources/input/semevaltask8/SemEval2010_task8_training/TRAIN_FILE.TXT"
df = get_sentences_from_file_with_annotations(file_path)
print(df[df['label'] >= 1])

e1 = []
e2 = []

for text in df['sent']:
  e1.append(BSHTML(text, features="lxml").e1.contents[0].strip())
  e2.append(BSHTML(text, features="lxml").e2.contents[0].strip())

print(e1[:10])
print(e2[:10])

for i in range(len(df)):
  if df.loc[i, 'label'] in [0,1]:
    df.loc[i, 'e1'], df.loc[i, 'e2'] = e1[i], e2[i]

  elif df.loc[i, 'label'] in [-1,2]:
    df.loc[i, 'e1'], df.loc[i, 'e2'] = e2[i], e1[i]
    df.loc[i, 'label'] = 1 if df.loc[i, 'label'] == 2 else 0
    
print(df.head(20))

df2 = df[df['label'] == 1]

df2.reset_index(inplace=True)

for i in range(len(df2)):
  s = df2.loc[i, 'sent']
  new_s = re.sub('</*e.>', '', s)
  new_s = re.sub('[\.\?\!]$', '', new_s)
  df2.loc[i, 'sent'] = new_s
  
df2.drop(columns=['index'], inplace=True)
#print(df2.head())

'''d = {'index': [], 'sent': [], 'label': [], 'e1': [], 'e2': []}
for row in df2.itertuples():
  d['index'].append(row[1])
  d['sent'].append(row[2])
  d['label'].append(0)
  d['e1'].append(row[5])
  d['e2'].append(row[4])

df3 = pd.DataFrame(d)
print(df3.head())

dff = pd.concat([df2, df3], ignore_index=True)
dff = dff.sample(frac=1).reset_index(drop=True)
'''

from graphviz import Source
from nltk.parse.corenlp import CoreNLPDependencyParser
s = df2.loc[0, 'sent']
print(s)
print(df2.loc[0, 'e1'])
print(df2.loc[0, 'e2'])
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000/')
parses, = dep_parser.raw_parse(s)
#print([[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses])
dep = []
l = parses.to_conll(4).split('\n')
for i, p in enumerate(l[:-1]):
  t = p.split('\t')
  #print(type(t[2]))
  dep.append((t[3], int(t[2]), i+1))
  
print(dep)
Source(parses.to_dot()).render('g1.gv', view=True)