"""
The entire world of events that can happen to a player that effects the game state.

It is very important to be careful when changing anything in this schema. The state is stored externally in DynamoDB.
It is highly likely that production code will break if non-backwards-compatible changes are made. Therefore, make sure
everything that is changed is backwards compatible. If you need to make a non-backwards compatible change,
session_state_builder has a method for handling non-backwards-compatible changes called session_state_schema_converter.

"""
from sets import Set

class Events(object):
    # --------------------------- Common ------------------------------#
    common_describe_inventory_once = 100
    common_restart_the_game_are_you_sure = 101

    # --------------------------- Goblin Town ------------------------------#
    goblin_town_go_through_rocks = 50
    goblin_town_break_rocks = 51
    goblin_town_sell_boots = 52
    goblin_town_seen_pickaxe = 53
    goblin_town_seen_key = 53
    goblin_town_seen_freshener = 53
    goblin_town_talked_to_grugg = 54
    goblin_town_eat_soup = 55
    goblin_town_inspect_pugs_house = 56
    goblin_town_eat_rock_jelly = 57

    # --------------------------- Aquarium ------------------------------#
    attempted_to_take_bow = 1
    druid_look_at_satchel = 2
    attempted_to_eat_kale = 3
    piranhas_all_gone = 4

    aquarium_maintenance_room_light1_on = 200
    aquarium_maintenance_room_light2_on = 201
    aquarium_maintenance_room_light3_on = 202

    # --------------------------- Keeper Trapper ------------------------------#

    keeper_trapper_talked_to_secretary = 5
    keeper_trapper_overflowing_toilet = 6
    keeper_trapper_plumber_in_washroom = 7
    keeper_trapper_faucet_removed = 8
    keeper_trapper_take_berries = 9
    keeper_trapper_talk_to_ogres = 10
    keeper_trapper_give_ogre_coffee = 11
    keeper_trapper_seen_coffee_carnage = 12
    keeper_trapper_water_zen_garden = 13
    keeper_trapper_place_seed_zen_garden = 14
    keeper_trapper_sprout_seed_zen_garden = 15
    keeper_trapper_looked_at_blueprints = 16
    keeper_trapper_silver_door_open = 17
    keeper_trapper_pitcher_in_trap_room = 18
    keeper_trapper_trap_broken = 19
    keeper_trapper_opened_elevator_after_trap_broken = 20
    keeper_trapper_opened_trap_bear_door = 21
    keeper_trapper_looked_at_strange_machine = 22
    keeper_trapper_strange_machine_tried_pushing_button = 23
    keeper_trapper_given_strange_machine_water = 24
    keeper_trapper_caffenox_lives = 25
    keeper_trapper_talk_to_elf_part_one = 26
    keeper_trapper_seen_fountain = 27
    keeper_trapper_seen_desk = 28
    keeper_trapper_place_goo_in_toilet = 29
    keeper_trapper_free_elf = 30
    keeper_trapper_open_envelope = 31

class EventInventory(object):
    """
    A class that holds the players inventory
    """
    def __init__(self):
        self.inventory = Set()

    def add(self, event_id):
        self.inventory.add(event_id)

    def remove(self, event_id):
        if event_id in self.inventory:
            self.inventory.remove(event_id)

    def get_events(self):
        return self.inventory

    def exists(self, event_id):
        return event_id in self.inventory

    def clear(self):
        self.inventory.clear()