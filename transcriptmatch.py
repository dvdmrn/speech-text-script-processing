#!usr/bin/env python

import re
from pprint import pprint
import csv 

SCRIPT_PATH = "script.txt"
CSV_PATH = "transcript.csv"
TRANSCRIPTION = ""
keywords = []

f = open("script.txt")
text = f.read()
text = text.lower()
txtList = text.split(" ")

def get_directions(corpus):
    # direction_pattern = re.compile("© \[(\w|\s|\.|\,|\/|\#|\!|\$|\%|\^|\&|\*|\;|\:|\{|\}|\=|\-|\_|\`|\~|\(|\)|\'|\’)+\]")

    direction_pattern = re.compile(r"© \[(.*?)\]")
    # direction_pattern = re.compile("© \[[\w\s.,/#!$%^&*;:=\-_`~()'’]+]")

    directions = direction_pattern.findall(corpus) 
    print("found directions: -------------------------")
    pprint(directions)
    return directions

def prep_corpus(purgeList, corpus):
    print("IN: ",corpus)
    print("purge list:",purgeList)
    new_corpus = corpus
    for i in range(0,len(purgeList)):
        print("\n\nremoving: ","["+purgeList[i]+"] for:"+str(i))
        new_corpus = new_corpus.replace("["+purgeList[i]+"]","<"+str(i)+">",1)
        pprint(new_corpus)
    new_corpus = new_corpus.replace("© ","")
    print("OUT: ",new_corpus)
    return new_corpus

def remove_traces(corpus):
    pattern = re.compile(r"©\d+")
    result = pattern.sub("",corpus)
    return result


def get_keywords(corpus,directions):
    """
    corpus:= string
    returns: list of Dicts
    """
    txtlst = corpus.split(" ")
    keywords = [] # {"w":"word","i":"index"}
    acc = 0
    for i in range(0,len(txtlst)-1):
        if "©" in txtlst[i]:
            keywords.append({
                "w":txtlst[i+1],
                "i":i,
                "direction":directions[acc]
                })
            acc+=1
    # print("keywords: -------------------------")
    # pprint(keywords, indent=4)
    return keywords

