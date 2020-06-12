import collections
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# read Excel file into DataFrame
df = pd.read_excel('cve_compact.xlsx')
text_list_old = []

# make list out of summary row
for index, row in df.iterrows():
    text_list_old.append(row.summary)

# remove all digits
text_list = []
for t in text_list_old:
    text_list.append(''.join([i for i in t if not i.isdigit()]))

#Stopwords
#with open('stopwords.txt', 'r') as file:
#    stopwords = file.read().splitlines()


# magic
cv = CountVectorizer(text_list, ngram_range=(1,3), max_df=0.6)
count_vector = cv.fit_transform(text_list)

myWordsDict = cv.vocabulary_
stop = cv.stop_words_

print(stop)

x = myWordsDict
y = {k: v for k, v in sorted(x.items(), reverse=True, key=lambda item: item[1])}
print(list(y.items())[:20])

# Make new DataFrame
df = pd.DataFrame(list(myWordsDict.items()), columns = ['Word', 'Count'])


# sort it
df.sort_values(['Count'], inplace=True, ascending=False)

#output excel file
df.to_excel('wc2.xlsx')
