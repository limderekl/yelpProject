# Testing framework for similarity-based star prediction

# Outline
# Given a user and a restaurant he has reviewed, remove the contribution
# of said restaurant from that users feature vector. This can be done by
# subtracting out the rating from each category that restaurant is 
# associated with. 

# Run the algorithm on this adjusted user's feature set and restaurant.
# Check how close the output of algorithm is to actual review.
import mongo
import yelp
import config
import json
import copy
import time
import similarity
import multiprocessing
import threading

yelpDB = mongo.Mongo()
MIN_BUSINESS_REVIEWS = 10
STAR_THRESHOLD = 1
START = 0
END = 100


#		print i, 'Average MSE: unweight: '+str(sum(unweightErrors) / float(total))+ ', weight: '+str(sum(weightErrors) / float(total)),'  |  ', 'Error in star prediction: unweight: '+ str(100.0 * float(unweightIncorrect) / float(total)) + '%'+ ', weight: '+ str(100.0 * float(weightIncorrect) / float(total)) + '%'



class multiTest(multiprocessing.Process):
    def __init__(self, s, e):
        multiprocessing.Process.__init__(self)
        self.s = s
        self.e = e
    def run(self):
        Test(self.s, self.e)

def Test(start, end):
	for i in range(20,21)
		absErrors = []
		mostErrors = []
		unweightErrors = []
		weightErrors = []

		absMostErrors = []
		absUnweightErrors = []
		absWeightErrors = []

		mostIncorrect = 0
		unweightIncorrect = 0
		weightIncorrect = 0
		total = 0
		inc = 0
		testFile = open(config.data['test'], 'r')
		testVectors = {}
		for line in testFile:
		    data = json.loads(line, 'utf-8')
		    testVectors[data['business_id']] = data['user_ids']
		testFile.close()
		for businessId in testVectors:
		    if inc < start:
		        inc += 1
		        continue
		    testUserId = testVectors[businessId][0]
		    testVectors[businessId].remove(testUserId)
		    mostError, mostPred, unweightError, unweightPred, weightError, weightPred, actual = GetUserStarPrediction(testUserId, businessId, testVectors[businessId],i)
		    mostErrors.append(mostError ** 2)
		    unweightErrors.append(unweightError ** 2)
		    weightErrors.append(weightError ** 2)

		    absMostErrors.append(abs(mostError))
		    absUnweightErrors.append(unweightError)
		    absWeightErrors.append(weightError)

		    if abs(mostPred - actual) > STAR_THRESHOLD:
		        mostIncorrect += 1
		    if abs(unweightPred - actual) > STAR_THRESHOLD:
		        unweightIncorrect += 1
		    if abs(weightPred - actual) > STAR_THRESHOLD:
		        weightIncorrect += 1
		    total += 1
		    inc += 1
		    if inc >= end:
		        break
		    print 'finished with test vector ' + str(inc)

		resultFile = open('results/' + str(start) + '_' + str(end) + '.txt', 'w')
		resultFile.write('Average Abs Error is: most:' + str(sum(absMostErrors) / float(total))  + ', unweight: ' + str(sum(absUnweightErrors) / float(total)) + ', weight: ' + str(sum(absWeightErrors) / float(total)) + '\n')
		resultFile.write('Average MSE is: ' + 'most: '+str(sum(mostErrors) / float(total))+ ', unweight: '+str(sum(unweightErrors) / float(total))+ ', weight: '+str(sum(weightErrors) / float(total)) + '\n')
		resultFile.write('Error in star prediction is: ' + 'most: '+ str(100.0 * float(mostIncorrect) / float(total)) + '%'+ ', unweight: '+ str(100.0 * float(unweightIncorrect) / float(total)) + '%'+ ', weight: '+ str(100.0 * float(weightIncorrect) / float(total)) + '%' + '\n')
		resultFile.close()
>>>>>>> 53e4af8240f2a3bab23178b659386aeb17b3ed93
    return

def GetUserStarPrediction(userId, businessId, userIds, i):
    # userId = '5W_Dv1E2loDsoXFpi-pqcQ'
    # businessId = 'SKLw05kEIlZcpTD5pqma8Q'
    user = yelpDB.GetUserById(userId)
    business = yelpDB.GetBusinessById(businessId)
    user['feature'] = AdjustUserFeatures(user, business)
    actual = yelpDB.GetStarsByUserAndBusinessId(userId, businessId)
    # most similar, unweighted avg, weighted avg
<<<<<<< HEAD
    mostPred, unweightPred, weightPred = yelp.GetStarPrediction(yelpDB, userId, businessId, i, user=user, userIds=userIds)
=======
    # mostPred, unweightPred, weightPred = similarity.TestPredictStars(yelpDB, user, userIds, businessId)
    mostPred, unweightPred, weightPred = yelp.GetStarPrediction(yelpDB, userId, businessId, user=user, userIds=userIds)

>>>>>>> 53e4af8240f2a3bab23178b659386aeb17b3ed93
    print 'Star Prediction: ' + 'most: ' + str(mostPred)+ ', unweight: ' + str(unweightPred)+ ', weight: ' + str(weightPred) + ' Actual: ' + str(actual) 
    return (abs(float(mostPred) - float(actual)), mostPred, abs(float(unweightPred) - float(actual)), unweightPred, abs(float(weightPred) - float(actual)), weightPred, actual)
    #most error, most pred, unweight error, unweight pred, weight error, weight hpred, actual


def AdjustUserFeatures(user, business):
    adjFeatures = copy.deepcopy(user['feature'])
    review = yelpDB.GetReviewByUserAndBusinessId(user['_id'], business['_id'])
    stars = review['stars']
    businessCategories = business['categories']
    for c in user['feature']:
        if c in businessCategories:
            adjFeatures[c][0] = adjFeatures[c][0] * adjFeatures[c][1] - stars
            adjFeatures[c][1] -= 1
            if adjFeatures[c][1] == 0:
                del adjFeatures[c]
                # adjFeatures[c][0] = 0
            else:
                adjFeatures[c][0] = adjFeatures[c][0] / adjFeatures[c][1]
    adjFeatures['average_stars'] = (user['average_stars'], 1)
    return adjFeatures

def GetTestData():
    businesses = yelpDB.GetAllBusinesses()
    testFile = open(config.data['test'], 'w')
    for business in businesses:
        userIds = []
        reviews = yelpDB.GetReviewsByBusinessId(business['_id'])
        for review in reviews:
            userId = review['user_id']
            exists = yelpDB.GetUserById(userId)
            if exists != None:
                userIds.append(review['user_id'])
        if len(userIds) < MIN_BUSINESS_REVIEWS:
            print 'not enough reviews for ' + business['_id']
            continue
        data = {'business_id': business['_id'], 'user_ids': userIds}
        testFile.write(json.dumps(data) + '\n')
        print 'YAY! enough reviews for ' + business['_id']
    testFile.close()

if __name__ == "__main__":  
    test1 = multiTest(0, 250)
    test2 = multiTest(251, 500)
    test3 = multiTest(501, 750)
    test4 = multiTest(751, 1000)
    test1.start()
    test2.start()
    test3.start()
    test4.start()
