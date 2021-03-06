# Examples for interfacing with database. All the methods in the mongo
# class can be found in mongo.py. Try to only use the methods defined 
# in the class as this prevents data corruption (unwanted erasures, etc).
# If we need a field to be added to all documents in a collection, tell
# me and I'll run a migration.
import mongo
# remember to create the credentials.py file (see README.md)
# connect to yelp database, this instantiates the Mongo class
yelpDB = mongo.Mongo()

# example of getting a single user object
user = yelpDB.GetUserById('Qtro4APUHh1wEwnVhciPPQ')
print "1", user   # treat as a dictionary

# example for setting the feature vector for a user
user = yelpDB.SetUserFeatureSet('Qtro4APUHh1wEwnVhciPPQ', [2.5, 1, 5])
print "2", user

# example for getting all businesses, the index i is just used
# to limit the number of items printed out
businesses = yelpDB.GetAllBusinesses()
i = 0
for business in businesses:
    print business
    i += 1
    if i > 5:
        break

# example for querying reviews by user id
reviews = yelpDB.GetReviewsByUserId('Qtro4APUHh1wEwnVhciPPQ')
i = 0
for review in reviews:
    print review
    i += 1
    if i > 5:
        break
