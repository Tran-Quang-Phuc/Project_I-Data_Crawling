from datetime import datetime

import gensim as gensim
import numpy as np
import pymongo
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize


class CreateDateToDatetime:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        dateString = adapter.get('createDate')  # 2023-01-03T15:11:00.000000
        if dateString:
            format = '%Y-%m-%dT%H:%M:%S.%f%z'
            Datetime = datetime.strptime(dateString, format)
            adapter['createDate'] = Datetime
        else:
            raise DropItem("Can not get the create date")

        return item


class ShortFormDateToDatetime:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        dateString = adapter.get('shortFormDate')
        format = '%Y-%m-%d'
        Datetime = datetime.strptime(dateString, format)
        adapter['shortFormDate'] = Datetime

        return item


class TimeCheckPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        today = datetime.now()
        if adapter.get('shortFormDate').date() != today.date():
            raise DropItem("This article is not published today")

        return item


class ConcatenateMessagePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        message = ''
        for para in adapter.get('message'):
            message = message + para
        adapter['message'] = message.replace('\n', '')

        return item


class SimilarMessageCheck:
    def __init__(self):
        self.news_message = []
        nltk.download('punkt')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        cur_message = adapter.get('message')

        if len(cur_message) < 20:
            raise DropItem("Message is too short!")
        elif len(self.news_message) != 0:
            for message in self.news_message:
                if self.checkSimilar(cur_message, message):
                    raise DropItem("Drop similar news!")
                else:
                    self.news_message.append(cur_message)
        else:
            self.news_message.append(cur_message)

        print("Add a new article")

        return item

    def checkSimilar(self, mess1, mess2):
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

        sims = gensim.similarities.Similarity('workdir/', tf_idf[corpus], num_features=len(dictionary))

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
            avg_sims.append(avg)

        total_avg = np.sum(avg_sims, dtype=np.cfloat)
        percentage_of_similarity = np.round(float(total_avg) * 100) // 3
        if percentage_of_similarity >= 100:
            return True
        return False


class StoreToMongoPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        db = self.conn['OnlineNews']
        self.collection = db['Vietnamnet']

    def process_item(self, item, spider):
        self.collection.insert_one(ItemAdapter(item).asdict())
        return item
