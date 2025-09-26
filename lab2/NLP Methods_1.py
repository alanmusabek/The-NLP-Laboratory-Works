from PIL import Image
import pytesseract
import numpy as np
import os
import matplotlib.pyplot as plt
%matplotlib inline

os.listdir('C:\Program Files (x86)\Tesseract-OCR\tesseract.exe')
os.listdir()
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'tesseract.exe'
filename = 'text_seminar_en.png'
#filename = 'latin_text2.jpg'
img1 = np.array(Image.open(filename))
text = pytesseract.image_to_string(img1)

print(dir(pytesseract.pytesseract.tesseract_cmd))
plt.imshow(img1);

print(text)


import os
import speech_recognition as sr
recognizer = sr.Recognizer()

recognizer.energy_threshold = 500
clean_support_call = sr.AudioFile("Easy Kazakh Conversation - Dialogue.wav")
with clean_support_call as source:
    clean_support_call_audio = recognizer.record(source)

# Transcribe AudioData to text
text = recognizer.recognize_google(clean_support_call_audio,
                                   language="kk-KZ")
# text = recognizer.recognize_google(clean_support_call_audio,
#                                    language="ru-RU")
    
print(text)

# Importing the speech_recognition library
import speech_recognition as sr
recognizer = sr.Recognizer()
# Convert audio to AudioFile
noisy_support_call = sr.AudioFile("Easy Kazakh Conversation - Dialogue.wav")
# Record the audio from the noisy support call
with noisy_support_call as source:
# Adjust the recognizer energy threshold for ambient noise
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    noisy_support_call_audio = recognizer.record(noisy_support_call)

#Transcribe the speech from the noisy support call
text = recognizer.recognize_google(noisy_support_call_audio,
                                   language="kk-KZ")
print(text)

import selenium
from selenium import webdriver
#from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
#Chrome
options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('--headless')
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
options.add_argument('--disable-logging')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=options)
#driver = webdriver.Chrome()
print('Driver started successfully!')
os.getcwd()
driver.get("https://americanliterature.com/childrens-stories/the-three-little-pigs")
driver.get("https://zakup.sk.kz/#/ext")
driver.get("https://egov.kz/cms/ru")

page_text=driver.find_elements_by_tag_name("body")[0].text

from selenium.webdriver.common.by import By

page_text=driver.find_elements(By.TAG_NAME, "body")[0].text
page_text.split('\n')
page_text=page_text.split('\n')

sentences=[]
for item in page_text[9:-3]:
    sentences=sentences+item.split('. ')


punctuation='~!@#$%^&*()-_+=:;\'\",./?'
de_punct_sent=[]
for s in sentences:
    for p in punctuation:
        s=s.replace(p,' ')
    s=s.strip()
    de_punct_sent.append(s)

'a'.islower()
unbroken=[]
for i,s in enumerate(de_punct_sent):
    if s[0].islower():
        unbroken[-1]=unbroken[-1]+' '+s
    else:
        unbroken.append(s)
        
de_punct_sent[0].lower().split()
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
nltk.download('wordnet')

def get_pos_tag(t):
    try:
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV,
                    "P": wordnet.NOUN,#
                    "C": wordnet.NOUN,
                    "D": wordnet.NOUN,
                    "E": wordnet.NOUN,
                    "I": wordnet.NOUN,
                    "L": wordnet.NOUN,
                    "M": wordnet.NOUN,
                    "T": wordnet.NOUN,
                    "U": wordnet.NOUN,
                    "W": wordnet.NOUN,
                    "F": wordnet.NOUN,
                    "S": wordnet.NOUN}
        return tag_dict[t[0]]
    except:
        return wordnet.NOUN

os.listdir()
lemmatizer = WordNetLemmatizer()
print(type(lemmatizer))

nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()
lemmed_sents=[''.join([lemmatizer.lemmatize(tg[0], pos=get_pos_tag(tg[1])) for tg in nltk.pos_tag(s.split())]) for s in de_punct_sent]


print(de_punct_sent[:5])
print()
print(lemmed_sents[:5])

#SKLearn tfidfvectorizer
#vec without leemm and with
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(de_punct_sent)
print(vectorizer.get_feature_names())
print(X.shape)

vectorizer2 = TfidfVectorizer()
X2 = vectorizer2.fit_transform(lemmed_sents)
print(vectorizer2.get_feature_names())
print(X2.shape)


from sklearn.decomposition import PCA
def get_2d_3d_rep(X):
    #2D
    pca = PCA(n_components=2)
    X_2d=pca.fit_transform(X)
    
    #3D
    pca = PCA(n_components=3)
    X_3d=pca.fit_transform(X)
    
    return X_2d, X_3d

X_2d, X_3d=get_2d_3d_rep(X.toarray())
X2_2d, X2_3d=get_2d_3d_rep(X2.toarray())

import plotly.express as px
fig = px.scatter(x=X_2d[:,0], y=X_2d[:,1], hover_data=[de_punct_sent])
fig.show()

fig = px.scatter_3d(x=X_3d[:,0], y=X_3d[:,1], z=X_3d[:,2], hover_data=[de_punct_sent])
fig.show()

fig = px.scatter(x=X2_2d[:,0], y=X2_2d[:,1], hover_data=[de_punct_sent])
fig.show()
fig = px.scatter_3d(x=X2_3d[:,0], y=X2_3d[:,1], z=X2_3d[:,2], hover_data=[de_punct_sent])
fig.show()