from transformers import GPT2LMHeadModel, GPT2Tokenizer
from QuestionData import QuestionData
from torch.optim import Adam
from torch.utils.data import DataLoader
import tqdm
import torch

def train(QuestionData, model, optim):
    epochs = 500
    best_loss = float('inf')
    patience = 10
    trials = 0

    for i in tqdm.tqdm(range(epochs)):
        model.train()
        total_loss = 0
        for X, a in questionData:
            X = X.to(device)
            a = a.to(device)
            optim.zero_grad()
            loss = model(X, attention_mask=a, labels=X).loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # Gradient clipping
            optim.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(questionData)
        print(f"epoch {i+1}/{epochs}, Loss: {avg_loss}")

        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(model.state_dict(), "model_state.pt")
            trials = 0
        else:
            trials += 1
            if trials >= patience:
                print("Early stopping ....")
                break
        
        if (i + 1) % 10 == 0:
            torch.save(model.state_dict(), "model_state.pt")
            print(infer("Ganyu"))
        
def infer(inp):
    inp = "<startofstring> "+inp+" <bot>: "
    inp = tokenizer(inp, max_length=30, return_tensors="pt")
    X = inp["input_ids"].to(device)
    a = inp["attention_mask"].to(device)
    output = model.generate(X, attention_mask=a, max_length=50, pad_token_id=tokenizer.eos_token_id)
    output = tokenizer.decode(output[0], skip_special_tokens=True)
    return output


device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(device)

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
tokenizer.add_special_tokens({"pad_token": "<pad>",
                              "bos_token": "<startofstring>",
                              "eos_token": "<endofstring>"})
tokenizer.add_tokens(["<bot>:"])

model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
model.resize_token_embeddings(len(tokenizer))

model = model.to(device)

questionData = QuestionData("./trainingData.txt", tokenizer)
questionData = DataLoader(questionData, batch_size=64)

model.train()

optim = Adam(model.parameters(), lr=1e-5)

print("training .... ")
train(questionData, model, optim)

print("infer from model : ")
while True:
    inp = input()
    print(infer(inp))
