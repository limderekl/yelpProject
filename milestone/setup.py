import json 
import numpy as np
import random

#set directory which data is located
#dataDir = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/"
dataDir = "/afs/.ir.stanford.edu/users/l/i/limderek/cs229/yelpProject/projectData/" #located on corn
#returns a dict of dicts, each inner dict is a user or business or review object. 
#outer dict indexed by user_id
#def readUser(file = dataDir+"yelp_academic_dataset_user.json"): 
def readUser(file = "smallUser.json"):
    userDict= {}
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        #extracts only wanted features
        newData = {}
        newData["friends"] = len(data["friends"])# of friends
        wantedList = ["user_id", "review_count", "average_stars", "votes", "elite", "yelping_since", "fans"]
        for item in wantedList: 
            newData[item] = data[item]
        userDict[newData["user_id"]] = newData
    json_file.close()
    return userDict
#outer dict indexed by business_id
#def readBusiness(file = dataDir+"yelp_academic_dataset_business.json"): 
def readBusiness(file = "smallBusiness.json"):
    businessDict = {}
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        #extracts wanted features
        newData = {}
        wantedList = ["business_id", "stars", "review_count", "categories"]
        for item in wantedList: 
            newData[item] = data[item]
        #extra price range from attributes, if none set as None
        if "Price Range" in data["attributes"]: 
            newData["price_range"] = data["attributes"]["Price Range"]
        else: 
            newData["price_range"] = None
        businessDict[newData["business_id"]] = newData
    json_file.close()
    return businessDict
#returns a dict of lists with keys of business_id, all reviews on same business in list
#def readReview(file = dataDir+"yelp_academic_dataset_review.json"): 
def readReview(file = "smallReview.json"):
    reviewDict = {}
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        #extracts wanted features
        newData = {}
        wantedList = ["business_id", "user_id", "stars", "date", "votes"]
        for item in wantedList: 
            newData[item] = data[item]
        if newData["business_id"] in reviewDict:
            reviewDict[newData["business_id"]].append(newData) # = newData
        else:
            reviewDict[newData["business_id"]] = [newData]
    json_file.close()
    return reviewDict
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
def getRandUserRev(userID, reviewDict): 
    #list of reviews given by userID
    userRevList = []
    for allBusRev in reviewDict.values():#allBusRev is a list of all reviews for a given business
        if allBusRev[0]["user_id"] == userID: 
            for review in allBusRev:
                userRevList.append(review)
    #print "user review list : {0}".format(userRevList)
    randRev = random.choice(userRevList)
    #print "rand review : {0}".format(randRev)
    return randRev
    
#returns a dictionary of star rating to count
def ratingDist(reviewDict): 
    distr = {}
    for review in reviewDict: 
        distr[review["stars"]] = distr.get(review["stars"],0) + 1
    return distr
# userDict = readUser()
# reviewDict = readReview()
# businessDict = readBusiness()
# print "userDict : {0}".format(userDict) + '\n'
# print "reviewDict: {0}".format(reviewDict) + '\n'
# print "businessDict: {0}".format(businessDict) + '\n'
#print getNumUserRev(userList, 100,float("inf"))
