"""
This file holds the transformers used to serialize and de-serialize between a SessionState python class and a json blob.
Used between calls to the lambda function within a session and used for external storage persistence.
"""

import jsonpickle
import json
from session import *

# ------------------- Converting from json to session_state itself ------------------


def session_to_json_string(session):
    """Must convert from the Session class to the SessionState class, then serialized to json for storage.

    :param session: a PrettySession object to convert to SessionState
    :return: json of the session_state to store
    """
    print("converting Session to SessionState")
    session_state = session.get_session_state()
    print("serializing SessionState to json")
    return json.loads(jsonpickle.encode(session_state))


def json_string_to_session(session_state_json):
    """Must convert from json to SessionState to Session

    :param session_state_json: json to deserialize
    :return: a Session object that houses the players session
    """
    print("deserializing session state to json")
    session_state_json = json.dumps(session_state_json)
    print("deserializing session state json to session_state")
    session_state = jsonpickle.decode(session_state_json)
    print("running schema converter on session state")
    session_state = session_state_schema_converter(session_state)
    print("converting SessionState to Session")
    return Session(session_state)


def session_state_schema_converter(session_state):
    """
    Given a session state, will convert between older versions to newer version if required. This should only be
    necessary for non-backwards-compatible changes to the session state schema.

    :param session_state: The state to convert
    :return: The converted state
    """
    return session_state