def getCSV():
    transcript = []
    with open(CSV_PATH,"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transcript.append(row)
        return transcript


# def collocation_search(transcript,keywords,script):
#     sl = script.split(" ")
#     # sl = [i for i in isl if i != ""]
#     # pprint(sl)
#     for kw in keywords:
#         for i in range(0,len(sl)):
#             degree = collocation_degree(kw,script,transcript,i)
#             print(degree)
#         print(degree)
#         # print(kw["i"],sl[max(0,kw["i"])])

# def collocation_degree(kw, script, transcript, iOffset):
#     # print("ioffset: ",iOffset)
#     s0 = script[max(0,iOffset-2)]
#     s1 = script[max(0,iOffset-1)]

#     sroot = script[max(0,iOffset)]
#     s2 = script[min(len(script)-1,iOffset+1)]
#     s3 = script[min(len(script)-1,iOffset+2)]

#     t0 = transcript[max(0,iOffset-2)]
#     t1 = transcript[max(0,iOffset-1)]
#     troot = transcript[max(0,iOffset)]
#     t2 = transcript[min(len(transcript)-1,iOffset+1)]
#     t3 = transcript[min(len(transcript)-1,iOffset+2)]

#     matchDegree = 0
#     matchDegree += 1 if s0==t0 else matchDegree   
#     matchDegree += 1 if s1==t1 else matchDegree   
#     matchDegree += 1 if sroot==troot else matchDegree   
#     matchDegree += 1 if s2==t2 else matchDegree   
#     matchDegree += 1 if s3==t3 else matchDegree   

#     return matchDegree


def get_ngrams(dirs,script):
    """
    note: script now looks like blah blah (c)<index> blah blah
    """
    ngrams = [] # list of dicts
    script_words = script.split(" ")
    pprint(script_words)
    for i in range(0,len(script_words)-len(dirs)):
        if "<" and ">" in script_words[i]:
            dirIndex = int(script_words[i][1:-1])
            del script_words[i]
            # i += 1
            ngram = get_ngram_forward(i,script_words)
            ngrams.append({"ngram":ngram,"dir":dirs[dirIndex]})
    pprint(ngrams)
    return ngrams

# def get_ngram_symmetrical(index,corpus):
#     """
#     strives to get a 5 gram
#     Requires: len(corpus) > 5

#     corpus :=  list of words
#     index := int

#     returns a tuple such that
#     (0:= a list of words (the ngram),
#      1:= the seed word (string)
#     )
#     """
#     max_tail_length = 2
    
#     # length of right and left tails bounded by array size
#     rightTail = min((len(corpus)-1)-index,max_tail_length) 
#     leftTail = min(index,max_tail_length)

#     # tops up left or right tail to ensure it's a 5gram
#     # 
#     overflowRight = max_tail_length - leftTail 
#     overflowLeft = max_tail_length - rightTail
#     rightTail += overflowRight
#     leftTail += overflowLeft

#     ngram = []
#     for i in range(1,leftTail+1):
#         left = leftTail+1-i
#         ngram.append(corpus[index-left])

#     ngram.append(corpus[index])
#     for j in range(1,rightTail+1):
#         nxt = corpus[index+j]
#         if "<" and ">" in nxt: # prevents from appending <n>s
#             ngram.append(corpus[index+j+1])
#         else:
#             ngram.append(corpus[index+j])
#     return (ngram,corpus[index])

def get_ngram_forward(index,corpus):
    """
    strives to get a 5 gram
    Requires: len(corpus) > 5

    corpus :=  list of words
    index := int

    returns: list of words
    """
    n = 5
    
    # length of right and left tails bounded by array size
    rightTail = min((len(corpus)-1)-index,n) 

    ngram = []
    
    ngram.append(corpus[index])
    for j in range(1,rightTail+1):
        nxt = corpus[index+j]
        if "<" and ">" in nxt: # prevents from appending <n>s
            ngram.append(corpus[index+j+1])
        else:
            ngram.append(corpus[index+j])
    return ngram

def match_degree(ngram,tosearch):
    """
    for a given ngram, find the degree to which
    it matches in a corpus tosearch
    ngram:= a list of words
    tosearch:= a list of words

    returns a best_candidate which is a (match_degree,index in tosearch)
    """
    depth = len(ngram)
    matchDegree = 0
    degrees = []
    for i in range(0,len(tosearch)-depth): 
        for j in range(0,depth): # compare sequence of 5 words (indexed by j, offset by i) to an ngram
            if tosearch[i+j]["word"] in ngram:
                matchDegree += 1
        degrees.append((matchDegree,i))
        matchDegree = 0
    best_candidate = max(degrees)
    print(best_candidate)
    print(tosearch[best_candidate[1]])
    return best_candidate

def get_matches(ngrams,transcript,directions):
    inst_candidates = []
    for ngram in ngrams:
        instruction_candidate = match_degree(ngram["ngram"],transcript)
        inst_candidates.append(instruction_candidate)
    k = 0
    for c in inst_candidates:
        transcript[c[1]]["instruction"] = directions[k]
        k+=1
    return transcript

def writeCSV(transcript):
    with open('instructions.csv', 'w') as csvfile:
        fieldnames = ["t","word","instruction"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in transcript:
            writer.writerow(d)


def main():
    directions = get_directions(text)
    preppedCorpus = prep_corpus(directions,text)
    ngrams = get_ngrams(directions,preppedCorpus)
    transcript = getCSV()
    populatedTranscript = get_matches(ngrams,transcript,directions)
    writeCSV(populatedTranscript)
    # match_degree(ngrams[0]["ngram"],transcript,dire)

    # kwds = get_keywords(preppedCorpus, directions)
    # print(preppedCorpus)

    # parsableScript = remove_traces(preppedCorpus)
  
    # collocation_search(transcript,kwds,parsableScript)

main()