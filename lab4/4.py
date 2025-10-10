from pymorphy3 import MorphAnalyzer
import re
import gensim
import logging
import nltk.data
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from gensim.models import word2vec
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from pymorphy2 import MorphAnalyzer
from gensim.test.utils import datapath
nltk.download('punkt')

from nltk import FreqDist
from tqdm import tqdm_notebook as tqdm
from sklearn.manifold import TSNE

from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook

from sklearn.decomposition import TruncatedSVD
import fasttext

from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm_notebook as tqdm
import re

model_path = 'ruwikiruscorpora-nobigrams_upos_skipgram_300_5_2018.vec.gz'

model_ru = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)

words = ['день_NOUN', 'ночь_NOUN', 'человек_NOUN', 'семантика_NOUN', 'биткоин_NOUN']

for word in words:
    # есть ли слово в модели?
    if word in model_ru:
        print(word)
        # смотрим на вектор слова (его размерность 300, смотрим на первые 10 чисел)
        print(model_ru[word][:10])
        # выдаем 10 ближайших соседей слова:
        for word, sim in model_ru.most_similar(positive=[word], topn=10):
            # слово + коэффициент косинусной близости
            print(word, ': ', sim)
        print('\n')
    else:
        # Увы!
        print('Увы, слова "%s" нет в модели!' % word)

print(model_ru.similarity('nvidia_PROPN', 'видеокарта_NOUN'))
print(model_ru.most_similar(positive=['татарин_NOUN', 'казахстан_NOUN'], negative=['казах_NOUN'])[0][0])
model_ru.doesnt_match('бешбармак_NOUN плов_NOUN манты_NOUN'.split())
model_ru.most_similar(positive=['ключ_NOUN'], topn=10)
model_ru.most_similar(positive=['дверь_NOUN'], topn=10)
model_ru.most_similar(positive=['италия_NOUN'], negative=['пицца_NOUN'])
model_ru.most_similar(positive=['идти_VERB'], topn=10)

# EXERCISE
import random
from pymorphy2 import MorphAnalyzer

# assume the model is already loaded
# e.g. model_ru = gensim.models.KeyedVectors.load('ruscorpora.model')

analyser = MorphAnalyzer()

def change_random_noun(sentence, model):
    """
    Replaces a random noun in the given sentence with its most similar word 
    according to the given Word2Vec model.
    """
    words = sentence.split()
    nouns = []

    # collect indices of nouns
    for i, w in enumerate(words):
        parsed = analyser.parse(w)[0]
        if parsed.tag.POS == 'NOUN':
            nouns.append((i, parsed.normal_form))  # store index and lemma form

    # if there are no nouns, just return sentence
    if not nouns:
        return sentence

    # choose random noun
    i, noun = random.choice(nouns)

    # try to find a close word using the model
    try:
        top1 = model.most_similar(positive=[noun], topn=1)[0][0]
    except KeyError:
        # if word not in vocab, skip replacement
        return sentence

    # replace noun with the similar one
    words[i] = top1

    # join back
    return ' '.join(words)

sent = 'маленький человек увидел обезьяну в Италии'
new_sent = change_random_noun(sent, model_ru)
print(new_sent)
