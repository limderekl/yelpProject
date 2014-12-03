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

yelpDB = mongo.Mongo()
MIN_BUSINESS_REVIEWS = 10
STAR_THRESHOLD = 1

def Test():
    errors = []
    incorrect = 0
    total = 0
    testFile = open(config.data['test'], 'r')
    testVectors = {}
    for line in testFile:
        data = json.loads(line, 'utf-8')
        testVectors[data['business_id']] = data['user_ids']
    testFile.close()
    for businessId in testVectors:
        error, prediction, actual = GetUserStarPrediction(testVectors[businessId][0], businessId)
        errors.append(error ** 2)
        if abs(prediction-actual) > STAR_THRESHOLD:
            incorrect += 1
        total += 1
    print 'Average MSE is: ' + str(sum(errors) / float(total))
    print 'Error in star prediction is: ' + str(100.0 * float(incorrect) / float(total)) + '%'
    return

def GetUserStarPrediction(userId, businessId):
    # userId = '5W_Dv1E2loDsoXFpi-pqcQ'
    # businessId = 'SKLw05kEIlZcpTD5pqma8Q'
    user = yelpDB.GetUserById(userId)
    business = yelpDB.GetBusinessById(businessId)
    user['feature'] = AdjustUserFeatures(user, business)
    actual = yelpDB.GetStarsByUserAndBusinessId(userId, businessId)
    prediction = yelp.GetStarPrediction(yelpDB, userId, businessId, user)
    print 'Star Prediction: ' + str(prediction) + ' Actual: ' + str(actual) 
    return (abs(float(prediction) - float(actual)), prediction, actual) 

def AdjustUserFeatures(user, business):
    adjFeatures = user['feature']
    review = yelpDB.GetReviewByUserAndBusinessId(user['_id'], business['_id'])
    stars = review['stars']
    businessCategories = business['categories']
    for c in user['feature']:
        if c in businessCategories:
            adjFeatures[c][0] = adjFeatures[c][0] * adjFeatures[c][1] - stars
            adjFeatures[c][1] -= 1
            if adjFeatures[c][1] == 0:
                adjFeatures[c][0] = 0
            else:
                adjFeatures[c][0] /= adjFeatures[c][1]
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

#Test()

businessId = "GGyHZtnAA5LBgouB-32ARA"

businesses = yelpDB.GetAllBusinesses()
i = 0
for b in businesses:
    if b['_id'] == businessId:
        break
    else:
        i += 1
print i