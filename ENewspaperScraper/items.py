from scrapy.item import Item, Field


class newsItem(Item):
    docID = Field()
    user = Field()
    userID = Field()
    type = Field()
    createDate = Field()
    shortFormDate = Field()
    title = Field()
    description = Field()
    message = Field()
    links_in_article = Field()
    picture = Field()
