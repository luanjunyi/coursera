def gen_sentence(f):
    w = gen_token(f)
    sent = []
    for token in w:
        if token == '':
            yield sent
            sent = []
        else:
            sent.append(token)

def gen_token(f):
    for line in f:
        yield line.strip()

def gen_sentence_train(f):
    w = gen_token_train(f)
    sent = []
    for token, tag in w:
        if token is not None:
            sent.append((token, tag))
        else:
            yield sent
            sent = []
        

def gen_token_train(f):
    for line in f:
        line = line.strip()
        yield [None, None] if line == '' else line.split()

def argmax(lst):
    return max(lst, key = lambda x: x[1])[0]
