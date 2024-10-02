import pymongo
from pymongo.errors import ServerSelectionTimeoutError

mongo_uri = "mongodb://192.168.5.143:27017/"

def connect_to_mongo(uri) -> pymongo.MongoClient:
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Trigger exception if connection fails
        print("Connected to MongoDB!")
        return client
    except ServerSelectionTimeoutError as e:
        print(f"Could not connect to MongoDB: {e}")
        raise

def query_documents(db, collection_name, field_name, filter_value, excluded_fields=None, limit=100) -> None:
    """
    Query a MongoDB collection based on a filter.
    
    :param db: The database object.
    :param collection_name: Name of the collection to query.
    :param field_name: The field to filter by.
    :param filter_value: The value that field should not be equal to.
    :param excluded_fields: A list of field names to exclude from the result (e.g., ["data"]).
    """
    # Select the collection
    collection = db[collection_name]
    
    # Query documents where the specified field is not equal to the filter_value
    query = {field_name: {"$ne": filter_value}}

    # Projection to exclude fields if provided
    projection = {field: 0 for field in excluded_fields} if excluded_fields else None

    try:
        # Perform the query
        results = collection.find(query, projection).limit(limit)

        # Print each document found
        for doc in results:
            print(doc)
    except Exception as e:
        print(f"Error querying documents: {e}")

def main():
    client = connect_to_mongo(mongo_uri)
    db = client["team5_vm3_db"]

    # Query the 'images' collection where 'inferedValue' is not blank, excluding the 'data' field
    query_documents(db, collection_name="images", field_name="inferedValue", filter_value="", excluded_fields=["data"])
    query_documents(db, collection_name="images", field_name="inferedValue", filter_value="1", excluded_fields=["data"], limit=2)

    # Close the connection
    client.close()

if __name__ == "__main__":
    main()

