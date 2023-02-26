from datetime import datetime

import pymongo
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


all_messages = []


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


class CheckTimePipeline:
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
        adapter['message'] = message.replace('\n', '').replace('\xa0', '')

        return item


class SimilarityPipeline:
    def __init__(self):
        self.articles = set()

    def _is_similar(self, article1, article2):
        # Convert the articles to lowercase to make the comparison case-insensitive
        article1 = article1.lower()
        article2 = article2.lower()

        # Create a TfidfVectorizer object and fit it to the articles
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([article1, article2])

        # Calculate the cosine similarity between the vectors
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

        # Return True if the similarity is greater than a threshold value, False otherwise
        return similarity > 0.8

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        message = adapter.get('message')
        if len(message) < 100:
            raise DropItem("This article is to short")
        # Check if the current article is similar to any of the previously seen articles
        for article in self.articles:
            if self._is_similar(message, article):
                # If the article is similar, drop it and return None
                raise DropItem("This message has already scraped")

        # If the article is not similar to any of the previously seen articles, add it to the set
        self.articles.add(message)

        # Return the item to continue processing it
        return item


class StoreToMongoPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        db = self.conn['OnlineNews']
        self.collection = db['Vietnamnet']

    def process_item(self, item, spider):
        self.collection.insert_one(ItemAdapter(item).asdict())
        return item
