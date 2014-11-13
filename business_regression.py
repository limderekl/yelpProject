import numpy
import setup
import json
import collections

users = setup.readUser('Reduced_Yelp_Data/reduced_yelp_academic_dataset_user.json')
business = setup.readBusiness('Reduced_Yelp_Data/reduced_yelp_academic_dataset_business.json')
reviewPath = 'Reduced_Yelp_Data/reduced_yelp_academic_dataset_review.json'
MIN_NUM = 80
ERROR_THRESHOLD = 1
VERBOSE = False

def getMostBusinessReviews():
    bIds = {}
    reviewFile = open(reviewPath)
    for line in reviewFile:
        data = json.loads(line, encoding = 'utf-8')
        if data['business_id'] in bIds:
            bIds[data['business_id']] += 1
        else:
            bIds[data['business_id']] = 1

    writeFile = open('common_business.txt', 'wb')
    commonBs = []
    for b in bIds:
        if bIds[b] >= MIN_NUM:
            commonBs.append(b)
            writeFile.write(b + '\n')
    writeFile.close()
    return commonBs

def getBusinessReviews(bId):
    bReviews = []
    reviewFile = open(reviewPath)
    for line in reviewFile:
        data = json.loads(line, encoding = 'utf-8')
        if data['business_id'] == bId:
            bReviews.append(data)
    return bReviews

def parseReviews(bReviews, trainRatio, features):
    trainRating = []
    trainFeature = []
    for i in xrange(0, len(features)):
        trainFeature.append([])
    for r in range(0, len(bReviews)):
        trainRating.append(bReviews[r]['stars'])
        uId = bReviews[r]['user_id']
        for f in xrange(0, len(features)):
            # split by comma
            fs = features[f].split(',')
            val = users[uId][fs[0]]
            for i in xrange(1, len(fs)):
                val = val[fs[i]]
            trainFeature[f].append(val)
    trainFeature.append([1] * len(bReviews))
    testFeature = []
    testRating  = []
    s = int(len(bReviews) * trainRatio)
    testRating = trainRating[s:]
    trainRating = trainRating[0:s]
    newTrainFeature = []
    for i in trainFeature:
        testFeature.append(i[s:])
        newTrainFeature.append(i[0:s])
    return (trainRating, newTrainFeature, testRating, testFeature)

def regress(trainRating, trainFeature):
    return numpy.linalg.lstsq(numpy.array(trainFeature).T, numpy.array(trainRating))[0]

def getHypothesis(testFeature, w, features):
    hypothesis = []
    for i in xrange(0, len(testFeature[0])):
        val = 0
        for j in xrange(0, len(features)+1):
            val += testFeature[j][i] * w[j]
        hypothesis.append(val)
    return hypothesis 

def printResult(hyp, testRating):
    error = 0
    if len(hyp) == 0:
        return 'not enough test samples'
    for i in range(0, len(hyp)):
        if VERBOSE:
            print 'Actual: ' + str(testRating[i]) + ' Prediction: ' + str(hyp[i])
        if abs(testRating[i] - hyp[i]) > ERROR_THRESHOLD:
            error += 1
    if VERBOSE:
        print 'Errors: ' + str(error) + '/' + str(len(hyp)) + ' -> ' + str(float(error)/float(len(hyp)) * 100) + '%'
    return str(float(error)/float(len(hyp)) * 100)

def businessRegression(bId, trainRatio, features, minNum = 10):
    bReviews = getBusinessReviews(bId)
    if len(bReviews) < minNum:
        print 'Not Enough Samples For bId: ' + bId
        return 

    trainRating, trainFeature, testRating, testFeature = parseReviews(bReviews, trainRatio, features)
    if VERBOSE:
        print trainFeature
        print testFeature
    w = regress(trainRating, trainFeature)
    if VERBOSE:
        print w
    hypRating = getHypothesis(testFeature, w, features)
    error = printResult(hypRating, testRating)
    return error

# vary the features
# vary the training and testing set ratio
# do this for each restaurant
def run():
    output = open('output.txt', 'wb')
    business = ['jf67Z1pnwElRSXllpQHiJg', 'PXviRcHR1mqdH4vRc2LEAQ', '2e2e7WgqU1BnpxmQL5jbfw', '4bEjOyTaDG24SY5TxsaUNQ']
    totalFeatures = ['review_count', 'average_stars', 'friends', 'votes,funny', 'votes,useful', 'votes,cool'] 
    
    length = len(totalFeatures)
    bi = bin(1)[2:].zfill(length)
    for f in xrange(1, 2**length):
        features = []
        for j in range(0, length):
            if bi[j] == '1':
                features.append(totalFeatures[j])
        bi = bin(int(bi, 2)+1)[2:].zfill(length) 

        d = {}
        d['features'] = features
        d['business'] = {}
        for b in business:
            d['business'][b] = []
            for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
                error = businessRegression(b, i, features, 10)
                d['business'][b].append(error)
        output.write(json.dumps(d) + '\n')
        print 'Finished with feature set: ' + str(features)
    output.close()

run()

def analyze():
    feature_data = open('feature_validation_data.json')
    for line in feature_data:
        data = json.loads(line, encoding = 'utf-8')
        features = data['features']
        print features
        business = data['business']
        avgError = [0] * 9
        for b in business:
            for e in xrange(0, len(business[b])):
                avgError[e] += float(business[b][e])
        print 'avg errors: '
        for e in xrange(0, len(avgError)):
            avgError[e] = avgError[e]/len(business)
            print avgError[e]
        print
    feature_data.close()


#analyze()



