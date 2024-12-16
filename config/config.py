from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://lamtruong3242:vanlam0384586024@my-cluster.i8ego.mongodb.net/?retryWrites=true&w=majority&appName=my-cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.furniture_shop

product_collection = db['products']
order_collection = db['orders']
user_collection = db['users']


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)