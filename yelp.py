import json

data = []
with open('yelp/yelp_academic_dataset_review.json') as f:
    for line in f:
        data.append(json.loads(line))
        print data
        print data[0].user_id
        break
    