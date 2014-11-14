import numpy
import setup
import json

users = setup.readUser('Reduced_Yelp_Data/reduced_yelp_academic_dataset_user.json')
business = setup.readBusiness('Reduced_Yelp_Data/reduced_yelp_academic_dataset_business.json')
reviews = setup.readReview('Reduced_Yelp_Data/reduced_yelp_academic_dataset_review.json')
######
reviewPath = 'Reduced_Yelp_Data/reduced_yelp_academic_dataset_review.json'
features = ['review_count', 'average_stars', 'friends']
MIN_NUM = 80
#########
'''
userFeatures = ['review_count', 'friends', 'fans']
businessFeatures = ['review_count']
allFeatures = ['u_review_count', 'u_friends', 'u_fans', 'b_review_count']

userFeatures = ['average_stars']
businessFeatures = ['stars']
allFeatures = ['u_average_stars', 'b_stars']
'''

userFeatures = ['review_count', 'average_stars', 'friends', 'fans']
businessFeatures = ['review_count', 'stars']
allFeatures = []
#allFeatures = ['u_review_count', 'u_average_stars', 'u_friends', 'u_fans', 'b_review_count', 'b_stars']

def getReviewFeatures():
    dataSet = []
    y = []
    for rKey in reviews.keys():
        for review in reviews[rKey]:
            dataSetEntry = {}
#            dataSetEntry['user_id'] = review['user_id']
#            dataSetEntry['business_id'] = review['business_id']
            y.append(review['stars'])
            for feature in userFeatures:
                if 'u_'+feature in allFeatures:
                    dataSetEntry['u_'+feature] = users[review['user_id']][feature]
            for feature in businessFeatures:
                if 'b_'+feature in allFeatures:
                    dataSetEntry['b_'+feature] = business[review['business_id']][feature]
#            print dataSetEntry, y[-1]
            dataSet.append(dataSetEntry)        
    return dataSet, y

def rparseReviews(reviews, y, trainRatio):
    trainRating = []
    trainFeature = []
    for i in xrange(0,len(allFeatures)):
        trainFeature.append([])
    for r in range(0,len(reviews)):
        trainRating.append(y[r])
        for f in xrange(0,len(allFeatures)):
            trainFeature[f].append(reviews[r][allFeatures[f]])
    trainFeature.append([1]*len(reviews))
    testFeature = []
    testRating = []
    s = int(len(reviews) * trainRatio)
    testRating = trainRating[s:]
    trainRating = trainRating[0:s]
    newTrainFeature = []
    for i in trainFeature:
        testFeature.append(i[s:])
        newTrainFeature.append(i[0:s])
    return (trainRating, newTrainFeature, testRating, testFeature)

def regress(trainRating, trainFeature):
    return numpy.linalg.lstsq(numpy.array(trainFeature).T, numpy.array(trainRating))[0]

#

def getHypothesis(testFeature, w):
    hypothesis = []
    for i in xrange(0, len(testFeature[0])):
        val = 0
        for j in xrange(0, len(allFeatures)+1):
            val += testFeature[j][i] * w[j]
        hypothesis.append(val)
    return hypothesis 

def printResult(hyp, testRating,train):
    error = 0
    for i in range(0, len(hyp)):
    #    print 'Actual: ' + str(testRating[i]) + ' Prediction: ' + str(hyp[i])
        if abs(testRating[i] - hyp[i]) > 1.0:
            error += 1
    #print allFeatures, 'Ratio: ' +str(train)+ ' Errors: ' + str(error) + '/' + str(len(hyp)) + ' -> ' + str(float(error)/float(len(hyp)) * 100) + '%'
    return float(error)/float(len(hyp))*100

def reviewRegression(trainRatio):
    featureVec, yVec = getReviewFeatures()
    trainRating, trainFeature, testRating, testFeature = rparseReviews(featureVec, yVec, trainRatio)
    w = regress(trainRating, trainFeature)
    hypRating = getHypothesis(testFeature, w)
    err = printResult(hypRating, testRating,trainRatio)
    return err


'''


businessFeatures
userFeatures
allFeatures
'''
'''
def permuteFeatures(index,featureList):
    permutations = []
    if index == len(featureList):
        temp = []
        return temp
    else:
        
    
    return permutations
''' 

def run():
    allRuns = []
    masterAllFeatures = ['u_review_count', 'u_average_stars', 'u_friends', 'u_fans', 'b_review_count', 'b_stars']
    output = open('allOutput.txt', 'wb')
    length = len(masterAllFeatures)
    bi = bin(1)[2:].zfill(length)
    for f in xrange(1, 2**length):
        global allFeatures
        allFeatures = []
        for j in range(0, length):
            if bi[j] == '1':
                allFeatures.append(masterAllFeatures[j])
        bi = bin(int(bi, 2)+1)[2:].zfill(length) 
        allErrors = []
        for i in xrange(1,10):
            error = reviewRegression(i*0.1)
            allErrors.append(error)
        averageError = float(sum(allErrors))/len(allErrors)
        allRuns.append((allFeatures,averageError,allErrors))
        output.write(str(allRuns[-1])+'\n')
        print 'Finished with feature set: ' + str(allFeatures)
    output.close()

run()

