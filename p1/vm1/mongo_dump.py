import pymongo
from pymongo.errors import ServerSelectionTimeoutError

mongo_uri = "mongodb://192.168.5.143:27017/"

try:
    # Connect
    client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Check server connection
    client.server_info()
    print("Connected to MongoDB!")

    # List all databases
    databases = client.list_database_names()
    print("Databases:", databases)

    # Iterate over each database
    for db_name in databases:
        print(f"\nDatabase: {db_name}")
        
        # Select the database
        db = client[db_name]
        
        # List all collections in the current database
        collections = db.list_collection_names()
        print(f" Collections in {db_name}: {collections}")

        # List some documents in each collection
        for col_name in collections:
            collection = db[col_name]
            print(f"  Documents in {col_name}:")
            
            # Print the first 5 documents in each collection for preview
            documents = collection.find().limit(5)
            for doc in documents:
                print(f"   {doc}")

except ServerSelectionTimeoutError as e:
    print(f"Could not connect to MongoDB: {e}")
finally:
    # Close the connection
    client.close()

