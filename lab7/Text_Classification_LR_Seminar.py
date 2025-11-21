# regular expression operations
import re
# string operation
import string
# shuffle the list
from random import shuffle

# linear algebra
import numpy as np
# data processing
import pandas as pd

# NLP library
import nltk
# module for stop words that come with NLTK
from nltk.corpus import stopwords
# module for stemming
from nltk.stem import PorterStemmer
# module for tokenizing strings
from nltk.tokenize import TweetTokenizer

# scikit model selection
from sklearn.model_selection import train_test_split

# smart progressor meter
from tqdm import tqdm
import seaborn as sns
import json

from google.colab import drive
drive.mount('/content/drive')

import os
os.listdir('drive/MyDrive/Zhalgas Zhiyenbekov/KBTU/NLP/Seminars/Text_Classification/nfact_data.json')


import pandas as pd

# Path to the CSV file
file_path = 'drive/MyDrive/Zhalgas Zhiyenbekov/KBTU/NLP/Seminars/Text_Classification/annotations_summaries.csv'

# Read the CSV file into a pandas DataFrame
try:
    data = pd.read_csv(file_path)
    # Display the first few rows as a table
    print("Data loaded successfully!")
    from IPython.display import display  # Ensure we can display as a table in Jupyter/Kaggle
    display(data.head())  # Displays the first 5 rows neatly as a table
except FileNotFoundError:
    print(f"The file at {file_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

import pandas as pd
import json

# Assuming 'data' is the DataFrame from the previous step
# data = pd.read_csv('your_file_path.csv')

# Let's classify the data into factual and non-factual
factual_data = data[data['is_factual'] == 'yes']['summary'].tolist()
non_factual_data = data[data['is_factual'] == 'no']['summary'].tolist()

# Define the paths for saving the separate JSON files
factual_output_path = 'drive/MyDrive/Zhalgas Zhiyenbekov/KBTU/NLP/Seminars/Text_Classification/fact_data.json'
non_factual_output_path = 'drive/MyDrive/Zhalgas Zhiyenbekov/KBTU/NLP/Seminars/Text_Classification/nfact_data.json'

# Write the factual data to a JSON file
with open(factual_output_path, 'w') as factual_json_file:
    json.dump(factual_data, factual_json_file, indent=4)

# Write the non-factual data to a JSON file
with open(non_factual_output_path, 'w') as non_factual_json_file:
    json.dump(non_factual_data, non_factual_json_file, indent=4)

print(f"Factual data saved to {factual_output_path}")
print(f"Non-factual data saved to {non_factual_output_path}")


# Path to your JSON files
factual_data_path = 'drive/MyDrive/Zhalgas Zhiyenbekov/KBTU/NLP/Seminars/Text_Classification/fact_data.json'
non_factual_data_path = 'drive/MyDrive/Zhalgas Zhiyenbekov/KBTU/NLP/Seminars/Text_Classification/nfact_data.json'

# Read the factual and non-factual data from JSON
with open(factual_data_path, 'r') as f:
    factual_data_path = json.load(f)

with open(non_factual_data_path, 'r') as f:
    non_factual_data_path = json.load(f)

# Check the length of the data
print(f"Factual data count: {len(factual_data_path)}")
print(f"Non-factual data count: {len(non_factual_data_path)}")


# Display the first 5 factual and nonfactual samples
print("\nFactual Samples:")
for i, sentence in enumerate(factual_data_path[:5], 1):
    print(f"{i}: {sentence}")

print("\nNon Factual Samples:")
for i, sentence in enumerate(non_factual_data_path[:5], 1):
    print(f"{i}: {sentence}")



# Let's have a look at the data
no_of_facts = 3
print("Example of Factual Sentences:")
print('\n'.join(factual_data_path[:no_of_facts]))
print("\nExample of Non factual sentences:")
print('\n'.join(non_factual_data_path[:no_of_facts]))



import nltk
nltk.download('stopwords')

#TODO
# helper class for doing preprocessing
class Sentence_Preprocess():

    def __init__(self):
        # instantiate tokenizer class
        self.tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True)
        # get the english stopwords
        self.stopwords_en = stopwords.words('english')
        # get the english punctuation
        self.punctuation_en = string.punctuation
        # Instantiate stemmer object
        self.stemmer = PorterStemmer()

    def __remove_unwanted_characters__(self, sentence):

        # remove resentence style text "RT"

        ## return removed text
        return sentence

    def __tokenize_sentence__(self, sentence):
        # tokenize sentences
        return

    def __remove_stopwords__(self, sentence_tokens):
        # remove stopwords
        sentences_clean = []


        return sentences_clean

    def __text_stemming__(self,sentence_tokens):
        # store the stemmed word
        sentences_stem = []

        return sentences_stem

    def preprocess(self, sentences):
        sentences_processed = []
        for _, sentence in tqdm(enumerate(sentences)):
            # apply removing unwated characters and remove style of resentence, URL
            sentence = self.__remove_unwanted_characters__(sentence)
            # apply nltk tokenizer
            sentence_tokens = self.__tokenize_sentence__(sentence)
            # apply stop words removal
            sentence_clean = self.__remove_stopwords__(sentence_tokens)
            # apply stemmer
            sentence_stems = self.__text_stemming__(sentence_clean)
            sentences_processed.extend([sentence_stems])
        return sentences_processed
    
