import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the tokenizer and model

def RunInference(passage, tokenizer, model, device):
    input_text = f"passage: {passage}"
    input_enc = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding='max_length')
    input_ids = input_enc.input_ids.to(device)
    attention_mask = input_enc.attention_mask.to(device)
    
    outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=512)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text

def GenerateQuestions(passage):
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    #generate the questions first
    model.load_state_dict(torch.load("model_state.pt"))
    model.to(device)
    model.eval()

    length = len(passage)
    start, end = 0, 0
    questions = []

    for i in range(10):
        end = int((i + 1) / 10 * length)
        question = RunInference(passage[start:end], tokenizer, model, device)
        if question not in questions:
            questions.append(question)
        else:
            questions.append("repeat question")
        start = end
    
    #then we generate the options and answers for the question
    model.load_state_dict(torch.load("options_model_state.pt"))
    model.to(device)
    model.eval()

    start, end = 0, 0
    output = {}

    for i in range(10):
        start = end
        end = int((i + 1) / 10 * length)
        if questions[i] == "repeat question":
            continue
        optionsPrompt = f"passage: {passage[start:end]} question: {question[i]}"
        options = RunInference(optionsPrompt, tokenizer, model, device)

        optionsDic = {}
        startOfOption = 1
        currentOption = 0
        correctOption = ord(options[-1]) - 65
        for optionsIndex in range(1, len(options)):
            if options[optionsIndex] == '&' or options[optionsIndex] == '#':
                option = options[startOfOption:optionsIndex-1]
                optionsDic[option] = currentOption == correctOption
                currentOption += 1
                startOfOption = optionsIndex + 1
                
        output[questions[i]] = optionsDic

    return output
 

if __name__ == "__main__":
    print("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    while True:
        passage = input("Enter passage: ")
        print(GenerateQuestions(passage))