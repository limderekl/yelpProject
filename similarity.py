import mongo 
import time

# def TestPredictStars(yelpDB, user, userIds, businessId, N=5):
#     featureVectors = {}
#     businessReviews = {}
#     start = time.time()
#     for userId in userIds:
#         u = yelpDB.GetUserById(userId)
#         br = yelpDB.GetReviewByUserAndBusinessId(userId, businessId)
#         featureVectors[u['_id']] = u['feature']
#         businessReviews[u['_id']] = br['stars']
#     print time.time() - start
#     return (0, 0, 0)
# yelpDB is passed from yelp.py and is a Mongo instance so no need 
# to reconnect to mongo here
def PredictStars(yelpDB, userId, userIds, businessId, N=5, user=None):
    #userId: user for prediction, userIds: other users who have reviewed a given restaurant
    # get all feature arrays of users in userIds array and compare
    # to userId. Use top N similar users to predict userIds star
    # rating of that restaurant and return (stars should be type int)
    if user == None:
        user = yelpDB.GetUserById(userId)
    #get feature vectors for all users 
    usersFeatVctr = []
    featList = []
    simDict = {}

    predUserFeatVctr = user
    rowAvg = float(sum(extractStars(predUserFeatVctr['feature'].values()))) / len(extractStars(predUserFeatVctr['feature'].values()))
    #normalize feat values (sub mean), remove tup notation
    for key1, value1 in predUserFeatVctr['feature'].items(): 
        predUserFeatVctr['feature'][key1] = value1[0] - rowAvg

    for userid1 in userIds: 
        tempFeatVctr = yelpDB.GetUserById(userid1)
        tempFeatVctr['feature']['average_stars'] = (tempFeatVctr['average_stars'], 1)
        rowAvg = float(sum(extractStars(tempFeatVctr['feature'].values()))) / len(extractStars(tempFeatVctr['feature'].values()))
        #normalize feat values (sub mean), remove tup notation
        for key1, value1 in tempFeatVctr['feature'].items(): 
            tempFeatVctr['feature'][key1] = value1[0] - rowAvg
        usersFeatVctr.append(tempFeatVctr)
    
    #computer cos similarity for each user
    userMagn = float(sum(x**2 for x in predUserFeatVctr['feature'].values())**.5)
    for tempUserVctr in usersFeatVctr:
        simSum = 0.0
        for key1, value1 in tempUserVctr['feature'].items():
            if key1 in predUserFeatVctr['feature']: 
                simSum += predUserFeatVctr['feature'][key1] * float(value1)
        tempMagn = float(sum(x**2 for x in tempUserVctr['feature'].values())**.5)
        if userMagn * tempMagn == 0.0:
            simDict[tempUserVctr['_id']] = 0.0
        else:
            simDict[tempUserVctr['_id']] = float(simSum) / (userMagn * tempMagn)

    #sort cos sim, tuple of (user_id, similarity)
    sortSimList = sorted(simDict.items(), key = lambda x:x[1], reverse = True)
    normSortSimList = []
    for tup in sortSimList: 
        # print tup
        normSortSimList.append((tup[0], float(tup[1])/2 + .5))

    simStars = []
    if N > len(sortSimList): 
        N = len(sortSimList) 
    
    #most similar
    mostStar = yelpDB.GetReviewByUserAndBusinessId(sortSimList[0][0], businessId)['stars']

    #pred using equal weight of top N 
    weightStarSum = 0.0
    weightSimSum = 0.0
    for i1 in xrange(N):
        simUserId = normSortSimList[i1][0]
        simReview = yelpDB.GetReviewByUserAndBusinessId(simUserId, businessId)
        simStars.append(simReview['stars'])
        weightStarSum += simReview['stars'] * normSortSimList[i1][1]
        weightSimSum += abs(normSortSimList[i1][1])
        # print 'sim: ' + str(normSortSimList[i1][1])
    unweightStar = float(sum(simStars))/len(simStars)

    weightStar = weightStarSum/ weightSimSum
    # print "userIds: " + str(userIds)
    # print "cos sim: "+str(simDict)
    # print "sim stars: "+str(simStars)
    #weighted avg
    # print 'most: ' + str(mostStar) + ' unweighted: '+str(unweightStar)+' weighted: '+str(weightStar)
    # print 'star sum: ' + str(weightStarSum) + 'sim sum: ' + str(weightSimSum)
    return mostStar, unweightStar, weightStar

# def test(): 
#     yelpDB = mongo.Mongo()
#     user = yelpDB.GetUserById('EaVmK7PPnV5TAEvB_tg-sw')
#     print user['feature'] 
#     print user
#     starPred = 0.0
#     return starPred

#turn a list of tuples: (star, count) to a list of stars
def extractStars(tupleList): 
    tempList = []
    for tup1 in tupleList: 
        #print tup1
        tempList.append(tup1[0])
    return tempList
def GetStarPrediction(yelpDB, userId, businessId):
    userIds = []
    reviews = yelpDB.GetReviewsByBusinessId(businessId)
    for review in reviews:
        #user ids which have reviewed same business
        #?? need to handle duplicate user ids?
        userIds.append(review['user_id'])
    stars = PredictStars(yelpDB, userId, userIds, businessId, 3)
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
# GetStars('EaVmK7PPnV5TAEvB_tg-sw', 'rdAdANPNOcvUtoFgcaY9KA')
#GetStars('SEJWhA6MRIavK4b3pGxwTg', 'rdAdANPNOcvUtoFgcaY9KA')
#test()
