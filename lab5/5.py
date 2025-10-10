# 1. At the lecture you studied the naive Bayesian algorithm, now it's time to do practice. The most common use of the naive Bayesov algorithm is the classification of messages as spam or not.

# You have a file `` "sample_messages" `` `with spam & non-spam (HAM) messages, download it to Pandas.Dataframe` `Data```` '.

import os
os.listdir()

#Начало вашего кода

import pandas as pd
data = pd.read_table('sample_messages.txt', names = ['status', 'message'])

#Конец вашего кода

data.head()

#2. Perform a research analysis of the data `` Data```` ', and answer the following questions:

#* How many messages are there in the data? Assign the result of the variable `` all_Messages````.

#*How much is ** spam ** messages in the data? Assign the result of a variable `` spam messages````.

#*How much is ** HAM ** messages in the data? Assign the result of the variable `` HAM_MESSAGES``` '.

#*What is the probability that the message will be ** spam **? Assign the result of the variable `` p_spam``` '.

#*What is the likelihood that the message will be ** HAM **? Assign the result of the variable `` P_HAM``` '.
#Начало вашего кода

all_messages = data['message'].count()
spam_messages = data[data['status'] == 'spam']['status'].count()
ham_messages = data[data['status'] == 'ham']['status'].count()
p_spam = spam_messages / all_messages
p_ham = ham_messages / all_messages
#Конец вашего кода

print(f"всего сообщений: {all_messages}")
print(f"всего spam сообщений: {spam_messages}")
print(f"всего ham сообщений: {ham_messages}")
print(f"вероятность того, что сообщение будет spam: {p_spam*100:.2f}%")
print(f"вероятность того, что сообщение будет ham: {p_ham*100:.2f}%")

#3. You may encounter the problem that messages have a different format and contain punctuation marks (which we can ignore). You must clean the data in this task.

clean_data = data.copy()
#Начало вашего кода

#Конец вашего кода
for i in range(len(clean_data)):
    print(f"{i}\t{clean_data['message'][i]}")

#4. As can be seen from the above text, there are many consistent spaces between words, please implement the function `` delete_whitespaces () ``, which will replace all consistent gaps with one gap.

def delete_whitespaces(x):
    #Начало вашего кода

    #Конец вашего кода

clean_data["message"] = clean_data["message"].apply(delete_whitespaces)

for i in range(len(clean_data)):
    print(f"{i}\t{clean_data['message'][i]}")


#5. Implement the function `` get_vocab (Data, Condition = None) `` `, which accepts one positional argument` `DATA``` (PANDAS.DATAFRAME) and one nominal argument` `` control````. This function should return the dictionary of words and their quantities in `` `Data`` 'relative to the argument` `` condition````.

#Example:

#* When `` `Condition =" HAM "` ``, the function should return the dictionary of words and their number only in `` `spam`` 'messages.

#* When `` `Condition =" Spam "` ``, the function should return the dictionary of words and their number only in `` HAM`` 'messages.

#* When `` `Condition = None``` ', the function should return the dictionary of words and their number only in all messages.

def get_vocab(data, condition=None):
    #Начало вашего кода

    #Конец вашего кода

ham_vocab = get_vocab(clean_data,condition="ham")
spam_vocab = get_vocab(clean_data,condition="spam")
vocab = get_vocab(clean_data)

print(ham_vocab,end="\n\n")
print(spam_vocab,end="\n\n")
print(vocab,end="\n\n")

# 6. Now the time has come to calculate the conditional probabilities for each word $ p (spam | (w_1, w_2, ..., w_n)) $ and $ p (Ham | (w_1, w_2, ..., w_n) $. Implement the function `` Calc_Prob (*arg) `` `, the first input argument is either` `spam_vocab````, or` `HAM_VOCAB`````, the second input should be` `` vOCAB``` `` `Message``` - a new message from the user.

import re

def calc_probs(sam_vocab, vocab, message, alpha=1):
    #Начало вашего кода
    # YOUR CODE
    
    #Конец вашего кода

message = "WINNER WINNER WINNER WINNER WINNER"

p_ham_given_message = p_ham*calc_probs(ham_vocab, vocab, message, alpha=1)
p_spam_given_message = p_spam*calc_probs(spam_vocab, vocab, message, alpha=1)

print(p_ham_given_message)
print(p_spam_given_message)

condition = "ham"

if p_spam_given_message > p_ham_given_message:
    condition = "spam"
print(condition)


#7. Implement the function `` Filter_spam (Message, P_Spam, Spam_vocab, P_HAM, HAM_VOCAB, VOCAB, Alpha = 1) `` `, which will check if the incoming message is` `spam``` 'or` `HAM``````.
 
def filter_spam(message, p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1):
    #Начало вашего кода

    #Конец вашего кода


print(filter_spam("Hello, how are you?", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
print(filter_spam("Congrats! You won 1000000", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
print(filter_spam("Winner! Winner! Winner!", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))
print(filter_spam("Urgent! You gor free ticket!", p_spam, spam_vocab, p_ham, ham_vocab, vocab, alpha=1))