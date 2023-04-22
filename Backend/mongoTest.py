
from pymongo.mongo_client import MongoClient
def addToDatabase(dictionary):

    # Replace the placeholder with your Atlas connection string
    uri = "mongodb://localhost:27017"

    # Create a new client and connect to the server
    client = MongoClient(uri)

# Send a ping to confirm a successful connection
    db = client['classPlanner']
    lectures = db['lectures']
    discussions = db['discussions']
    print(db.list_collection_names())
    #books = db.books
    #print(books.find_one({'rating': {"$gt": 7}}))


