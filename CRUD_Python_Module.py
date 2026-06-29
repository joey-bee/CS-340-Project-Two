from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal Shelter collection in MongoDB """

    def __init__(self, username, password, host="localhost", port=27017, db_name="aac", collection_name="animals"):
        """
        Initializes the MongoClient and establishes connection authentication
        for the specified database and collection.
        """
        # Connection Variables
        USER = username
        PASS = password
        HOST = host
        PORT = port
        DB = db_name
        COL = collection_name

        # Initialize the Connection
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    def create(self, data):
        """
        Inserts a document into the specified MongoDB collection.
        Input: Dictionary (key/value pairs) representing the document.
        Return: True if successful insert, else False.
        """
        if data is not None and isinstance(data, dict):
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"An error occurred during creation: {e}")
                return False
        else:
            raise ValueError("Input data must be a non-empty dictionary")

    def read(self, query=None):
        """
        Queries for documents from the MongoDB collection.
        Input: Key/value lookup pair dictionary. Defaults to empty dictionary to return all.
        Return: Result in a Python list if successful, else an empty list.
        """
        if query is None:
            query = {}
            
        if isinstance(query, dict):
            try:
                # Use find() as required instead of find_one()
                cursor = self.collection.find(query)
                # Convert the returned MongoDB cursor to a standard Python list
                result_list = list(cursor)
                return result_list
            except Exception as e:
                print(f"An error occurred during read: {e}")
                return []
        else:
            raise ValueError("Query parameters must be formatted as a dictionary")

    def update(self, query, update_data):
        """
        Queries for and updates document(s) within the collection.
        Input: query -> key/value lookup dictionary.
               update_data -> a dictionary containing MongoDB update operators (e.g., {'$set': {...}}).
        Return: The total number of objects modified in the collection.
        """
        if isinstance(query, dict) and isinstance(update_data, dict):
            try:
                result = self.collection.update_many(query, update_data)
                return result.modified_count
            except Exception as e:
                print(f"An error occurred during update: {e}")
                return 0
        else:
            raise ValueError("Both query and update_data must be dictionaries")

    def delete(self, query):
        """
        Queries for and removes document(s) from the collection.
        Input: key/value lookup dictionary.
        Return: The total number of objects removed from the collection.
        """
        if isinstance(query, dict):
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"An error occurred during deletion: {e}")
                return 0
        else:
            raise ValueError("Query parameters must be a dictionary")