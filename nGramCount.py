#!/usr/bin/env python
# coding=UTF-8
#
# Output the 50 most-used words from a text file, using NLTK FreqDist()
# (The text file must be in UTF-8 encoding.)
#
# Usage:
#
#   python nGramCount.py input.txt
#


import sys
import re
import codecs
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams

"""
By Henry Weckermann
Create FrequencyDistance of input file. Counts Mono/Bi/Tri - Grams
Outputs the 100 most used mono/bi/tri - grams
"""


def createSummaryTextFile():
    # read Excel file into DataFrame
    df = pd.read_excel('cve_compact.xlsx')
    text_list_old = []

    # make list out of summary row
    for index, row in df.iterrows():
        text_list_old.append(row.summary)

    # remove all digits
    text_list = []
    for sentence in text_list_old:
        text_list.append(''.join([i for i in sentence if not i.isdigit()]))


    with open('summary.txt', 'w') as f:
        for item in text_list:
            f.write("%s\n" % item)

def main():
    # NLTK's default English stopwords
    default_stopwords = set(nltk.corpus.stopwords.words('english'))

    # We're adding some on our own - could be done inline like this...
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    stopwords_file = './stopwords.txt'
    custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

    all_stopwords = default_stopwords | custom_stopwords

    input_file = sys.argv[1]

    fp = codecs.open(input_file, 'r', 'utf-8')

    words = nltk.word_tokenize(fp.read())

    #removing digits and floats
    words = [re.sub(r'[0-9\.]+', '', word) for word in words]
    words = [re.sub(r'(\w){1}\-(\w){1}\b', '', word) for word in words]

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 2]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]


    #creating bigrams
    bgs = nltk.bigrams(words)

    #ngrams
    tgs = ngrams(words, 3)

    # Calculate frequency distributions
    fdist = nltk.FreqDist(words)
    fdist_bgs = nltk.FreqDist(bgs)
    fdist_tgs = nltk.FreqDist(tgs)

    # Output top 50 words
    print("Monograms")
    for word, frequency in fdist.most_common(50):
        print(u'{} : {}'.format(word, frequency))


    print("\n\nBigrams")
    for word, frequency in fdist_bgs.most_common(50):
        print(u'{} : {}'.format(word, frequency))

    print("\n\nnGrams")
    for word, frequency in fdist_tgs.most_common(50):
        print(u'{} : {}'.format(word, frequency))


if __name__ == "__main__":
    main()

