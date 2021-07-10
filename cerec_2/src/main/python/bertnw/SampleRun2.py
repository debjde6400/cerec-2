import os
import sys
#os.chdir('..' + os.path.sep + '..')
sys.path.append(os.getcwd())

from datetime import datetime
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
torch.cuda.empty_cache()

import numpy as np
import pandas as pd
#from pylab import rcParams
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from collections import defaultdict

from torch import nn

# packages for adding pos tags
import spacy
from python.bertnw.CausalClassifier import CausalClassifier
import python.bertnw.DataHandling as DH

currentTime = str(datetime.now())
model_save_name = 'causal_classifier_' + currentTime + '.bin'
use_pos_tags = False

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

df = pd.read_csv("./resources/input/cira/annotation_causal.csv", encoding='utf-8') 

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
df = df[:2000]

class_names = ['not causal', 'causal']

# Class count
count_class_non_causal, count_class_causal = df.Label.value_counts()

# Divide by class
df_class_non_causal = df[df['Label'] == 0]
df_class_causal = df[df['Label'] == 1]

# undersample "non causal" class
df_class_non_causal_under = df_class_non_causal.sample(count_class_causal)
df_undersampled = pd.concat([df_class_non_causal_under, df_class_causal], axis=0)

print('Random under-sampling:')
print(df_undersampled.Label.value_counts())

# add POS Tags to sentences
#import en_core_web_sm
df = df_undersampled
MAX_LEN = 384

if use_pos_tags == True:
    nlp = spacy.load('en_core_web_sm')
    #nlp = en_core_web_sm.load()

    for index, row in df.itertuples():
        doc = nlp(row['Sentence'])
        new_sentence = ""

        for token in doc:
          new_sentence += token.text + "_" + token.dep_ + " "

        df.loc[index, 'Sentence'] = new_sentence

print(df.head())

PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

token_lens = []

for txt in df.Sentence:
  tokens = tokenizer.encode(txt, max_length=512, truncation=True)
  token_lens.append(len(tokens))
  
df_train, df_test = train_test_split(df, test_size=0.2, random_state=RANDOM_SEED)
df_val, df_test = train_test_split(df_test, test_size=0.5, random_state=RANDOM_SEED)

BATCH_SIZE = 16

train_data_loader = DH.create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
val_data_loader = DH.create_data_loader(df_val, tokenizer, MAX_LEN, BATCH_SIZE)
test_data_loader = DH.create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

bert_model = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)

model = CausalClassifier(len(class_names))
model = model.to(device)

EPOCHS = 10
LEARNING_RATE = 2e-5

optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, correct_bias=False)
total_steps = len(train_data_loader) * EPOCHS

scheduler = get_linear_schedule_with_warmup(
  optimizer,
  num_warmup_steps=0,
  num_training_steps=total_steps
)

loss_fn = nn.CrossEntropyLoss().to(device)

history = defaultdict(list)
best_accuracy = 0

for epoch in range(EPOCHS):

  print(f'Epoch {epoch + 1}/{EPOCHS}')
  print('-' * 10)

  train_acc, train_loss = DH.train_epoch(
    model,
    train_data_loader,    
    loss_fn, 
    optimizer, 
    device, 
    scheduler, 
    len(df_train)
  )

  print(f'Train loss {train_loss} accuracy {train_acc}')

  val_acc, val_loss = DH.eval_model(
    model,
    val_data_loader,
    loss_fn, 
    device, 
    len(df_val)
  )

  print(f'Val   loss {val_loss} accuracy {val_acc}')
  print()

  history['epoch'].append(epoch)  
  history['batch_size'].append(BATCH_SIZE)  
  history['learning_rate'].append(LEARNING_RATE)
  history['train_acc'].append(train_acc.item())
  history['train_loss'].append(train_loss)
  history['val_acc'].append(val_acc.item())
  history['val_loss'].append(val_loss)

  if val_acc > best_accuracy:
    torch.save(model.state_dict(), model_save_name)
    best_accuracy = val_acc

pd.DataFrame(history).to_csv('training_results_' + currentTime + '.csv', mode='a')

test_acc, _ = DH.eval_model(
  model,
  test_data_loader,
  loss_fn,
  device,
  len(df_test)
)

text_file = open("test_acc.txt", "a")
n = text_file.write('Test Accuracy of the best model (highest val accuracy): ' + str(test_acc.item()) + "\n")
text_file.close()

print(test_acc.item())


y_requirement_texts, y_pred, y_pred_probs, y_test = DH.get_predictions(
  model,
  test_data_loader,
  device
)

report = classification_report(y_test, y_pred, target_names=class_names, output_dict=True)
df_report = pd.DataFrame(report).transpose()

df_report.to_csv("classification_report_BERT.csv")

print(classification_report(y_test, y_pred, target_names=class_names))

idx = 5

sentence_text = y_requirement_texts[idx]
true_label = y_test[idx]
pred_df = pd.DataFrame({
  'class_names': class_names,
  'values': y_pred_probs[idx]
})

from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

text_file = open("test_acc.txt", "a")
n = text_file.write('AUC Score of the best model (highest val accuracy): ' + str(roc_auc_score(y_test, y_pred)) + "\n")
text_file.close()

print(''.join(sentence_text))
print(f'True sentiment: {class_names[true_label]}')