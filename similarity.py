import mongo 
N = 5 # max number of similar users to find

# yelpDB is passed from yelp.py and is a Mongo instance so no need 
# to reconnect to mongo here
def PredictStars(yelpDB, userId, userIds, businessId):
    #userId: user for prediction, userIds: other users who have reviewed a given restaurant
    stars = 0.0
    # get all feature arrays of users in userIds array and compare
    # to userId. Use top N similar users to predict userIds star
    # rating of that restaurant and return (stars should be type int)
    user = yelpDB.GetUserById('EaVmK7PPnV5TAEvB_tg-sw')
    #get feature vectors for all users 
    usersFeatVctr = {}
    featList = []
    simDict = {}

    predUserFeatVctr = yelpDB.GetUserById(userid1)
    rowAvg = float(sum(predUserFeatVctr['feature'].values())) / len(predUserFeatVctr['feature'].values())
    #normalize feat values (sub mean)
    for key1, value1 in predUserFeatVctr['feature']: 
        predUserFeatVctr['feature'][key1] = value1 - rowAvg

    for userid1 in userIds: 
        tempFeatVctr = yelpDB.GetUserById(userid1)
        rowAvg = float(sum(tempFeatVctr['feature'].values())) / len(tempFeatVctr['feature'].values())
        #normalize feat values (sub mean)
        for key1, value1 in tempFeatVctr['feature'].items(): 
            tempFeatVctr['feature'][key1] = value1 - rowAvg
        usersFeatVctr.append(tempFeatVctr)
        #for feat in tempFeatVctr['feature'].keys():
            #if feat not in featList: 
                #featList.append(feat)
    
    #computer cos similarity for each user
    userMagn = float(sum(x**2 for x in predUserFeatVctr['feature'].values())**.5
    for tempUserVctr in usersFeatVctr:
        simSum = 0.0
        for key1, value1 in tempUserVctr['feature'].items():
            if key1 in predUserFeatVctr['feature']: 
                simSum += predUserFeatVctr['feature'][key1] * float(value1)
        tempMagn = float(sum(x**2 for x in tempUserVctr['feature'].values())**.5
        simDict[tempUserVctr['_id']] = float(simSum) / (userMagn * tempMagn)

    #sort cos sim
    sortSimDict = sorted(simDict.items(), key = lambda x:x[1], reverse = True)

    #pred using equal weight of top N 
    simStars = []
    for i1 in xrange(N):
        simUserId = sortSimDict[i1][0]
        simReview = yelpDB.GetReviewByUserAndBusinessId(simUserId, businessId)
        simStars.append(simReview['stars'])
    stars = float(sum(simStars))/len(simStars)
    return stars

def test(): 
    yelpDB = mongo.Mongo()
    user = yelpDB.GetUserById('EaVmK7PPnV5TAEvB_tg-sw')
    print user['feature'] 
    print ''
    print user
    print ''
    print user['feature']['Buffets']
    #userId: user for prediction, userIds: other users who have reviewed a given restaurant
    starPred = 0.0
    # get all feature arrays of users in userIds array and compare
    # to userId. Use top N similar users to predict userIds star
    # rating of that restaurant and return (stars should be type int)

    return starPred
def GetStarPrediction(yelpDB, userId, businessId):
    userIds = []
    reviews = yelpDB.GetReviewsByBusinessId(businessId)
    for review in reviews:
        #user ids which have reviewed same business
        #?? need to handle duplicate user ids?
        userIds.append(review['user_id'])
    stars = PredictStars(yelpDB, userId, userIds, businessId)
    return stars

def GetStars(userId, businessId):
    yelpDB = mongo.Mongo()
    #review to be predicted on
    review = yelpDB.GetReviewByUserAndBusinessId(userId, businessId)
    if review != None:
        print review
        return review['stars']
    else:
        return GetStarPrediction(yelpDB, userId, businessId)
#GetStars('EaVmK7PPnV5TAEvB_tg-sw', 'rdAdANPNOcvUtoFgcaY9KA')
test()
