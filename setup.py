import json 
import numpy as np
import random

#set directory which data is located
#dataDir = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/"
dataDir = "/afs/.ir.stanford.edu/users/l/i/limderek/cs229/yelpProject/projectData/" #located on corn
#returns a list of dicts, each dict is a user or business or review object. 
def readUser(file = dataDir+"yelp_academic_dataset_user.json"): 
#def readUser(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/oneObj.json"): 
    userList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        userList.append(data)
    json_file.close()
    return userList
def readBusiness(file = dataDir+"yelp_academic_dataset_business.json"): 
    businessList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        businessList.append(data)
    json_file.close()
    return businessList
def readReview(file = dataDir+"yelp_academic_dataset_review.json"): 
    reviewList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        reviewList.append(data)
    json_file.close()
    return reviewList
def readCheckin(file = dataDir+"yelp_academic_dataset_checkin.json"): 
    checkinList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        checkinList.append(data)
    json_file.close()
    return checkinList
def readTip(file = dataDir+"yelp_academic_dataset_tip.json"): 
    tipList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        tipList.append(data)
    json_file.close()
    return tipList
#get num users with review count between min and max, inclusive
def getNumUserRev(userList, minN, maxN): 
    numUsers = 0
    for user in userList: 
        if user.get("review_count", 0) >= minN and user.get("review_count",0) <= maxN: 
            numUsers+=1
    return numUsers

#returns a random review for a userID
def getRandUserRev(userID, reviewList): 
    #list of reviews given by userID
    userRevList = []
    for review in reviewList: 
        if review["user_id"] == userID: 
            userRevList.append(review)
    #print "user review list : {0}".format(userRevList)
    randRev = random.choice(userRevList)
    #print "rand review : {0}".format(randRev)
    return randRev
    
#first baseline of prediction based solely on most commonly given rating by user. 
#baseline1 is a single run, runBaseline1 is multiple
def baseline1(userID, userList, reviewList): 
    #get a random user review to be tested on,
    testRev = getRandUserRev(userID, reviewList)
    testRevRating= testRev["stars"]
    #gets avg star rating for userID
    for user in userList: 
        if userID == user["user_id"]: 
            predRating = round(user["average_stars"])
            break
    accuracy = 1 if testRevRating == predRating else 0
    return predRating, accuracy

def runBaseline1(userList, reviewList, revCountThreshold): 
    totalCount = 0.0
    numCorrect = 0.0
    for i in xrange(1000):    
        #only run for those with 5 or more reviews
        if userList[i]["review_count"] >=revCountThreshold: 
            #print "user: {0}".format(userList[i])
            predRating, accuracy = baseline1(userList[i]["user_id"], userList, reviewList)
            numCorrect += accuracy #accuracy is 0 for incorrect, 1 for correct
            totalCount += 1
    print "totalCount: {0}, numCorrect: {1}, %: {2}".format(totalCount, numCorrect, numCorrect/totalCount)
    return
    
#second baseline of prediction based solely on avg business review
#baseline2 is a single run, runBaseline2 is multiple
def baseline2(userID, userList, reviewList, businessList): 
    #get a random user review to be tested on, returns a tuple
    testRev = getRandUserRev(userID, reviewList)
    testBusinessID= testRev["business_id"]
    testRevRating= testRev["stars"]
    #gets avg star rating for userID
    for business in businessList: 
        if testBusinessID == business["business_id"]:
            predRating = round(business["stars"])
            break
    accuracy = 1 if testRevRating == predRating else 0
    return predRating, accuracy
def runBaseline2(userList, reviewList, businessList, revCountThreshold): 
    totalCount = 0.0
    numCorrect = 0.0
    for i in xrange(1000):    
        #only run for those with review count > threshold
        if userList[i]["review_count"] >=revCountThreshold: 
            #print "user: {0}".format(userList[i])
            predRating, accuracy = baseline2(userList[i]["user_id"], userList, reviewList, businessList)
            numCorrect += accuracy #accuracy is 0 for incorrect, 1 for correct
            totalCount += 1
    print "totalCount: {0}, numCorrect: {1}, %: {2}".format(totalCount, numCorrect, numCorrect/totalCount)
#returns a dictionary of star rating to count
def ratingDist(reviewList): 
    distr = {}
    for review in reviewList: 
        distr[review["stars"]] = distr.get(review["stars"],0) + 1
    return distr

def getBusinessRating(businessID, businessList): 
    for business in businessList: 
        if businessID == business["business_id"]: 
            return business["stars"]
    return 3
userList = readUser()
reviewList = readReview()
businessList = readBusiness()
#runBaseline2(userList, reviewList, businessList, 100)
#runBaseline1(userList, reviewList, 0)
#print getNumUserRev(userList, 50,float("inf"))
