  # -*- coding: utf-8 -*-
import gensim
from gensim import corpora, models, similarities
import pymorphy2
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import sys
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
morph = pymorphy2.MorphAnalyzer()

########################### Пути по умолчанию ###########################

cursed = 'C:\Anaconda/lenin.txt' ### Путь к обрабатываемому файлу 
cured = 'C:\Anaconda/test.txt' ### Путь к обработанному
path_stoplist = 'C:\Anaconda/stoplist.txt' ### Путь к файлу "стоп-слов"

#########################################################################

def normalize(token):
	try: 
		gram_info = morph.parse(token)
		return gram_info[0].normal_form
	except:
		return token


args = [arg for arg in sys.argv]
if len(args) != 1:
	s = sys.path[0]
	cursed = s + '/' + args[1]
	cured = s + '/' + args[2]
	path_stoplist =  s + '/' + args[3]

fid = open(path_stoplist,'r')
stoplist = [line.strip().decode('utf-8') for line in fid.readlines()]
fid.close()


fid = open(cursed,'r')
lines = fid.readlines()
fid.close()


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
			
	


dictionary = corpora.Dictionary(sentences)
corpus = [dictionary.doc2bow(sentence) for sentence in sentences]

stopwords = [stopword for stopword in stoplist if stopword in dictionary.token2id]

stopsetnences = []

index = similarities.SparseMatrixSimilarity(corpus, num_features=len(dictionary))
for sw in stopwords:
	new_vec = dictionary.doc2bow(sw.split())
	sims = index[new_vec]
	for s in range(len(sims)):
		if sims[s] > 0:
			if s not in stopsetnences:
				stopsetnences.append(s)

stopsetnences = sorted(stopsetnences)


sentences = []
tokenized_lines = map(tokenizer.tokenize, [line.decode('utf-8').strip() for line in lines])
for tokenized_line in tokenized_lines: 
	sentence = []
	for token in tokenized_line:
		if not token == '.':
 			sentence.append(token)
		else:
			sentence.append(token)
			sentences.append(sentence)
			sentence = []

fid = open(cured,'w')
for sen in range(len(sentences)):
	if sen not in stopsetnences:
		for word in sentences[sen]:
			if not word in string.punctuation:
				fid.write(" " + word.encode('utf-8'))
			else:
				fid.write(word.encode('utf-8'))
fid.close() 

