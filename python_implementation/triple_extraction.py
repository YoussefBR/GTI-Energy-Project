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

word_connections = {}

def get_freq(word_and_freq):
    return word_and_freq[1]

def findPOS(pos):
    """defines the general pos category based on the first two chars of the pos

    Args:
        pos (str): the part of speech of a word

    Returns:
        str: the part of speech category for a word
    """    
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
    
def extractTriples(lemmatized_with_pos: list) -> list:
    """From lemmatized words in document go through and pull out NN-VB-NN triples

    Args:
        lemmatized_with_pos (list): All words in the original document after they've been lemmatized and the stop words have been filtered out

    Returns:
        list: return a list of triples that fit the NN-VB-NN format
    """    
    triples = []
    length = len(lemmatized_with_pos) - 2
    for i in range(length):
        word1, pos1 = lemmatized_with_pos[i]
        word2, pos2 = lemmatized_with_pos[i+1]
        word3, pos3 = lemmatized_with_pos[i+2]
        if pos1[0:2] == "NN" and pos2[0:2] == "VB" and pos3[0:2] == "NN":
            triples.append((word1, word2, word3))
    return triples

def getWordFreq(words: list) -> dict:
    """Using words in document, count up all duplicates and put into a dictionary with the format {word: count}

    Args:
        words (list): A list of every word in the original document, lemmatized with the stopwords filtered out

    Returns:
        dict: A dictionary of every unique word in the document with the frequency in which it appears
    """    
    word_freq = {}
    for word in words:
        if word in word_freq:
            count = word_freq[word]
            word_freq.update({word: count + 1})
        else:
            word_freq.update({word: 1})
    return word_freq

def gradeTriples(triples: list, word_freq: dict) -> list:
    """Grade triples by adding up the frequency of all three words in the triple

    Args:
        triples (list): The list of triples in the document
        word_freq (dict): A dictionary of each unique word and it's frequency in the document

    Returns:
        list: A list of tuples where the first value is the triple and the second value is the score
    """    
    graded_triples = []
    for triple in triples:
        word1, word2, word3 = triple
        freq_score = 0
        freq_score += word_freq[word1]
        freq_score += word_freq[word2]
        freq_score += word_freq[word3]
        graded_triples.append((triple, freq_score))
    graded_triples = sorted(graded_triples, key=get_freq, reverse=True)
    return graded_triples

def filterScoredTriples(triples_by_score: list) -> list:
    """builds the dictionary of connections to a unique word from the scored triples list and returns a filtered version of the input list

    Args:
        triples_by_score (list): a list of tuples that contain a triple and its score

    Returns:
        list: a filtered version of the input list that doesn't contain connections to itself or connections involving recs
    """    
    filtered_triples_scored = []
    for triple, score in triples_by_score:
        word1, word2, word3 = triple
        # recs is the name of the company so we don't want to include it and connections to self are implied so should be removed
        if "recs" not in triple and word1 != word3:
            if word1 in word_connections:
                word_connections[word1].append(word3)
            else:
                connections = []
                connections.append(word3)
                word_connections[word1] = connections
            if word3 in word_connections:
                word_connections[word3].append(word1)
            else:
                connections = []
                connections.append(word1)
                word_connections[word3] = connections
            score = gradingRules(triple, score)
            filtered_triples_scored.append((triple, score))
    return filtered_triples_scored

def gradingRules(triple: tuple, freq_score: int) -> int:
    """takes in the triple and it's original score and modifies the score based on the grading rules

    Args:
        triple (tuple): the triple, follows the format NN-VB-NN
        freq_score (int): the triple's score

    Returns:
        int: the adjusted score based on the grading rules
    """    
    word1, word2, word3 = triple
    # bad connections
    # data should never be a verb, due to the frequency of this word and the limitations of the pdf converter it would occasionally be fraudulently put in as a verb
    if(word2 == "data" and freq_score > 0):
        freq_score *= -1
    # if(word2 == "ing" and freq_score > 0):
    #     freq_score *= -1
    # This is in place of a dictionary check, generally any word under 3 characters ends up being a false read of something in the pdf
    if((len(word1) < 3 or len(word3) < 3) and freq_score > 0):
        freq_score *= -1
    if freq_score < 0:
        return int(freq_score)
    # good connections
    elec_included = word1 == "electricity" or word3 == "electricity"
    if(word2 == "use" or elec_included):
        freq_score *= 2
    # data analysis is usually a big part of reports, and due to the sheer amount of time needed to discuss results in data it tends to skew the graph in favor it so we need to make data analysis less impactful
    if(word1 == "data" or word3 == "data"):
        freq_score /= 2
    if(word2 == "sample"):
        freq_score /= 2
    if(word1 == "estimate" or word3 == "estimate"):
        freq_score /= 2
    return int(freq_score)
    

def main():
    """converts the pdf to text and then performs natural langauage processing on the text to extract information in the form of triples and a dictionary of connections.
    """    
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
    triples = extractTriples(lemmatized_with_pos)
    # print(triples)

    # find most common words
    words, poss = zip(*lemmatized_with_pos)
    word_freq = {}
    word_freq = getWordFreq(words)

    # right now household and housing are considered seperate words, in a more optimized system we'd probably find some way of throwing these two in the same category.
    words_by_freq = [ (word, freq) for word, freq in word_freq.items() ]
    words_by_freq = sorted(words_by_freq, key=get_freq, reverse=True)
    # print(words_by_freq)

    # grade each triple based on word frequency then sort
    scored_triples = []
    scored_triples = gradeTriples(triples, word_freq)
    # print(triples_by_score)

    filtered_triples_scored = []
    filtered_triples_scored = filterScoredTriples(scored_triples)
    # print(filtered_triples_scored)

    gt_length = len(filtered_triples_scored)
    with open("triples.txt", "w") as trip_file:
        trip_file.write(str(gt_length) + "\n")
        for triple, score in filtered_triples_scored:
            word1, word2, word3 = triple
            triple_str = str(word1) + " " + str(word2) + " " + str(word3)
            trip_file.write(triple_str + " " + str(score) + "\n")
        

def getTriples() -> list:
    """returns the triples extracted by main and stored into the triples.txt file

    Returns:
        list: a list of tuples containing triples and their scores
    """    
    triples = []
    with open("triples.txt") as triples_file:
        line = triples_file.readline()
        line = triples_file.readline()
        while line != "":
            word1, word2, word3, score = line.split(' ')
            triple = (word1, word2, word3)
            triples.append((triple, int(score[:-1])))
            line = triples_file.readline()
    return triples

def getWordConnections() -> dict:
    """returns the dictionary of connections of each unique word which is set up in the main function

    Returns:
        dict: a dictionary that follows the format {unique word: list of connected words}
    """    
    return word_connections
