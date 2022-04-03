import nltk
nltk.download('stopwords')
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from scipy.sparse.linalg import svds

stop_words = nltk.corpus.stopwords.words('english')

def normalize_document(doc):
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
    doc = doc.lower()
    doc = doc.strip()
    # tokenize document
    tokens = nltk.word_tokenize(doc)
    # filter stopwords out of document
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc

def low_rank_svd(matrix, singular_count):
    u, s, vt = svds(matrix, k=singular_count)
    return u, s, vt

def extractive_summariser(DOCUMENT):
    nltk.download('punkt')

    DOCUMENT = re.sub(r'\n|\r', ' ', DOCUMENT)
    DOCUMENT = re.sub(r' +', ' ', DOCUMENT)
    DOCUMENT = DOCUMENT.strip()

    sentences = nltk.sent_tokenize(DOCUMENT)

    normalize_corpus = np.vectorize(normalize_document)

    norm_sentences = normalize_corpus(sentences)

    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
    dt_matrix = tv.fit_transform(norm_sentences)
    dt_matrix = dt_matrix.toarray()

    vocab = tv.get_feature_names_out()
    td_matrix = dt_matrix.T

    pd.DataFrame(np.round(td_matrix, 2), index=vocab)

    l = len(sentences)

    if(l <= 2):
        return ("\n".join(np.array(sentences)))

    num_sentences = 0
    
    # if(l < 10):
    #     num_sentences = 2
    # elif(l < 50):
    #     num_sentences = 5
    # elif(l < 500):
    #     num_sentences = 10
    # elif(l < 1000):
    #     num_sentences = 15
    # else:
    #     num_sentences = 20

    if(l < 10):
        num_sentences = 3
    elif(l < 100):
        num_sentences = int(l/3)
    elif(l < 500):
        num_sentences = int(l/8)
    elif(l < 1000):
        num_sentences = int(l/14)
    else:
        num_sentences = 72

    u, s, vt = low_rank_svd(td_matrix)  

    term_topic_mat, singular_values, topic_document_mat = u, s, vt

    # remove singular values below threshold                                         
    sv_threshold = 0.5
    min_sigma_value = max(singular_values) * sv_threshold
    singular_values[singular_values < min_sigma_value] = 0

    salience_scores = np.sqrt(np.dot(np.square(singular_values), 
                                    np.square(topic_document_mat)))

    top_sentence_indices = (-salience_scores).argsort()[:num_sentences]
    top_sentence_indices.sort()
    
    return ("\n".join(np.array(sentences)[top_sentence_indices]))