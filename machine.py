
import nltk
from nltk.corpus import treebank

# 首次使用需要下载
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('treebank')

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
# Tokenize
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)

# Identify named entities
entities = nltk.chunk.ne_chunk(tagged)

# Display a parse tree
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()