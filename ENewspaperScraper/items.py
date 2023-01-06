from scrapy.item import Item, Field


class newsItem(Item):
    docID = Field()
    user = Field()
    userID = Field()
    # docType = Field()
    type = Field()
    # statusType = Field()
    createDate = Field()
    shortFormDate = Field()
    title = Field()
    message = Field()

    links_in_article = Field()
    picture = Field()
    numLikes = Field()
    numComments = Field()
    numShares = Field()
