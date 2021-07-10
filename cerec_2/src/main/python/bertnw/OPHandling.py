import torch
from python.bertnw.CDOnlyIP import CDOnlyIP
from torch.utils.data import DataLoader
import torch.nn.functional as F

def create_data_loader2(df, tokenizer, max_len, batch_size):
  ds = CDOnlyIP(
    sentences=df.Sentence.to_numpy(),
    tokenizer=tokenizer,
    max_len=max_len
  )

  return DataLoader(
    ds,
    batch_size=batch_size,
    num_workers=4
  )

def predict_sentence_output(model, data_loader, device):
  model = model.eval()
  
  requirement_texts = []
  predictions = []
  prediction_probs = []

  with torch.no_grad():
    for d in data_loader:

      texts = d["requirement_text"]
      input_ids = d["input_ids"].to(device)
      attention_mask = d["attention_mask"].to(device)

      outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask
      )
      _, preds = torch.max(outputs, dim=1)

      probs = F.softmax(outputs, dim=1)

      requirement_texts.extend(texts)
      predictions.extend(preds)
      prediction_probs.extend(probs)

  predictions = torch.stack(predictions).cpu()
  prediction_probs = torch.stack(prediction_probs).cpu()
  return requirement_texts, predictions, prediction_probs