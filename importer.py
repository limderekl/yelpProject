# Data importer to Compose hosted MongoDB
# This script should just be run one time to import all data to Mongo

from pymongo import MongoClient
import config
import credentials
import json

def MongoConnect(user, secret, url):
    client = MongoClient('mongodb://' + user + ':' + secret + '@' + url)
    return client.playground

def ImportUserCollection(db, datafile, fields):
    collection = db.user
    datafile = open(datafile)
    for line in datafile:
        data = json.loads(line, encoding = 'utf-8')
        obj = {}
        for key in fields:
            if key == 'user_id':
                obj['_id'] = data[key]
            else:
                obj[key] = data[key]
        collection.insert(obj)
    datafile.close()
    return

def ImportBusinessCollection(db, datafile, fields):
    collection = db.business
    datafile = open(datafile)
    for line in datafile:
        data = json.loads(line, encoding = 'utf-8')
        obj = {}
        for key in fields:
            if key == 'business_id':
                obj['_id'] = data[key]
            else:
                obj[key] = data[key]
        # add this check here for fun, not really needed though
        if collection.find_one({'_id': obj['_id']}) == None:
            collection.insert(obj)
        else:
            print 'Index with id: ' + obj['_id'] + ' already exists, skipping ...'
    datafile.close()
    return

def ImportReviewCollection(db, datafile, fields):
    collection = db.review
    businessCol = db.business
    userCol = db.user
    datafile = open(datafile)
    for line in datafile:
        data = json.loads(line, encoding = 'utf-8')
        obj = {}
        # only insert if business and user are in database!
        if (businessCol.find_one({'_id': data['business_id']}) != None) and (userCol.find_one({'_id': data['user_id']}) != None):
            for key in fields:
                if key == 'review_id':
                    obj['_id'] = data[key]
                else:
                    obj[key] = data[key]
            collection.insert(obj)
    datafile.close()
    return

# This function should only be run once to set up the database. Never again afterwards!!
def DoImport():
    db = MongoConnect(credentials.mongo['user'], credentials.mongo['secret'], credentials.mongo['url'])
    # ImportUserCollection(db, config.data['user'], config.fields['user'])
    # ImportBusinessCollection(db, config.data['business'], config.fields['business'])
    # ImportReviewCollection(db, config.data['review'], config.fields['review'])
    return

# DoImport()