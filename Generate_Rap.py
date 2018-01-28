
# coding: utf-8

# In[6]:


import urllib.request as r
#import bs4
import re
import string
from collections import Counter, OrderedDict
import random
import argparse
import sys
import unittest


# In[7]:


class Utils(object):

    @staticmethod
    def split_symbol(text, symbol, drop_symbol=False):
        if drop_symbol:
            return text.split(symbol)

        parts = text.split(symbol)
        result = []
        for part in parts:
            result += [part, symbol]
        return result[:-1]

    @staticmethod
    def split_for_tokens(text):
        splited = []
        number = ''
        word = ''
        other = ''
        for i in range(len(text)):
            if text[i].isdigit():
                if len(other) > 0:
                    splited += [other]
                    other = ''
                if len(word) > 0:
                    splited += [word]
                    word = ''
                number += text[i]
            elif text[i].isalpha():
                if len(other) > 0:
                    splited += [other]
                    other = ''
                if len(number) > 0:
                    splited += [number]
                    number = ''
                word += text[i]
            else:
                if len(word) > 0:
                    splited += [word]
                    word = ''
                if len(number) > 0:
                    splited += [number]
                    number = ''
                other += text[i]
        if len(word) > 0:
            splited += [word]
        if len(number) > 0:
            splited += [number]
        if len(other) > 0:
            splited += [other]
        return splited

    @staticmethod
    def parts_split_symbol(parts, symbol, drop_symbol=False):
        new_parts = []
        for part in parts:
            new_parts += Utils.split_symbol(part, symbol, drop_symbol)
        return [s for s in filter(lambda x: len(x) != 0, new_parts)]

    @staticmethod
    def split(text, delimiters, delimiters_to_drop=[]):
        """

        :param text: type(str)
        :param delimiters: to split text
        :param delimiters_to_drop: to split text and not include to result
        :return: splitted text with delimiters and w/o delimiters_to_drop
        """
        parts = [text]

        for symbol in delimiters_to_drop:
            parts = Utils.parts_split_symbol(parts, symbol, drop_symbol=True)

        for symbol in delimiters:
            parts = Utils.parts_split_symbol(parts, symbol, drop_symbol=False)

        new_parts = []
        for part in parts:
            new_parts += Utils.split_for_tokens(part)
        return new_parts

    @staticmethod
    def tokenize(text, depth=1, drop_whitespace=False):
        """

        :param text: type(str)
        :param depth: length of words chain
        :param drop_whitespace: if true, drops whitespaces in final list
        :return: list of tokens
        """
        delimiters = []
        delimiters_to_drop = []
        if drop_whitespace:
            delimiters = []
            delimiters_to_drop = string.whitespace + string.punctuation
        else:
            delimiters = string.punctuation + string.whitespace

        splited = Utils.split(text, delimiters, delimiters_to_drop)
        return [tuple(splited[i:i + depth]) for i in range(0, len(splited) - depth + 1)]

    @staticmethod
    def get_chains(text, depth=1):
        splited_text = text.split('\n')
        chains = dict()
        for line in splited_text:
            chains_with_future = Utils.tokenize(line, depth + 1, drop_whitespace=True)
            for item in chains_with_future:
                if item[:depth] not in chains:
                    chains[item[:depth]] = []
                chains[item[:depth]] += item[depth:]
        return chains

    @staticmethod
    def count_probabilities(chains):
        chains_with_probabilities = OrderedDict()
        for key, values in chains.items():
            counts = Counter(values)
            total = len(values)
            probabilities = OrderedDict()
            for v in values:
                probabilities[v] = counts[v] / total
            chains_with_probabilities[key] = OrderedDict(sorted(list(probabilities.items()),
                                                                key=lambda x: x[0])
                                                         )
        return OrderedDict(sorted(chains_with_probabilities.items(), key=lambda x: x[0]))

    @staticmethod
    def unique(l):
        """
        :param l:
        :return: unique elements of list
        """
        return list(set(l))


# In[8]:


class TokenizeTask(object):
    def __init__(self, text):
        self.text = text
        self.tokens = Utils.tokenize(self.text)

    def __str__(self):
        return '\n'.join([s[0] for s in self.tokens])


# In[9]:


class CalculateProbabilitiesTask(object):
    def __init__(self, text, depth=1):
        self.chains = [Utils.get_chains(text, depth=i) for i in range(0, depth + 1)]
        self.probabilities = [Utils.count_probabilities(chain) for chain in self.chains]

    def __str__(self):
        pr = []
        for d in self.probabilities:
            for key, values in d.items():
                pr += [(key, values)]
        pr = sorted(pr, key=lambda x: x[0])
        ans = []
        for pr_per_level in pr:
            history, values = pr_per_level[0], pr_per_level[1]
            ans.append(' '.join(history))
            for next_word, p in values.items():
                ans.append('  {}: {:.2f}'.format(next_word, p))
        return '\n'.join(ans)


# In[10]:


class TextGenerator(object):
    def __init__(self, depth=1, size=20):
        self.depth = depth
        self.size = size
        self.probabilities = []

    def fit(self, text):
        prob_task = CalculateProbabilitiesTask(text, self.depth)
        self.probabilities = prob_task.probabilities

    def generate(self):
        generated_words = []
        new_word = self.__choice(self.probabilities[0][()])
        generated_words.append(new_word)

        for i in range(1, self.size):
            slice_size = min(self.depth - 1, i)
            prev_chain = tuple(generated_words[-slice_size:])
            while prev_chain not in self.probabilities[slice_size]:
                slice_size -= 1
                prev_chain = tuple(generated_words[-slice_size:])
                if (slice_size < 0):
                    slice_size = 0
                    prev_chain = ()
                    break
            new_word = self.__choice(self.probabilities[slice_size][prev_chain])
            generated_words.append(new_word)
        generated_words[0] = generated_words[0].capitalize()
        return ' '.join(generated_words)

    def __choice(self, future):
        total_prob = 0
        for next_word, p in future.items():
            total_prob += p
        result = random.uniform(0, total_prob)
        lower_bound = 0
        for next_word, p in future.items():
            lower_bound += p
            if lower_bound > result:
                return next_word


# In[163]:


import random
def main(a,b='Сощщников',c='Дима',d='Даня',e='Саша'):
    result = ""
    text = ""
    stop_world='@'
    with open("corpus.txt", 'r') as f:
        for line in f.readlines():
            text += line
    tg = TextGenerator(5, 200)
    print(type(tg))
    tg.fit(text)
    rap_gad = tg.generate()
    l = rap_gad.split(' ')
    print(type(l))
    t = ''
    f = 0
    k = 0
    l[3]=a
    for i in range(len(l)):
        if i%10==2:
            l[i]=random.choice([a,b,c,d,e])
            
    for i in range(0,len(l)-4):
        if (l[i] == l[i+1]) or (l[i+1] == l[i+7]):
            print("Overfiting on ", l[i])
            stop_word = l[i]
            f = 1
            break
#    while i != len(l)-k:
 #       if (l[i] == stop_word):
  #          l = l[::i-1]+l[i+1::]
   #         k +=1
    #    i += 1
    for i in range(0, len(l)):
        print(l[i], end=' ')
        if (i + 1) % 6 == 0:
            print()
    return l[::25]


# In[164]:


l = main('Конференция')


# In[121]:




