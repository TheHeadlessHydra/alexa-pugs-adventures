"""
The DynamoDB implementation of the storage interface. It uses dynamodb as a simple key value store. The hash key
is the user_id and the session itself is stored as a json blob in the table.

This class uses the pynamodb library to model and interact with the dynamodb table.

The configurations for this class are stored in config.py
"""
from config import *
from storage import *
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, JSONAttribute
)


class DynamoSession(Model):
    class Meta:
        table_name = Config.table_name
        region = Config.region

    user_id = UnicodeAttribute(hash_key=True)
    session = JSONAttribute()


class DynamoStorage(Storage):
    def write_json_string(self, id, json_string):
        print("Writing id to dynamo: " + str(id) + ", with json blob: " + str(json_string))
        dynamo_session_item = DynamoSession(id, session=json_string)
        dynamo_session_item.save()

    def get_json_string(self, id):
        """Will get the stored session state json blob from dynamo.

        :param user_id: The user id of the session state to get
        :return: session_state json blob if user id exists, or None if user id does not exist
        """
        print "Searching for session for user with user_id: " + str(id)
        json_string = None
        count = 0
        for dynamo_item in DynamoSession.query(id):
            json_string = dynamo_item.session
            count = count + 1

        if count == 0:
            return None
        elif count == 1:
            return json_string
        else:
            raise Exception("Found more than one entry for a user in the table. Failing.")

    def delete_item(self, id):
        print("Deleting id from dynamo: " + str(id))
        DynamoSession.delete(DynamoSession())
        DynamoSession.delete(self, id)