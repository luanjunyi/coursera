import sys, os, re
from collections import defaultdict

def simple_reduce(word):
    return '_RARE_'

def is_num(word):
    return re.match(".*[0-9].*", word) is not None

def is_all_cap(word):
    return word.isupper()

def is_last_cap(word):
    return word[-1].isupper()

def four_class_reduce(word):
    if is_num(word):
        return '_DIGITS_'
    if is_all_cap(word):
        return '_ALLCAP_'
    if is_last_cap(word):
        return '_LASTCAP_'
    return '_RARE_'

def reduce_rare(infile_path, reducer = simple_reduce):
    word_count = defaultdict(int)

    with open(infile_path) as infile:
        line = infile.readline()
        while line:
            line = line.strip()
            if line:
                words = line.split(" ")
                words = words[:-1]
                for word in words:
                    word_count[word] += 1
            line = infile.readline()

    with open(infile_path) as infile:
        line = infile.readline()
        while line:
            line = line.strip()
            if line:
                word, tag = line.split(" ")
                if word_count[word] < 5:
                    word = reducer(word)
                print word, tag
            else:
                print ''
            line = infile.readline()

if __name__ == "__main__":
    infile = sys.argv[1]
    if len(sys.argv) > 2:
        reducer = eval(sys.argv[2])
    else:
        reducer = simple_reduce
    reduce_rare(infile, reducer)
