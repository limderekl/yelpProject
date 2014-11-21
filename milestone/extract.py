import json 
MIN_REVIEWS = 50
MAX_REVIEWS = 80
directory = "../Yelp/"
userFilename = "yelp_academic_dataset_user.json"
reviewFilename = "yelp_academic_dataset_review.json"
businessFilename = "yelp_academic_dataset_business.json"

def extractUsersFromReviews(filename):
    userList = {}
    jsonFile = open(directory+filename)
    for line in jsonFile:
        data = json.loads(line, encoding = 'utf-8')
        userId = data['user_id']
        if userId in userList:
            userList[userId].append(data['business_id'])
        else:
            userList[userId] = [data['business_id']]
    jsonFile.close()

    acceptedUsers = {}
    for userId in userList:
        if (len(userList[userId]) > MIN_REVIEWS) and (len(userList[userId]) < MAX_REVIEWS):
            acceptedUsers[userId] = userList[userId]
    return acceptedUsers

def extractBusinessFromReviews(userIds, filename):
    businessList = []
    jsonFile = open(directory+filename)
    for line in jsonFile:
        data = json.loads(line, encoding = 'utf-8')
        for uId in userIds:
            if uId == data['user_id']:
                businessList.append(data['business_id'])
    jsonFile.close()
    return businessList


def writeUsersDataset(userIds, filename):
    jsonFile = open(directory + filename)
    reducedFile = open(directory + 'reduced_' + filename, 'wb')
    for line in jsonFile:
        data = json.loads(line, encoding = 'utf-8')
        for uId in userIds:
            if uId == data['user_id']:
                encodeData = json.dumps(data)
                reducedFile.write(encodeData + '\n')
    reducedFile.close()
    jsonFile.close()
    return 

def writeBusinessDataset(acceptedUsers, filename):
    businessIds = []
    for userId in acceptedUsers:
        for bId in acceptedUsers[userId]:
            if businessIds.count(bId) == 0:
                businessIds.append(bId)
    jsonFile = open(directory + filename)
    reducedFile = open(dir)
    reducedFile = open(directory + 'reduced_' + filename, 'wb')
    for line in jsonFile:
        data = json.loads(line, encoding = 'utf-8')
        for bId in businessIds:
            if bId == data['business_id']:
                encodeData = json.dumps(data)
                reducedFile.write(encodeData + '\n')
    reducedFile.close()
    jsonfile.close()
    return 

def writeReviewDataset(userIds, filename):
    jsonFile = open(directory + filename)
    reducedFile = open(directory + 'reduced_' + filename, 'wb')
    for line in jsonFile:
        data = json.loads(line, encoding = 'utf-8')
        for uId in userIds:
            if uId == data['user_id']:
                encodeData = json.dumps(data)
                reducedFile.write(encodeData + '\n')
    reducedFile.close()
    jsonfile.close()
    return 

# # # get the reduced users data
# print 'Getting users'
# acceptedUsers = extractUsersFromReviews(reviewFilename)
# print 'Finished getting users'
# # businessIds = extractBusinessFromReviews(reviewFilename, userIds)
# writeUsersDataset(acceptedUsers.keys(), userFilename)
# print 'Finished reducing user dataset'
# # writeBusinessDataset(acceptedUsers, businessFilename)
# # print 'Finished reducing business dataset'
# # # writeReviewDataset(userIds, reviewFilename)
# # # print 'Finished reducing review dataset'

# def writeReviewDataset(filename):
#     userIds = []
#     userFile = open(directory + "reduced_yelp_academic_dataset_user.json")
#     for line in userFile:
#         data = json.loads(line, encoding = 'utf-8')
#         userIds.append(data['user_id'])
#     userFile.close()

#     reducedFile = open(directory + 'reduced_' + filename, 'wb')
#     reviewFile = open(directory + filename)
#     for line in reviewFile:
#         data = json.loads(line, encoding = 'utf-8')
#         for uId in userIds:
#             if uId == data['user_id']:
#                 encodedData = json.dumps(data)
#                 reducedFile.write(encodedData + '\n')
#     reviewFile.close()
#     reducedFile.close()
#     return
# print 'getting review dataset'
# writeReviewDataset(reviewFilename)

def writeBusinessDataset(filename):
    businessIds = []
    reviewFile = open(directory + 'reduced_yelp_academic_dataset_review.json')
    for line in reviewFile:
        data = json.loads(line, encoding = 'utf-8')
        if businessIds.count(data['business_id']) == 0:
            businessIds.append(data['business_id'])
    reviewFile.close()

    reducedFile = open(directory + 'reduced_' + filename, 'wb')
    businessFile = open(directory + filename)
    for line in businessFile:
        data = json.loads(line, encoding = 'utf-8')
        for bId in businessIds:
            if bId == data['business_id']:
                encodedData = json.dumps(data)
                reducedFile.write(encodedData + '\n')
    businessFile.close()
    reducedFile.close()
    return
print 'getting business dataset'
writeBusinessDataset(businessFilename)