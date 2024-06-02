from torch.utils.data import Dataset

class QuestionData(Dataset):
    def __init__(self, path: str, tokenizer):
        self.lines = open(path, "r", encoding="utf-8").readlines()

        self.X = []
        info = ""
        mcq = None

        for line in self.lines:
            line = line.strip()
            if line == "":
                continue
            if line.startswith("Q: "):
                mcq = {"question": line, 
                       "options": [],
                       "answer": ""}
            elif line.startswith("A. ") or line.startswith("B. ") or line.startswith("C. ") or line.startswith("D. "):
                if mcq:
                    mcq["options"].append(line)
            elif line.startswith("Answer: "):
                if mcq:
                    mcq["answer"] = line
                    options_text = " ".join(mcq["options"])
                    formatted_text = f"<startofstring> {info} <bot>: {mcq['question']} {options_text} {mcq['answer']} <endofstring>"
                    self.X.append(formatted_text)
                    mcq = None
            else:
                if info == "":
                    info = line
                else:
                    info += " " + line

        self.X_encoded = tokenizer(self.X,max_length=40, truncation=True, padding="max_length", return_tensors="pt")
        self.input_ids = self.X_encoded['input_ids']
        self.attention_mask = self.X_encoded['attention_mask']

    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx], self.attention_mask[idx]
    