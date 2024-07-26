def GenerateQuestions(passage):
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    #generate the questions first
    model.load_state_dict(torch.load("model_state.pt"))
    model.to(device)
    model.eval()

    length = len(passage)
    start, end = 0, 0
    questions = []
    fullstops = 0
    for i in range(length // 2):
        if i == ".":
            fullstops += 1
            
    if fullstops > 4:
        for i in range(10):
            end = int((i + 1) / 10 * length)
            while end < length and passage[end] != ".":
                end += 1
            if end < length and passage[end] == ".":
                end += 1
            question = RunInference(passage[start:end], tokenizer, model, device)
            questions.append((question, passage[start : end]))
            start = end
    else:
        for i in range(10):
            end = int((i + 1) / 10 * length)
            question = RunInference(passage[start:end], tokenizer, model, device)
            questions.append((question, passage[start : end]))
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
        startOfOption = 0
        currentOption = 0
        correctOption = ord(options[-1]) - 65
        for optionsIndex in range(len(options)):
            if options[optionsIndex] == '&' or options[optionsIndex] == '#':
                option = options[startOfOption:optionsIndex]
                optionsDic[option] = currentOption == correctOption
                currentOption += 1
                startOfOption = optionsIndex + 1
                
        output[questions[i]] = optionsDic

    return output


def GenerateMore(passage):
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    #generate the questions first
    model.load_state_dict(torch.load("model_state.pt"))
    model.to(device)
    model.eval()

    length = len(passage)
    start, end = 0, 0
    questions = []

    fullstops = 0
    for i in range(length // 2):
        if i == ".":
            fullstops += 1

    if fullstops > 4:
        while len(questions) < 10:
            mid = random.randint(0, length - 1)
            start, end = mid, mid

            while start > 0 and start != ".":
                start -= 1
            while end < length and end != ".":
                end += 1
            if end < length and end != ".":
                end += 1
            
            question = RunInference(passage[start:end], tokenizer, model, device)
            if question not in questions:
                questions.append((question, passage[start : end]))
            else:
                continue
    else:
        while len(questions) < 10:
            start = random.randint(0, length - 1)
            end = start
            while end < length and end - start < length // 5:
                end += 1

            question = RunInference(passage[start:end], tokenizer, model, device)
            if any(q[0] == question for q in questions):
                continue
            else:
                questions.append((question, passage[start:end]))
                
    model.load_state_dict(torch.load("options_model_state.pt"))
    model.to(device)
    model.eval()

    start, end = 0, 0
    output = {}

    for i in range(10):
        start = end
        end = int((i + 1) / 10 * length)
        optionsPrompt = f"passage: {passage[start:end]} question: {question[i][0]}"
        options = RunInference(optionsPrompt, tokenizer, model, device)

        optionsDic = {}
        startOfOption = 0
        currentOption = 0
        correctOption = ord(options[-1]) - 65
        for optionsIndex in range(len(options)):
            if options[optionsIndex] == '&' or options[optionsIndex] == '#':
                option = options[startOfOption:optionsIndex]
                optionsDic[option] = currentOption == correctOption
                currentOption += 1
                startOfOption = optionsIndex + 1
                
        output[questions[i]] = optionsDic

    return output