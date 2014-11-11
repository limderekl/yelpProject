import json 
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

#returns review ID, review rating for a random review by userID
def getRandUserRev(userID, reviewList): 
    #list of reviews given by userID
    userRevList = []
    for review in reviewList: 
        if review["user_id"] == userID: 
            userRevList.append(review)
    #print "user review list : {0}".format(userRevList)
    randRev = random.choice(userRevList)
    #print "rand review : {0}".format(randRev)
    return randRev["review_id"], randRev["stars"]
    
#first baseline of prediction based solely on most commonly given rating by user. 
#baseline1 is a single run, runBaseline1 is multiple
def baseline1(userID, userList, reviewList): 
    #get a random user review to be tested on, returns a tuple
    testRevID, testRevRating = getRandUserRev(userID, reviewList)
    #gets avg star rating for userID
    for user in userList: 
        if userID == user["user_id"]: 
            predRating = round(user["average_stars"])
            break
    accuracy = 1 if testRevRating == predRating else 0
    return predRating, accuracy

#second baseline of prediction based solely on avg business review
#baseline2 is a single run, runBaseline2 is multiple
def baseline2(userID, userList, reviewList): 
    #get a random user review to be tested on, returns a tuple
    testRevID, testRevRating = getRandUserRev(userID, reviewList)
    #gets avg star rating for userID
    for user in userList: 
        if userID == user[user_id]: 
            predRating = round(user[average_stars])
            break
    accuracy = 1 if testRevRating == predRating else 0
    return predRating, accuracy
#def ratingDist(reviewList): 
    #for review in reviewList: 
        
    #return
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
    
userList = readUser()
reviewList = readReview()
runBaseline1(userList, reviewList, 20)
#print getNumUserRev(userList, 50,float("inf"))
    

