import os
import pandas as pd
import re
from collections import Counter
import numpy as np

# 1. Load data
data = pd.read_table('lab5\sample_messages.txt', names=['status', 'message'])
data.head()

# 2. Basic statistics
all_messages = data['message'].count()
spam_messages = data[data['status'] == 'spam']['status'].count()
ham_messages = data[data['status'] == 'ham']['status'].count()
p_spam = spam_messages / all_messages
p_ham = ham_messages / all_messages

print(f"всего сообщений: {all_messages}")
print(f"всего spam сообщений: {spam_messages}")
print(f"всего ham сообщений: {ham_messages}")
print(f"вероятность того, что сообщение будет spam: {p_spam*100:.2f}%")
print(f"вероятность того, что сообщение будет ham: {p_ham*100:.2f}%")


# 3. Clean data (remove punctuation, lowercase)
clean_data = data.copy()
#Начало вашего кода
clean_data['message'] = clean_data['message'].apply(
    lambda x: re.sub(r'[^a-zA-Z\s]', '', x.lower())
)
#Конец вашего кода

for i in range(len(clean_data)):
    print(f"{i}\t{clean_data['message'][i]}")


# 4. Replace multiple spaces with single space
def delete_whitespaces(x):
    #Начало вашего кода
    return re.sub(r'\s+', ' ', x).strip()
    #Конец вашего кода

clean_data["message"] = clean_data["message"].apply(delete_whitespaces)

for i in range(len(clean_data)):
    print(f"{i}\t{clean_data['message'][i]}")


# 5. Build vocab
def get_vocab(data, condition=None):
    #Начало вашего кода
    if condition == "ham":
        messages = data[data['status'] == 'ham']['message']
    elif condition == "spam":
        messages = data[data['status'] == 'spam']['message']
    else:
        messages = data['message']

    words = []
    for msg in messages:
        words.extend(msg.split())

    vocab = dict(Counter(words))
    return vocab
    #Конец вашего кода


ham_vocab = get_vocab(clean_data, condition="ham")
spam_vocab = get_vocab(clean_data, condition="spam")
vocab = get_vocab(clean_data)

print("HAM vocab sample:", dict(list(ham_vocab.items())[:10]), "\n")
print("SPAM vocab sample:", dict(list(spam_vocab.items())[:10]), "\n")
print("GLOBAL vocab sample:", dict(list(vocab.items())[:10]), "\n")


# 6. Calculate conditional probabilities
def calc_probs(sam_vocab, vocab, message, alpha=1):
    #Начало вашего кода
    words = re.findall(r'\b[a-z]+\b', message.lower())
    total_words_in_class = sum(sam_vocab.values())
    vocab_size = len(vocab)

    prob = 1.0
    for word in words:
        word_count = sam_vocab.get(word, 0)
        prob *= (word_count + alpha) / (total_words_in_class + alpha * vocab_size)
    return prob
    #Конец вашего кода


message = "WINNER WINNER WINNER WINNER WINNER"

p_ham_given_message = p_ham * calc_probs(ham_vocab, vocab, message, alpha=1)
p_spam_given_message = p_spam * calc_probs(spam_vocab, vocab, message, alpha=1)

print("p(ham|message):", p_ham_given_message)
print("p(spam|message):", p_spam_given_message)

condition = "ham"
if p_spam_given_message > p_ham_given_message:
    condition = "spam"
print("Predicted:", condition)


# 7. Build a reusable filter function
def filter_spam(message, p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1):
    #Начало вашего кода
    p_ham_given_message = p_ham * calc_probs(ham_vocab, vocab, message, alpha)
    p_spam_given_message = p_spam * calc_probs(spam_vocab, vocab, message, alpha)

    if p_spam_given_message > p_ham_given_message:
        return "spam"
    else:
        return "ham"
    #Конец вашего кода


print(filter_spam("Hello, how are you?", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
print(filter_spam("Congrats! You won 1000000", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
print(filter_spam("Winner! Winner! Winner!", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
print(filter_spam("Urgent! You got free ticket!", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
