import nltk
import json
import sys

freqs = json.loads(open("freqs.py", "r").read())

def freq_file(nltktext):    
    freq = dict(nltk.FreqDist(nltktext))

    new_file = open("freqs.py", "w")
    json.dump(freq, new_file)
    new_file.close()

def find_word_freqs(word):
    """finds the frequency from a string
    adds the frequensies to word_info.txt
    """

    if word not in freqs:
        return word, 0
    else:
        return word, freqs[word]

def find_similar_freqs():
    similar_great = "the major real considerable new european serious political greater \
                huge good clear important special significant general particular some\
                specific necessary"

    similar_large = "the small european new other major all great these certain specific\
        clear national different political good huge public important first"
    
    words = similar_great.split()
    words2 = similar_large.split()
    results2 = {}
    results = {}

    for word in words:
        found = find_word_freqs(word)
        results[found[0]] = found[1]
        
    for word in words2:
        found = find_word_freqs(word)
        results2[found[0]] = found[1]

    stdoutOrigin=sys.stdout 
    sys.stdout = open("word_info.txt", "a")

    print("\n\nHow often the frequensies of similar words to great occur:")
    print(results)
    print()
    print("How often the frequensies of similar words to large occur:")
    print(results2)

    sys.stdout.close()
    sys.stdout=stdoutOrigin