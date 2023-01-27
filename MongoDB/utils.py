from pymongo import MongoClient
def connectToMongo( password):

    client = MongoClient(f"mongodb+srv://seconduser:{password}@tobbetuseniors.wxh9mrf.mongodb.net/?retryWrites=true&w=majority")
    
    return  client