import nltk
from europython.bigram_editor import *
from europython.freqs_editor import *
from europython.info_collector import *

file = "/home/lehthelj/Kielitieteet/lopputyö/EuroPython/EuroParl_EnglishExcerpt.txt"
text = open(file, "r").read()
tokenized = nltk.word_tokenize(text)
nltktext = nltk.Text(tokenized)

def make_word_info_file():
    collect_info(text)
    find_similar_freqs()

def make_bigram_chart():
    bigrams_to_chart(25)

def make_w_pair_chart():
    freqs = json.loads(open("freqs.py", "r").read())
    file = open("word_pair_chart.txt", "w")
    file.close()
    word_pair_freq_chart("great", freqs, 30)
    word_pair_freq_chart("large", freqs, 30)


"""
TODO:
collect_info() updated, update find_word_freqs()
make find_bigrams() so that it ignores the upper case
Tag words and analyse
more statistics
"""

# make_word_info_file()
# make_w_pair_chart()
# make_bigram_chart()
compare_next_words()