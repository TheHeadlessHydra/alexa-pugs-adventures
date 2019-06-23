"""
Storage factory. This class will take the storage_layer_class variable and use reflection to build the appropriate
storage class. All implementation of the storage interface need to be imported into this class for it to be able to
properly reflect.
"""
from storage_dynamo import *


def get_storage_layer(storage_layer_class):
    print("Converting " + storage_layer_class + " to storage class")
    class_lookup = {'class_name': storage_layer_class}
    storage_layer = globals()[storage_layer_class]()
    if storage_layer is None:
        raise Exception("Could not find implementation of storage layer: " + str(storage_layer_class))
    else:
        return storage_layer
