N = 5 # max number of similar users to find

# yelpDB is passed from yelp.py and is a Mongo instance so no need 
# to reconnect to mongo here
def PredictStars(yelpDB, userId, userIds, businessId):
    #userId: user for prediction, userIds: other users who have reviewed a given restaurant
    stars = 0.0
    # get all feature arrays of users in userIds array and compare
    # to userId. Use top N similar users to predict userIds star
    # rating of that restaurant and return (stars should be type int)

    return stars
import mongo 
def test(): 
    yelpDB = mongo.Mongo()
    user = yelpDB.GetUserById('EaVmK7PPnV5TAEvB_tg-sw')
    print user['feature']

    return
test()
