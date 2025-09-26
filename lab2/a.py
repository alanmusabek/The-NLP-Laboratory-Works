import pandas as pd
import numpy as np
from tqdm import tqdm_notebook
ds = pd.read_csv('lenta-ru-news.csv')
ds.head()
ds.shape
ds.isnull().sum()
ds.dropna(inplace= True)
ds.shape
ds_sample = ds.sample(n=1000)
ds_sample.to_csv('ds_sample.csv',index = False)
new_data = pd.read_csv('ds_sample.csv')
new_data.dropna(inplace = True)
new_data.shape
from collections import Counter
Counter(ds_sample.tags)

cntr = Counter(ds.tags)
{k: v for k, v in sorted(cntr.items(), key=lambda item: item[1], reverse=True)}

texts = ds_sample.text.values
#remove punctuation

def rem_punc(t):
# define punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'''

# remove punctuation from the string
    for c in punctuations:
        t=t.replace(c,' ')

# display the unpunctuated string
    return t.replace('\n',' ')

no_punc_text = [rem_punc(t) for t in tqdm_notebook(texts)]
#lowercase
lc_text = [t.lower() for t in tqdm_notebook(no_punc_text)]
lc_text[0]

#stopword removal
import nltk
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
sw = stopwords.words('russian')

text = "Я очень люблю изучать обработку естественного языка"

# tokenize into words
words = nltk.word_tokenize(text, language="russian")

# filter out stopwords
filtered = [w for w in words if w.lower() not in sw]

print("Original:", words)
print("Without stopwords:", filtered)

ds['title'][0]
words = nltk.word_tokenize(ds['title'][0], language="russian")

# Clean the data set from stop words
# your code
clean_texts = []

for t in tqdm_notebook(lc_text):
    words = nltk.word_tokenize(t, language="russian")   # токенизация
    filtered = [w for w in words if w not in sw]        # убираем стоп-слова
    clean_texts.append(filtered)

# посмотрим первый результат
print(clean_texts[0][:50])