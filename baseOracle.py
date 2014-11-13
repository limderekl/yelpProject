import json
import setup
import numpy as np

userDict = setup.readUser('Reduced_Yelp_Data/reduced_yelp_academic_dataset_user.json')
businessDict = setup.readBusiness('Reduced_Yelp_Data/reduced_yelp_academic_dataset_business.json')
reviewDict= setup.readReview('Reduced_Yelp_Data/reduced_yelp_academic_dataset_review.json')

#first baseline of prediction based solely on most commonly given rating by user. 
#baseline1 is a single run, runBaseline1 is multiple
def baseline1(userID, userDict, reviewDict): 
    #get a random user review to be tested on,
    testRev = setup.getRandUserRev(userID, reviewDict)
    testRevRating= testRev["stars"]
    #gets avg star rating for userID
    predRating = userDict[userID]["average_stars"]
    return predRating, testRevRating

def runBaseline1(userDict, reviewDict, revCountThreshold): 
    totalUsers = 0.0
    numErrors= 0.0
    #for i in xrange(1000):    
    for user in userDict.values():
        #only run for users who meet revCountThreshold
        if user["review_count"] >=revCountThreshold: 
            predRating, testRevRating = baseline1(user["user_id"], userDict, reviewDict)
            if abs(predRating - testRevRating)> .5: 
                numErrors += 1
            totalUsers += 1
    print "totalUsers: {0}, numErrors: {1} -> % error: {2}".format(totalUsers, numErrors, numErrors/totalUsers)
    return
    
#second baseline of prediction based solely on avg business review
#baseline2 is a single run, runBaseline2 is multiple
def baseline2(userID, userDict, reviewDict, businessDict): 
    #get a random user review to be tested on, returns a tuple
    testRev = setup.getRandUserRev(userID, reviewDict)
    testBusinessID= testRev["business_id"]
    testRevRating= testRev["stars"]
    #gets avg star rating business
    predRating = businessDict[testBusinessID]['stars']
    return predRating, testRevRating 
def runBaseline2(userDict, reviewDict, businessDict, revCountThreshold): 
    totalUsers= 0.0
    numErrors = 0.0
    for user in userDict.values():
        #only run for those with review count > threshold
        if user["review_count"] >=revCountThreshold: 
            predRating, testRevRating= baseline2(user["user_id"], userDict, reviewDict, businessDict)
            if abs(predRating - testRevRating)> .5: 
                numErrors += 1
            totalUsers += 1
    print "totalUsers: {0}, numErrors: {1} -> % error: {2}".format(totalUsers, numErrors, numErrors/totalUsers)
runBaseline1(userDict, reviewDict, 50)
runBaseline2(userDict, reviewDict, businessDict, 50)
