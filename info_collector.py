import re
import sys
import nltk


def collect_info(text):
    """Collects info of the words and prints it into a separate file
    """

    great_variants = re.findall("[gG]reat\w*", text)
    large_variants = re.findall("[Ll]arge\w*", text)

    tokenized = nltk.word_tokenize(text)
    nltktext = nltk.Text(tokenized)

    name = "word_info.txt"
    tokens = len(nltktext)
    
    great_count = 0
    greats = {}
    for word in list(set(great_variants)):
        amount = nltktext.count(word)
        great_count += amount
        if word not in greats:
            greats[word] = 0
        greats[word] += amount
    
    large_count = 0
    larges = {}
    for word in list(set(large_variants)):
        amount = nltktext.count(word)
        large_count += amount
        if word not in larges:
            larges[word] = 0
        larges[word] += amount
    
    new_file = open(name, "w")
    new_file.write(f"Number of tokens: {tokens}\n")
    new_file.write(f"\nThe word great appears {great_count} times\n\n")
    
    new_file.write("Great variants:\n")
    for word, nums in greats.items():
        new_file.write(f"{word}: {nums}\n")

    new_file.write(f"\nThe word large appears {large_count} times\n\n")

    new_file.write("Large variants:\n")
    for word, nums in larges.items():
        new_file.write(f"{word}: {nums}\n")

    new_file.close()

    stdoutOrigin=sys.stdout 
    sys.stdout = open(name, "a")
    
    print(f"\n\nCommon context:\n")
    nltktext.common_contexts(["great", "large"])

    print(f"\n\nSimilar to great:\n")
    nltktext.similar("great")

    print(f"\n\nSimilar to large:\n")
    nltktext.similar("large")
    
    sys.stdout.close()
    sys.stdout=stdoutOrigin
