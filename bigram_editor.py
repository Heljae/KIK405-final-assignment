import nltk
import json
import sys
from math import log2


def find_bigrams(nltktext):
    bis = nltk.collocations.BigramCollocationFinder.from_words(nltktext).ngram_fd
    bigrams_dict = {f"{a}||{b}": count for (a, b), count in bis.items()}
    with open("bigrams.json", "w") as file:
        json.dump(bigrams_dict,file)

def find_from_bigrams(word, index=0):
    """if index == 0, word is on the right, with 1 on the left
    """
    with open("bigrams.json", "r") as file:
        bigrams = json.load(file)
    result = []
    
    for words, num in bigrams.items():
        a, b = words.split("||")
        if index == 0:
            if a == word:
                result.append((b,num))
        else:
            if b == word:
                result.append((a,num))
    return result

def bigrams_to_chart(max_counter):
    great_r = find_from_bigrams("great", 0)
    great_l = find_from_bigrams("great", 1)

    large_r = find_from_bigrams("large", 0)
    large_l = find_from_bigrams("large", 1)

    max_len = max([len(great_r), len(great_l), len(large_l), len(large_r)])

    great_r = sorted(great_r, key=lambda data: data[1], reverse=True) # longest

    if len(great_l) < max_len:
        great_l += (max_len-len(great_l))*[(0,0)]
        great_l = sorted(great_l, key=lambda data: data[1], reverse=True)

    if len(large_r) < max_len:
        large_r += (max_len-len(large_r))*[(0,0)]
        large_r = sorted(large_r, key=lambda data: data[1], reverse=True)

    if len(large_l) < max_len:
        large_l += (max_len-len(large_l))*[(0,0)]
        large_l = sorted(large_l, key=lambda data: data[1], reverse=True)

    counter = 0

    if max_counter == -1:
        max_counter = len(great_r)+1

    stdoutOrigin = sys.stdout
    sys.stdout = open("bigrams_chart.txt", "w")

    print((6*15)*"_")
    for i in range(max_len):
        if counter == max_counter:
            break
        counter += 1
        print("| " + "{:<20}".format(f"{great_r[i][0]}: {great_r[i][1]}") + "| " + "{:<20}".format(f"{great_l[i][0]}: {great_l[i][1]}") + "|| " + "{:<20}".format(f"{large_r[i][0]}: {large_r[i][1]}") + "| " + "{:<20}".format(f"{large_l[i][0]}: {large_l[i][1]}") + " |")
    print((6*15)*"_")

    sys.stdout.close()
    sys.stdout = stdoutOrigin


def word_pair_freq_chart(word, freq: dict, counter_top):
    """word1 either great or large
    if counter top == -1, it prints all
    """


    bigrams = find_from_bigrams(word, 0)
    results = []
    for (w, n) in bigrams:
        results.append((w, freq[w], n))
    results = sorted(results, key=lambda data: data[2], reverse=True)

    counter = 0
    if counter_top == -1:
        counter = len(results)

    stdoutOrigin = sys.stdout
    sys.stdout = open("word_pair_chart.txt", "a")

    print(((3*18-4)*"_"))
    print("| " + "{:20}".format("word") + " | " + "{:10}".format("word freq") + " | " + "{:10}".format(f"{word}-word freq") + " |")
    print("|" + (3*18-2-4)*"_" + "|")
    for (w, wf, wpf) in results:
        counter += 1
        print("| " + "{:20}".format(f"{w}") + " | " + "{:10}".format(f"{wf}") + " | " + "{:10}".format(f"{wpf}") + " |")
        if counter == counter_top:
            break
    print("|" + (3*18-2-4)*"_" + "|")
    print((3*18*"_") + "\n\n")

    sys.stdout.close()
    sys.stdout = stdoutOrigin

def measure_similarity(word1, word2, freqs: dict):
    words = find_bigrams(word1, 0)
    
    total = 5452422    # from word_info.txt
    w1_count = freqs[word1]
    w2_count = freqs[word2]


    for (w,n) in words:
        if w == word2:
            freq_w1_w2 = n
            break

    return log2((freq_w1_w2*total)/(w1_count*w2_count))

def similar_lytics(word1:str, word2:str, nltktext):
    w1 = nltktext.similar(word1).split()
    w2 = nltktext.similar(word2).split()

    results = []

    for w in w1:
        if w in w2:
            results.append(w)
    return results

def compare_next_words():
    """Finds the next word and compares them for the best word
    """
    great_next = find_from_bigrams("great",0)
    large_next = find_from_bigrams("large", 0)

    g_dict = {}
    for (w, n) in great_next:
        g_dict[w] = n
    l_dict = {}
    for (w, n) in large_next:
        l_dict[w] = n

    more_in_great = []
    more_in_large = []

    for w, n in g_dict.items():
        if w in l_dict:
            if n >= l_dict[w]:
                more_in_great.append((w, n-l_dict[w], n, l_dict[w])) # word, minus, word num in great, word num in large
            else:
                more_in_large.append((w, l_dict[w]-n, n, l_dict[w]))
        else:
            # doesn't appear after large
            more_in_great.append((w, n, n, 0))

    for (w,n) in l_dict.items():
        if w not in g_dict:
            more_in_large.append((w, n, 0, n))

    more_in_great = sorted(more_in_great, key=lambda data: data[1], reverse=True)
    more_in_large = sorted(more_in_large, key=lambda data: data[1], reverse=True)

    compare_2_chart(more_in_great, more_in_large)

def compare_2_chart(l1, l2):
    """makes a chart of the 2 lists
    list = (compared word, minus amounts, num in great, num in large)
    """

    file = "comaring_next_word.txt"
    counter = 0

    stdoutOrigin = sys.stdout
    sys.stdout = open(file, "w")

    print((6*10)*"_")
    for (w, num, g_num, l_num) in l1:
        if counter == 25:
            break
        counter += 1
        print("| " + "{:<20}".format(f"{w}") + "| " + "{:<9}".format(f"{num}") + "| " + "{:<9}".format(f"{g_num}") + "| " + "{:<9}".format(f"{l_num}") + " |")
    print((6*10)*"_")

    counter = 0

    print("\n\n" + (6*10)*"_")
    for (w, num, g_num, l_num) in l2:
        if counter == 25:
            break
        counter += 1
        print("| " + "{:<20}".format(f"{w}") + "| " + "{:<9}".format(f"{num}") + "| " + "{:<9}".format(f"{g_num}") + "| " + "{:<9}".format(f"{l_num}") + " |")
    print((6*10)*"_")

    sys.stdout.close()
    sys.stdout = stdoutOrigin