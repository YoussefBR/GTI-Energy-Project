import PyPDF2
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
# nltk.download("stopwords")
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

def get_freq(word_and_freq):
    return word_and_freq[1]

def findPOS(pos):
    two = pos[:2]
    if(two == "NN"):
        return "n"
    elif(two == "JJ"):
        return "a"
    elif(two == "RB"):
        return 'r'
    elif(two == "VB"):
        return 'v'
    else:
        return ''

pdf = open("2020 RECS_Methodology Report.pdf", 'rb')
pdfreader=PyPDF2.PdfReader(pdf)

numPages = len(pdfreader.pages)
text = []
for pageNum in range(numPages):
    page = pdfreader.pages[pageNum]
    text.append(page.extract_text())

text = " ".join(text)
with open("converted_pdf.txt", 'w') as f:
    f.write(text)

# get all the words in the text
words = word_tokenize(text)

# filter out the stop words
stop_words = set(stopwords.words("english"))
filtered = [ word for word in words if word.casefold() not in stop_words and word.isalpha() ]

# lemmatize the words and find the parts of speech (pos)
lemmatizer = WordNetLemmatizer()
filtered_with_pos = nltk.pos_tag(filtered)
lemmatized_with_pos = [(lemmatizer.lemmatize(word.casefold(), findPOS(pos)) if findPOS(pos) != "" else word, pos) for word, pos in filtered_with_pos]
# print(lemmatized_with_pos)

# chunk data
triples = []
length = len(lemmatized_with_pos) - 2
for i in range(length):
    word1, pos1 = lemmatized_with_pos[i]
    if pos1[0:2] == "NN":
        word2, pos2 = lemmatized_with_pos[i+1]
        if pos2[0:2] == "VB":
            word3, pos3 = lemmatized_with_pos[i+2]
            if pos3[0:2] == "NN":
                triples.append((word1, word2, word3))
# print(triples)

# find most common words
words, poss = zip(*lemmatized_with_pos)
word_freq = {}
for word in words:
    if word in word_freq:
        count = word_freq[word]
        word_freq.update({word: count + 1})
    else:
        word_freq.update({word: 1})

# right now household and housing are considered seperate words, in a more optimized system we'd probably find some way of throwing these two in the same category.
words_by_freq = [ (word, freq) for word, freq in word_freq.items() ]
words_by_freq = sorted(words_by_freq, key=get_freq, reverse=True)
# print(sorted_by_freq)

# grade each triple based on word frequency
graded_triples = []
for triple in triples:
    word1, word2, word3 = triple
    freq_score = 0
    freq_score += word_freq[word1]
    freq_score += word_freq[word2]
    freq_score += word_freq[word3]
    graded_triples.append((triple, freq_score))
# print(graded_triples)

triples_by_score = sorted(graded_triples, key=get_freq, reverse=True)
# print(triples_by_score)
filtered_triples_scored = []
for triple, score in triples_by_score:
    if "recs" not in triple:
        filtered_triples_scored.append((triple, score))
print(filtered_triples_scored)

gt_length = len(triples_by_score)
with open("triples.txt", "w") as trip_file:
    trip_file.write(str(gt_length) + "\n")
    for triple, score in triples_by_score:
        word1, word2, word3 = triple
        triple_str = str(word1) + " " + str(word2) + " " + str(word3)
        trip_file.write(triple_str + " " + str(score) + "\n")

