# -*- coding: utf-8 -*-
import sys
import gensim
from gensim import corpora, models, similarities
import pymorphy2
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
morph = pymorphy2.MorphAnalyzer()

def normalize(token):
      try:
              gram_info = morph.parse(token)
              return gram_info[0].normal_form
      except:
              return token

dirty = 'C:\Anaconda\lenin.txt'
clean = 'C:\Anaconda\clean.txt'
path_stoplist = 'C:\Anaconda\stoplist.txt'

args = [arg for arg in sys.argv]
if len(args) != 1:
        s = sys.path[0]
        dirty = s + '/' + args[1]
        clean = s + '/' + args[2]
        path_stoplist = s + '/' +args[3]

fid = open(path_stoplist,'r')
stoplist = [line.strip().decode('utf-8') for line in fid.readlines()]
fid.close()

fid = open(dirty,'r')
lines = fid.readlines()
fid.close()

original_sentences = []
tokenized_lines = map(tokenizer.tokenize, [line.decode('utf-8').strip() for line in lines])
for tokenized_line in tokenized_lines:
      original_sentence = []
      for token in tokenized_line:
              original_sentence.append(token)
              if token == '.':
                      original_sentences.append(original_sentence)
                      original_sentence = []

sentences = []
tokenized_lines = map(tokenizer.tokenize, [line.decode('utf-8').strip() for line in lines])
for tokenized_line in tokenized_lines:
      sentence = []
      for token in tokenized_line:
              if not token == '.':
                      if not token in string.punctuation:
                              sentence.append(normalize(token))
              else:
                      sentences.append(sentence)
                      sentence = []

result = open(clean, 'w')


dictionary = corpora.Dictionary(sentences)
corpus = [dictionary.doc2bow(sentence) for sentence in sentences]

stopwords = [stopword for stopword in stoplist if stopword in dictionary.token2id]

bad_sentences = []

index = similarities.SparseMatrixSimilarity(corpus, num_features=len(dictionary))
for sw in stopwords:
      new_vec = dictionary.doc2bow(sw.split())
      sims = index[new_vec]
      for s in range(len(sims)):
              if sims[s] > 0:
                      bad_sentences.append(s)

for i in range(len(original_sentences)):
      if not i in bad_sentences:
              for word in original_sentences[i]:
                      if not word in string.punctuation:
                              result.write(' ' + word.encode('utf-8'))
                      else:
                              result.write(word.encode('utf-8'))

result.close()

