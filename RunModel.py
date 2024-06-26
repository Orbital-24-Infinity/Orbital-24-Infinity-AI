import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(device)

def run_inference(passage):
    input_text = f"passage: {passage}"
    input_enc = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding='max_length')
    input_ids = input_enc.input_ids.to(device)
    attention_mask = input_enc.attention_mask.to(device)
    
    outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=512)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text

if __name__ == "__main__":
    while True:
        model.load_state_dict(torch.load("model_state.pt"))
        model.to(device)
        model.eval()

        passage = input("Enter passage: ")
        length = len(passage)
        print("\n")

        start, end = 0, 0
        questions = []
        for i in range(1, 11):
            end = int(i / 10 * length)
            question = run_inference(passage[start:end])
            if question not in questions:
                questions.append(question)
            else:
                question.append("repeat qestion")
            start = end

        model.load_state_dict(torch.load("options_model_state.pt"))
        model.to(device)
        model.eval()

        start, end = 0, 0

        for i in range(1, 11):
            if question[i - 1] == "repeat qestion":
                continue
            end = int(i / 10 * length)
            options = run_inference(f"passage: {passage[start:end]} question: {question[i - 1]}")
            print(questions[i - 1])
            print({options})
            start = end