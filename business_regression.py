import numpy
import setup
import json

users = setup.readUser('Reduced_Yelp_Data/reduced_yelp_academic_dataset_user.json')
business = setup.readBusiness('Reduced_Yelp_Data/reduced_yelp_academic_dataset_business.json')
reviewPath = 'Reduced_Yelp_Data/reduced_yelp_academic_dataset_review.json'
features = ['review_count', 'average_stars', 'friends']
MIN_NUM = 80

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

def parseReviews(bReviews, trainRatio):
    trainRating = []
    trainFeature = []
    for i in xrange(0, len(features)):
        trainFeature.append([])
    for r in range(0, len(bReviews)):
        trainRating.append(bReviews[r]['stars'])
        uId = bReviews[r]['user_id']
        for f in xrange(0, len(features)):
            trainFeature[f].append(users[uId][features[f]])
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

def getHypothesis(testFeature, w):
    hypothesis = []
    for i in xrange(0, len(testFeature[0])):
        val = 0
        for j in xrange(0, len(features)+1):
            val += testFeature[j][i] * w[j]
        hypothesis.append(val)
    return hypothesis 

def printResult(hyp, testRating):
    error = 0
    for i in range(0, len(hyp)):
        print 'Actual: ' + str(testRating[i]) + ' Prediction: ' + str(hyp[i])
        if abs(testRating[i] - hyp[i]) > 0.5:
            error += 1
    print 'Errors: ' + str(error) + '/' + str(len(hyp)) + ' -> ' + str(float(error)/float(len(hyp)) * 100) + '%'

def businessRegression(bId, trainRatio, minNum):
    bReviews = getBusinessReviews(bId)
    if len(bReviews) < minNum:
        print 'Not Enough Samples For bId: ' + bId
        return 

    trainRating, trainFeature, testRating, testFeature = parseReviews(bReviews, trainRatio)
    # print trainFeature
    # print testFeature
    w = regress(trainRating, trainFeature)
    hypRating = getHypothesis(testFeature, w)
    printResult(hypRating, testRating)
    return

businessRegression('jf67Z1pnwElRSXllpQHiJg', 0.50, 10)

# print getMostBusinessReviews()

