import os, sys
#os.chdir('..' + os.path.sep + '..')
sys.path.append(os.getcwd())
import pandas as pd
import python.sentence.StanfordCoreNLP_ann as SNLP
import python.data.DataPaths as DP


df = pd.read_csv('./resources/input/cira/annotation_causal.csv', encoding='utf-8') 

# As the sentences are labeled by multiple annotators, we need to merge all labels into one colum.
# looks like = 1,1,1,1,1...
df['Label'] = df[df.columns[1:7]].apply(
    lambda x: ','.join(x.dropna().astype(str)),
    axis=1
)

# After that we just need to use the first label of the merged colum.
# Different labeling decisions are already discussed in our labeling process.
for index, row in df.iterrows():
    df.at[index,'Label'] = int(float(row['Label'][0:3]))

# to make further processing easier we can drop unncessary columns
df.drop(df.columns[[1,2,3,4,5,6]], axis=1, inplace=True)
#df = df[:2000]

df2 = pd.read_csv("./resources/input/cira/overall.csv")

df['Causal'] = df2['Causal']
df['Marker'] = df2['Markers']
print(df.head())

arr = []
import pickle

for fpath in DP.PURE_COLL_min:
  fname = fpath.split(os.path.sep)[-1][:-5]
  fp = open("./resources/output/untrained_" + fname + "_patterns.bin", 'rb')
  try:
    arr.extend(pickle.load(fp))
  except EOFError:
    print('Problemma')
  else:
    print(len(arr))

stl = []

#import re

pattern_new_sent = dict()

for row in df[:300].itertuples():
  if (row[2] == 1 and row[4] == row[4]):
    #print(str(row[0]), str(re.split(row[4], row[1], flags=re.IGNORECASE)))
    sent = SNLP.CoreNLPAnnotator(url='http://localhost:9000/').create_sentence(row[1])

    for p in arr:
      if p.isCompliant(sent):
        print('\nTrue')
        print(sent.getRootConstituent().toString(True, True))
        g1 = p.causalityExtraction.generateGraphFromSentence(sent)
        print('')
        
        if p not in pattern_new_sent:
          pattern_new_sent[p] = [(sent, g1)]
        else:
          pattern_new_sent[p].append((sent, g1))
      else:
        print('Bhow ', end='')
        
  print('  ', end='')

print('\noooooooo')
print(f'Length : {len(pattern_new_sent)}')

for k, v in pattern_new_sent.items():
  print(f"{k.getStructure().toString()}: ")
  for pr in v:
    print(f"{pr[0].getRootConstituent().getCoveredText()}")
    print(f"{str(pr[1])}")
  