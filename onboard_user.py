import mongo
import config

def ClientOnboard(yelpDB, userId):
    reviews = yelpDB.GetReviewsByUserId(userId)
    feature = {}
    for review in reviews:
        businessId = review['business_id']
        business = yelpDB.GetBusinessById(businessId)
        categories = business['categories']
        for i in range(0, len(categories)):
            c = categories[i]
            if config.categories.count(c) != 0: 
                if c in feature:
                    feature[c] = (feature[c][0] + int(review['stars']), feature[c][1] + 1) 
                else:
                    feature[c] = (int(review['stars']), 1)
    for key in feature:
        feature[key] = feature[key][0] / feature[key][1]
    return yelpDB.SetUserFeatureSet(userId, feature)

def OnboardAll():
    yelpDB = mongo.Mongo()
    users = yelpDB.GetAllUsers()
    for user in users:
        ClientOnboard(yelpDB, user['_id'])
        print user['_id']
    return

def OnboardSingleUser(userId):
    yelpDB = mongo.Mongo()
    ClientOnboard(yelpDB, userId)
    return

OnboardAll()