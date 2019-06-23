"""
This is the schema of the state of a player.
This is passed along between sessions and stored in an external persistence layer between calls.

It is very important to be careful when changing anything in this schema. The state is stored externally in DynamoDB.
It is highly likely that production code will break if non-backwards-compatible changes are made. Therefore, make sure
everything that is changed is backwards compatible. If you need to make a non-backwards compatible change,
session_state_builder has a method for handling non-backwards-compatible changes called session_state_schema_converter.

The serialize and deserialize methods will optimize the writes of each individual object in the state.
If changes need to be made to the schema, the serialize and deserialize methods need to be changed to reflect the changes.
Make sure to compact and compress the final result as best as possible to save on storage costs. This is the reason we
do not simple pickle the entire Session object.
"""

from config import *
from world import *
from events import *


class Session(object):
    def __init__(self, session_state):
        self.user_id = self.set_user_id_deserialize(session_state)
        self.seen_location_before = self.set_seen_location_before_deserialize(session_state)
        self.stored_game_state = self.set_stored_game_state_deserialize(session_state)
        self.previous_game_state = self.set_previous_stored_game_state_deserialize(session_state)
        self.item_inventory = self.set_item_inventory_deserialize(session_state)
        self.event_inventory = self.set_event_inventory_deserialize(session_state)

        # Decorators used throughout the code but not commited to session state
        self.is_keeper_trapper_purchased = None
        self.is_keeper_trapper_purchasable = None

    # -------------------- SessionState builder --------------------
    def get_session_state(self):
        session_state = SessionState(self.get_user_id_serializable())
        session_state.stored_game_state = self.get_stored_game_state_serializable()
        session_state.previous_game_state = self.get_previous_stored_game_state_serializable()
        session_state.seen_location_before = self.get_seen_location_before_serializable()
        session_state.events = self.get_event_inventory_serializable()
        session_state.inventory = self.get_item_inventory_serializable()
        return session_state

    # -------------------- user id --------------------
    def get_user_id_serializable(self):
        return self.user_id

    def set_user_id_deserialize(self, session_state):
        return session_state.user_id

    # -------------------- seen locations --------------------
    def is_location_seen_before(self, seen_location):
        return seen_location in self.seen_location_before

    def get_seen_location_before_serializable(self):
        seen_location_before = []
        for location in self.seen_location_before:
            seen_location_before.append(location)
        return seen_location_before

    def set_seen_location_before_deserialize(self, session_state):
        seen_location_before = Set()
        for location in session_state.seen_location_before:
            seen_location_before.add(location)
        return seen_location_before

    def new_seen_location(self, seen_location):
        self.seen_location_before.add(seen_location)

    # -------------------- game state --------------------
    def get_stored_game_state(self):
        return self.stored_game_state

    def set_stored_game_state(self, stored_game_state):
        self.stored_game_state = stored_game_state

    def get_stored_game_state_serializable(self):
        return self.stored_game_state

    def set_stored_game_state_deserialize(self, session_state):
        return session_state.stored_game_state

    # -------------------- previous game state --------------------
    def get_previous_stored_game_state(self):
        return self.previous_game_state

    def set_previous_stored_game_state(self, previous_game_state):
        self.previous_game_state = previous_game_state

    def get_previous_stored_game_state_serializable(self):
        return self.previous_game_state

    def set_previous_stored_game_state_deserialize(self, session_state):
        return session_state.previous_game_state

    # -------------------- inventory --------------------
    def get_item_inventory(self):
        return self.item_inventory

    def get_item_inventory_serializable(self):
        session_inventory = []
        for item in self.item_inventory.get_items():
            session_inventory.append((item.get_item_id(), item.get_usage()))
        return session_inventory

    def set_item_inventory_deserialize(self, session_state):
        inventory = ItemInventory()
        for tuple in session_state.inventory:
            inventory.add(tuple[0], tuple[1])
        return inventory

    # -------------------- events --------------------
    def get_event_inventory(self):
        return self.event_inventory

    def get_event_inventory_serializable(self):
        event_inventory = []
        for event in self.event_inventory.get_events():
            event_inventory.append(event)
        return event_inventory

    def set_event_inventory_deserialize(self, session_state):
        event_inventory = EventInventory()
        for event_state in session_state.events:
            event_inventory.add(event_state)
        return event_inventory

    # -------------------- decorators --------------------
    def get_is_keeper_trapper_purchased(self):
        return self.is_keeper_trapper_purchased

    def get_is_keeper_trapper_purchasable(self):
        return self.is_keeper_trapper_purchasable

    def set_is_keeper_trapper_purchased(self, is_keeper_trapper_purchased):
        self.is_keeper_trapper_purchased = is_keeper_trapper_purchased

    def set_is_keeper_trapper_purchasable(self, is_keeper_trapper_purchasable):
        self.is_keeper_trapper_purchasable = is_keeper_trapper_purchasable

    def restart_session(self):
        self.seen_location_before.clear()
        self.stored_game_state = None
        self.previous_game_state = None
        self.item_inventory.clear()
        self.event_inventory.clear()


class SessionState(object):
    """The object that gets serialized and deserialized to storage. It has been stripped down to its bare essentials
    to save on storage costs. The serialize and deserialize methods above handle the conversion from the storage
    format to the Session object.
    """

    def __init__(self, user_id):
        self.user_id = user_id

        # Where the player is, indicated by the ClassName of the state in the StateMachine.
        self.stored_game_state = None

        # Where the player was last, indicated by the ClassName of the state in the StateMachine.
        self.previous_game_state = None

        # A basic array that holds ClassNames. Each class indicates a specific state that the player can be in. If the
        # ClassName exists in the array, then the player has been there before.
        self.seen_location_before = []

        # All events that could have happened for the player that effect the world.
        self.events = []

        # The inventory of the player.
        self.inventory = []

        # The version of this schema
        self.version = Config.session_state_version
