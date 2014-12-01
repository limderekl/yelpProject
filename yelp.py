import mongo
import config

def GetStarPrediction(yelpDB, userId, businessId):
    userIds = []
    reviews = yelpDB.GetReviewsByBusinessId(businessId)
    for review in reviews:
        userIds.append(review['user_id'])
    stars = similarity.PredictStars(yelpDB, userId, userIds, businessId)
    return stars

def GetStars(userId, businessId):
    yelpDB = mongo.Mongo()
    review = yelpDB.GetReviewByUserAndBusinessId(userId, businessId)
    if review != None:
        return review['stars']
    else:
        return GetStarPrediction(yelpDB, userId, businessId)

GetStars('EaVmK7PPnV5TAEvB_tg-sw', 'rdAdANPNOcvUtoFgcaY9KA')
