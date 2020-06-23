import sys
import os
import numpy as np
import random


def count_list(the_dict, alpha=0):
    wordlist = []
    for key in the_dict.keys():
        wordlist.append([key, the_dict[key]])
    summ = 0
    for word in wordlist:
        summ += word[1] + alpha
        word[1] = summ
    return wordlist


def choose_random_word(wordlist):
    value = np.random.uniform(0, wordlist[-1][1])
    left = 0
    right = len(wordlist)
    while right - left > 1:
        middle = int((right + left) / 2)
        if value > wordlist[middle][1]:
            left = middle
        else:
            right = middle
    return wordlist[left][0]


def create_token_list(directory):
    files = os.listdir(directory)
    my_list = []
    for filename in files:
        if str.endswith(filename, ".txt"):
            with open(directory + filename) as fileobject:
                for line in fileobject:
                    line = line.lower()
                    line = "".join(c for c in line if c not
                                   in ('(', ')', ':', '"', ',', ';', '\n','[',']') and not c.isdigit())
                                   line = line.replace('.', ' . $').replace('!', ' ! $').replace('?', ' ? $').replace('\xa0', '')
                                   my_list.extend(line.split(' '))
                print("File {} is done".format(filename))
    my_list.append('$')
    print(len(my_list))
    return my_list


def create_symbol_list(directory):
    files = os.listdir(directory)
    my_list = []
    for filename in files:
        if str.endswith(filename, '.txt'):
            with open(directory + filename) as fileobject:
                for line in fileobject:
                    my_list.extend(list(line))
    print(len(my_list))
    return my_list


def create_dict_and_start(token_list, n_gram=3):
    start_set = set()
    big_dict = {}
    prev = tuple(token_list[0: n_gram - 1])
    succeeder = token_list[1: n_gram]
    for i in range(n_gram, len(token_list)):
        if big_dict.get(prev, None) is None:
            big_dict[prev] = {tuple(succeeder): 1}
        else:
            big_dict[prev][tuple(succeeder)] = big_dict[prev].get(tuple(succeeder), 0) + 1
        if prev[0] == '$':
            start_set.add(prev)
        prev = tuple(succeeder)
        succeeder.append(token_list[i])
        succeeder.pop(0)
    for key in big_dict.keys():
        big_dict[key] = count_list(big_dict[key], alpha=0)
    return (big_dict, start_set)


def generate_text(list_dict, start_set, size=4000):
    current = random.choice(list(start_set))
    wordlist = list(current)
    for i in range(size):
        word = choose_random_word(list_dict[current])
        wordlist.append(word[-1])
        current = word
    string = ' '.join(wordlist)
    sentences = string.split(sep='$ ')
    n_sentences = []
    for sent in sentences:
        n_sentences.append(sent.capitalize())
    string = ''.join(n_sentences)
    string = string.replace(' .', '.').replace(' !', '!').replace(' ?', '?').replace('$', '')
    print(string)


token_list = create_symbol_list("./Python_Project_hse/BOOKS/")
dict_start = create_dict_and_start(token_list, n_gram=10)
the_dict = dict_start[0]
start_set = dict_start[1]
generate_text(the_dict, start_set, size=4000)
