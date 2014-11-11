import json 
def readUser(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_user.json"): 
#def readUser(file = "/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/oneObj.json"): 
    userList = []
    json_file = open(file)
    for line in json_file:
        data = json.loads(line,encoding = "utf-8")
        userList.append(data)
    json_file.close()
readUser()
