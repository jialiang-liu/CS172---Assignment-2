#!/usr/bin/env python3

import os
import math
import time
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import numpy as np
 
# Stop-words
stopword = stopwords.words('english')
# Initialize stemmer
stemmer = PorterStemmer()
# Initialize tokenizer
tokenizer = RegexpTokenizer(r'\w+')

# Using dictionary to store terms
# Using linked list to store the frequency
class Node(object):
	def __init__(self):
		self.docID = 0
		self.docFreq = 0
		self.next = None
class List(object):
	def __init__(self):
		self.head = None
		self.length = 0
	# Create a node for a document that has this term
	def append(self, Node):
		if not self.head:
			self.head = Node
		else:
			node = self.head
			while node.next:
				node = node.next
			node.next = Node
		self.length += 1
	# Update the frequency of a term for a specific document
	def update(self, ID):
		node = self.head
		while node is not None:
			if node.docID == ID:
				node.docFreq += 1
				break
			else:
				node = node.next
	# A function that can get the frequency for a term in a specific document
	def getFreq(self, ID):
		node = self.head
		while node is not None:
			if node.docID == ID:
				return node.docFreq
			else:
				node = node.next
		return 0
	# Check if a document has a node for a term
	def hasNode(self, ID):
		node = self.head
		if node is None:
			return False
		while node is not None:
			if node.docID == ID:
				return True
			else:
				node = node.next
		return False

dterm = {}
nterm = []
words = []
did = []
ndoc = 0

qterm = {}
nqterm = []

# Read the collection
# Record documents and their terms
def readdoc():
	global nterm, words, ndoc
	dno = 0
	path = os.path.dirname(__file__) + "/data/ap89_collection"
	with open(path, 'r') as f:
		flag = 0
		# Read the document
		for line in f:
			temp = line.strip()
			temp = line.split()
			if len(temp) != 0:
				if temp[0] == '<DOC>':
					dno += 1
					words.append([])
				elif temp[0] == '<DOCNO>':
					did.append(temp[1])
				elif temp[0] == '<TEXT>':
					flag = 1
				elif temp[0] == '</TEXT>':
					flag = 0
				if flag == 1 and temp[0] != '<TEXT>':
					line = tokenizer.tokenize(line)
					words[dno - 1] += line
	f.close()
	ndoc = len(words)
	for i in range(ndoc):
		l = 0
		doc = words[i]
		for word in doc:
			word = word.lower()
			word = stemmer.stem(word)
			# Check for stop-words
			if word not in stopword:
				l += 1
				# Check if the term exists
				if not dterm.__contains__(word):
					dterm[word] = List()
				# Check if a node of this term for this document has been created
				if not dterm[word].hasNode(i + 1):
					node = Node()
					node.docID = i + 1
					dterm[word].append(node)
				# Frequency += 1
				dterm[word].update(i + 1)
		# Record for the number of terms in this document
		nterm.append(l)

# Get the document index for a term
def getDocs(case, term):
	if case == 'd':
		if dterm.__contains__(term):
			return dterm[term].length
		else:
			return 0
	elif case == 'q':
		if qterm.__contains__(term):
			return qterm[term].length
		else:
			return 0
# Get term frequency with term and document number
def getPost(case, term, ID):
	if case == 'd':
		if dterm.__contains__(term):
			return dterm[term].getFreq(ID)
		else:
			return 0
	elif case == 'q':
		if qterm.__contains__(term):
			return qterm[term].getFreq(ID)
		else:
			return 0
# Compute the TF-IDF
def TFIDF(case):
	global iterm, tfidf, sqd, sqq
	if case == 'd':
		iterm = dterm.copy()
		nt = nterm.copy()
		n = ndoc
	elif case == 'q':
		iterm = qterm.copy()
		nt = nqterm.copy()
		n = len(nqterm)
	tfidf = np.zeros([1, n])
	count = 0
	for term in iterm:
		iterm[term] = count
		count += 1
		tf = []
		for i in range(n):
			tf.append(getPost(case, term, i + 1) / nt[i])
		idf = math.log(n / (getDocs(case, term))) + 1
		tfidf = np.r_[tfidf, np.array([[a * idf for a in tf]])]
	tfidf = np.delete(tfidf, 0, axis = 0)
	if case == 'd':
		sqd = np.power(np.sum((tfidf * tfidf).T, axis = 1), 0.5)
	elif case == 'q':
		sqq = np.power(np.sum((tfidf * tfidf).T, axis = 1), 0.5)
# Compute the cosine similarity
def cossim(vecs, q):
	global sqd, qsqq
	rank = (vecs @ q).T / np.array([sqd]) / qsqq
	return rank

# Processing the rank
def procrank(rank):
	global ndoc, qno, did, rf
	index = np.array(range(1, ndoc + 1))
	rank = ((np.r_[[index], rank]).T).tolist()
	rank = sorted(rank, key = lambda x: (-x[1], x[0]))
	i = 0
	res = []
	while i < ndoc:
		if rank[i][1] == 0 or i == 100:
			break
		res.append([qno, rank[i][0], i + 1, rank[i][1]])
		i += 1
	res = sorted(res, key = lambda x: (x[1]))
	for r in res:
		r[1] = did[int(r[1] - 1)]
		opstr = str(r[0]) + " Q0 " + str(r[1]) + ' ' + str(r[2]) + ' ' + str(r[3]) + " Exp\n"
		rf.write(opstr)

# Processing the query
def query(query):
	global iterm, tfidf, ndoc, qno
	query = tokenizer.tokenize(query)
	qno = query[0]
	query.pop(0)
	vec = np.zeros([1, ndoc])
	for term in query:
		if term not in stopword:
			term = term.lower()
			term = stemmer.stem(term)
			if iterm.__contains__(term):
				vec = np.r_[vec, [tfidf[iterm[term]]]]
			else:
				vec = np.r_[vec, np.zeros([1, len(tfidf[0])])]
	vec = (np.delete(vec, 0, axis = 0)).T
	q = np.ones([vec.shape[1], 1])
	rank = cossim(vec, q)
	procrank(rank)

# Read queries
def readquery():
	path = os.path.dirname(__file__) + "/data/query_list.txt"
	i = 1
	with open(path, 'r') as f:
		for line in f:
			line = tokenizer.tokenize(line)
			qno = line[0]
			line.pop(0)
			l = len(line)
			for term in line:
				if term not in stopword:
					term = term.lower()
					term = stemmer.stem(term)
					if not qterm.__contains__(term):
						qterm[term] = List()
					if not qterm[term].hasNode(i):
						node = Node()
						node.docID = i
						qterm[term].append(node)
					qterm[term].update(i)
				else:
					l -= 1
			nqterm.append(l)
			i += 1
	f.close()

# Initialize
def init():
	global rf
	start_2 = time.time()
	readquery()
	TFIDF('q')
	end_2 = time.time()
	start_1 = time.time()
	readdoc()
	TFIDF('d')
	end_1 = time.time()
	print("Document processing was finished in", end_1 - start_1, "second(s).")
	print("Query processing was finished in", end_2 - start_2, "second(s).")
	rf = open(os.path.dirname(__file__) + "/data/results_file.txt", "w")
	rf.truncate()

def takequery():
	global qsqq
	path = os.path.dirname(__file__) + "/data/query_list.txt"
	i = 0
	with open(path, 'r') as f:
		for line in f:
			qsqq = sqq[i]
			query(line)
			i += 1
	f.close()
	rf.close()
	print("Results for your list of queries has been writen into \"results_file.txt\".")

if __name__ == '__main__':
	init()
	takequery()






