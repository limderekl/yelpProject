import json 

#returns a list of dicts, each dict is a user or business or review object. 
def readUser(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_user.json"): 
#def readUser(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/oneObj.json"): 
    userList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        userList.append(data)
    json_file.close()
    return userList
def readBusiness(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_business.json"): 
    businessList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        businessList.append(data)
    json_file.close()
    return businessList
def readReview(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_review.json"): 
    reviewList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        reviewList.append(data)
    json_file.close()
    return reviewList
def readCheckin(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_checkin.json"): 
    checkinList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        checkinList.append(data)
    json_file.close()
    return checkinList
def readTip(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_tip.json"): 
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


userList = readUser()
print getNumUserRev(userList, 50,float("inf"))
print getNumUserRev(userList, 50,100)

