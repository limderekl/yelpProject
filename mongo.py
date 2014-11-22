from pymongo import MongoClient
import credentials

class Mongo():
    def __init__(self):
        user = credentials.mongo['user']
        secret = credentials.mongo['secret']
        url = credentials.mongo['url']
        self.db = MongoClient('mongodb://' + user + ':' + secret + '@' + url).playground
        self.userCol = self.db.user
        self.businessCol = self.db.business
        self.reviewCol = self.db.review

    def GetUserById(self, userId):
        user = self.userCol.find_one({'_id': userId}) 
        return user

    def GetBusinessById(self, businessId):
        business = self.businessCol.find_one({'_id': businessId})
        return business

    def GetReviewById(self, reviewId):
        review = self.reviewCol.find_one({'_id': reviewId})
        return review

    def GetAllUsers(self):
        return self.userCol.find()

    def GetAllBusinesses(self):
        return self.businessCol.find()

    def GetAllReviews(self):
        return self.reviewCol.find()

    def GetReviewsByUserId(self, userId):
        reviews = self.reviewCol.find({'user_id': userId})
        return reviews

    def GetReviewsByBusinessId(self, businessId):
        reviews = self.reviewCol.find({'business_id': businessId})
        return reviews

    def GetReviewByUserAndBusinessId(self, userId, businessId):
        return self.reviewCol.find({'user_id': userId, 'business_id': businessId})

    def SetUserFeatureSet(self, userId, feature):
        return self.userCol.update({'_id': userId}, {'$set': {'feature': feature}})


