import json 
import pprint
#json_data = open("\\Users\\limbo0710\\Documents\\Stanford\\Fall2014\\cs229\\projectData\\yelp_dataset_challenge_academic_dataset2\\yelp_academic_dataset_user.json")
json_file = open("/Users/limbo0710/Documents/Stanford/Fall2014/cs229/projectData/yelp_dataset_challenge_academic_dataset2/yelp_academic_dataset_user.json")
line = json_file.readline()
print line
data = json.loads(line,encoding = "utf-8")
#pprint data[yelping_since]
#pprint( data)
print data
print 'test: '+data[u'yelping_since']
print 'test: '+data[yelping_since]
json_file.close()

