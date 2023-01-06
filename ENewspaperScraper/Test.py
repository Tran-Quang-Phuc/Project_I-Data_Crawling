import gensim
import nltk
from nltk import word_tokenize, sent_tokenize
import numpy as np

nltk.download('punkt')


def checkSimilar(mess1, mess2):
    mess1_docs = []
    for line in sent_tokenize(mess1):
        mess1_docs.append(line)

    gen_docs = []
    for line in mess1_docs:
        gen_doc = [word.lower() for word in word_tokenize(line)]
        gen_docs.append(gen_doc)

    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)

    sims = gensim.similarities.Similarity('workdir/', tf_idf[corpus],
                                          num_features=len(dictionary))

    mess2_docs = []
    avg_sims = []
    for line in sent_tokenize(mess2):
        mess2_docs.append(line)

    for line in mess2_docs:
        query_doc = [w.lower() for w in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_doc)  # update an existing dictionary and create bag of words
        query_doc_tf_idf = tf_idf[query_doc_bow]
        sum_of_sims = np.sum(sims[query_doc_tf_idf], dtype=np.cfloat)
        avg = sum_of_sims / len(mess1_docs)
        print(f'avg: {avg}')
        avg_sims.append(avg)

    total_avg = np.sum(avg_sims, dtype=np.cfloat)
    percentage_of_similarity = np.round(total_avg * 100)
    if percentage_of_similarity >= 100:
        return True
    return False


if __name__ == "__main__":
    a = 'abcd ef. hai ba bon'
    b = 'abcd ef. hai ba bon'
    if checkSimilar(a, b):
        print("Message is similar")
    else:
        print("Message is different")
