
# coding: utf-8

# In[177]:


import random
import string as s


# In[178]:


def insert_except(l, pos, word):
    return l[::pos]+word+l[pos+1::]


# In[179]:


print(set_politics())


# In[180]:


text=''
with open("DushaPacana.txt", 'r') as f:
   for line in f.readlines():
       text += line


# In[181]:


def politicate(text,person):
    def set_politics():
        random.seed()
        return random.choice(['Путин', 'Трамп', 'Навальный',person])
    
    text.lower()
    stop_words = ['братан', 'брат', 'чувак', 'ты', 'Он' 'один', 'друг', 'девушка', 'земля', 'тот','сын', 'кто']
    for i in range (len(stop_words)):
        text=text.replace(stop_words[i], set_politics())
    return text


# In[182]:


text=politicate(text, 'Калугин')


# In[183]:


print(text)
with open('dump.txt', 'w+') as f:
    f.write(text)

