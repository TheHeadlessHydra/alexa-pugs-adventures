"""
The entire world of items in the game that can be placed in a users inventory.

It is very important to be careful when changing anything in this schema. The state is stored externally in DynamoDB.
It is highly likely that production code will break if non-backwards-compatible changes are made. Therefore, make sure
everything that is changed is backwards compatible. If you need to make a non-backwards compatible change,
session_state_builder has a method for handling non-backwards-compatible changes called session_state_schema_converter.
"""

from session import *

# ------------------- Item IDs of the world ------------------
class World(object):
    # --------------------------- Aquarium ------------------------------#
    ranger_stiff_fish = 1
    druid_kale_snack = 2
    charm_animal_scroll = 3
    maintenance_room_key = 4

    # --------------------------- Keeper Trapper ------------------------------#
    keeper_trapper_eldritch_wrench = 6
    keeper_trapper_seed = 7
    keeper_trapper_golden_door_key = 8
    keeper_trapper_coffee = 9
    keeper_trapper_envelope = 10
    keeper_trapper_goo = 11
    keeper_trapper_letter_opener = 12
    keeper_trapper_everlasting_pitcher = 13
    keeper_trapper_faucet = 14
    keeper_trapper_elven_boot = 15

    # --------------------------- Goblin Town ------------------------------#
    goblin_town_various_boots = 50
    goblin_town_pickaxe = 51
    goblin_town_freshener = 52



class Item(object):
    """
    A pretty class that holds extra information about an item that is not needed for storage. These get decorated via
    the code below.
    """
    def __init__(self, item_id):
        self.item_id = item_id
        self.been_used = False
        self.pretty_name = get_name_of_item(item_id)
        self.pretty_description = get_description_of_item(item_id)

    def get_item_id(self):
        return self.item_id

    def get_usage(self):
        return self.been_used

    def get_pretty_name(self):
        return self.pretty_name

    def get_pretty_description(self):
        return self.pretty_description

    def mark_as_used(self):
        self.been_used = True

    def is_item_already_used(self):
        return self.been_used

class ItemInventory(object):
    """
    A class that holds the players inventory
    """
    def __init__(self):
        self.inventory = dict()

    def add(self, item_id, been_used = False):
        if item_id in self.inventory:
            return
        new_item = Item(item_id)
        if been_used:
            new_item.mark_as_used()
        self.inventory[item_id] = new_item

    def size(self):
        return len(self.inventory)

    def get(self, item_id):
        return self.inventory.get(item_id)

    def get_items(self):
        return self.inventory.values()

    def exists(self, item_id):
        return item_id in self.inventory

    def mark_item_as_used(self, item_id):
        if self.inventory.has_key(item_id):
            self.inventory[item_id].mark_as_used()

    def is_item_already_used(self, item_id):
        if self.inventory.has_key(item_id):
            return self.inventory[item_id].is_item_already_used()
        else:
            return False

    def clear(self):
        self.inventory.clear()

# ------------------- Mappings to add decorations to items that are not needed for storage ------------------

def get_name_of_item(item_id):
    if item_id == World.ranger_stiff_fish:
        return "Stiff sword fish"
    elif item_id == World.druid_kale_snack:
        return "Kale snack bar"
    elif item_id == World.charm_animal_scroll:
        return "Charm animal scroll"
    elif item_id == World.maintenance_room_key:
        return "Maintenance room key"
    elif item_id == World.keeper_trapper_eldritch_wrench:
        return "Eldritch wrench"
    elif item_id == World.keeper_trapper_seed:
        return "A stone seed"
    elif item_id == World.keeper_trapper_golden_door_key:
        return "A Golden key"
    elif item_id == World.keeper_trapper_coffee:
        return "Fragrant cup of coffee"
    elif item_id == World.keeper_trapper_envelope:
        return "Rune emblazoned envelope"
    elif item_id == World.keeper_trapper_goo:
        return "Super goo"
    elif item_id == World.keeper_trapper_letter_opener:
        return "Letter opener plus 1"
    elif item_id == World.keeper_trapper_everlasting_pitcher:
        return "Everlasting pitcher"
    elif item_id == World.keeper_trapper_faucet:
        return "Golden faucet"
    elif item_id == World.keeper_trapper_elven_boot:
        return "Fine elven boot"
    elif item_id == World.goblin_town_various_boots:
        return "Collection of boots"
    elif item_id == World.goblin_town_pickaxe:
        return "Pink pickaxe"
    elif item_id == World.goblin_town_freshener:
        return "Air freshener of Foreshadowing"
    else:
        return "Whoops. We forgot to name this ite: " + str(item_id)

def get_description_of_item(item_id):
    if item_id == World.ranger_stiff_fish:
        return "A very long fish with rigor mortis set in."
    elif item_id == World.druid_kale_snack:
        return "A dead druid's disgusting kale snack bar."
    elif item_id == World.charm_animal_scroll:
        return "A magical scroll to charm an animal."
    elif item_id == World.maintenance_room_key:
        return "A key marked maintenance."
    elif item_id == World.keeper_trapper_eldritch_wrench:
        return "A magical wrench stolen from the magical plumber."
    elif item_id == World.keeper_trapper_seed:
        return "Obtained from the statue in the lobby of KEEPER TRAPPER LLC."
    elif item_id == World.keeper_trapper_golden_door_key:
        return "Fit for a golden door."
    elif item_id == World.keeper_trapper_coffee:
        return "It smells wonderfully earthy."
    elif item_id == World.keeper_trapper_envelope:
        return "An envelope with colored runes emblazoned. Using his own strength, Pug cannot open this."
    elif item_id == World.keeper_trapper_goo:
        return "The amazing new toy from KEEPER TRAPPER FOR KIDS! WARNING: Keep away from toilets."
    elif item_id == World.keeper_trapper_letter_opener:
        return "A magical letter opener that can open or cut magically infused objects."
    elif item_id == World.keeper_trapper_everlasting_pitcher:
        return "A pitcher that magically generates water infinitely."
    elif item_id == World.keeper_trapper_faucet:
        return "A fancy golden faucet stolen from the executive washroom."
    elif item_id == World.keeper_trapper_elven_boot:
        return "A wonderfully beautiful boot."
    elif item_id == World.goblin_town_various_boots:
        return "The haul of boots Pug collected on his last day of work."
    elif item_id == World.goblin_town_pickaxe:
        return "Used for smashing rocks."
    elif item_id == World.goblin_town_freshener:
        return "This air freshener drips with foreshadowing of the future of this game."
    else:
        return "Whoops. We forgot to give this item a description: " + str(item_id)
