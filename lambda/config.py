"""
All configurations for this instance of the labmda function go here.
"""


class Config(object):
    # ------------------- custom configs -------------------
    mad_mage_name = "Kalidar"
    goblin_town_name = "Cragdag"

    # ------------------- custom configs -------------------

    session_state_version = "0.0.2"

    # the storage type to use
    storage_layer = "DynamoStorage"

    # ------------------- dynamodb storage configs -------------------
    table_name = "pugs_adventures_sessions"
    region = "us-east-1"
