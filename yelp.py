import mongo
import config
import similarity
import time

def GetStarPrediction(yelpDB, userId, businessId, N, user=None, userIds=None):
    if userIds == None:
        userIds = []
        reviews = yelpDB.GetReviewsByBusinessId(businessId)
        for review in reviews:
            #user ids which have reviewed same business
            #?? need to handle duplicate user ids?
            if userId != review['user_id']:
                userIds.append(review['user_id'])
    stars = similarity.PredictStars(yelpDB, userId, userIds, businessId, N=N, user=user)
    return stars

def GetStars(userId, businessId):
    yelpDB = mongo.Mongo()
    #review to be predicted on
    review = yelpDB.GetReviewByUserAndBusinessId(userId, businessId)
    if review != None:
        return review['stars']
    else:
        return GetStarPrediction(yelpDB, userId, businessId)

# GetStars('EaVmK7PPnV5TAEvB_tg-sw', 'rdAdANPNOcvUtoFgcaY9KA')
