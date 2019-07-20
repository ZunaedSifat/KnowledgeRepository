import nltk
from summa import keywords

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from documents import wordart


def lemmatize(words):
    lem = WordNetLemmatizer()
    lemmatized_words = dict()

    words = dict(words)

    for k in words:
        lemmatized = lem.lemmatize(k)
        lemmatized = lem.lemmatize(lemmatized, 'v')
        if lemmatized not in lemmatized_words:
            lemmatized_words[lemmatized] = words.get(k)
        else:
            lemmatized_words[lemmatized] = lemmatized_words.get(lemmatized) + words.get(k)

    lemmatized_words = sorted(lemmatized_words.items(), key=lambda x: x[1], reverse=True)

    return lemmatized_words


def generate_summa_keywords(text, outputfile):
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words("english"))

    file2 = open(outputfile, 'w', encoding='UTF-8')

    ps = PorterStemmer()
    _keywords = list()
    valid_keywords = dict()

    try:
        _keywords = dict(keywords.keywords(text, scores=True))
        # print(_keywords)
        for key, val in _keywords.items():
            if len(key) > 2 and key not in stop_words:
                valid_keywords[key] = val
    except UnicodeDecodeError:
        print('Error')

    # stemmed_words = []
    #
    # for w in _keywords:
    #     stemmed = ps.stem(w)
    #     if stemmed not in stemmed_words:
    #         stemmed_words.append(stemmed)

    l = lemmatize(valid_keywords)
    # print('Lemmatized Keywords:', l)
    # print('Total', l.__len__())
    print('summa',l)

    s = str()
    for k, v in l:
        s += k + '\n'
    file2.write(s)

    return l


# def generate_summa_keywords_without_lemmatize(inputfile, outputfile):
#     nltk.download('stopwords')
#     nltk.download('wordnet')
#     stop_words = set(stopwords.words("english"))
#
#     file1 = open(inputfile, "r", encoding='UTF-8')
#     file2 = open(outputfile, 'w', encoding='UTF-8')
#
#     ps = PorterStemmer()
#     _keywords = list()
#     try:
#         text = file1.read()
#         _keywords = str(keywords.keywords(text)).split('\n')
#         for k, v in enumerate(_keywords):
#             if v in stop_words:
#                 _keywords.remove(k)
#                 # print(v)
#     except UnicodeDecodeError:
#         print('Error')
#
#     # stemmed_words = []
#     #
#     # for w in _keywords:
#     #     stemmed = ps.stem(w)
#     #     if stemmed not in stemmed_words:
#     #         stemmed_words.append(stemmed)
#
#     s = str()
#     for v in _keywords:
#         s += v + '\n'
#     file2.write(s)

#
# l = generate_summa_keywords(open('t.txt', 'r', encoding='UTF-8').read(), 'k.txt')
#
# wordart.generate_word_art('k.txt', 'a')
