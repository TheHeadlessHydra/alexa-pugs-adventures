"""
Base class for the storage layer. 
"""

class Storage(object):
    def write_json_string(self, id, json_string):
        assert 0, "write not implemented"

    def get_json_string(self, id):
        assert 0, "get not implemented"

    def delete_item(self, id):
        assert 0, "delete not implemented"
