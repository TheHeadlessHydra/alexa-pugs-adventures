"""
All helper methods to interact with the Alexa JSON object model.
"""

# --------------- Special input types ------------------
from session_state_builder import *
from storage_factory import *
from session_state_builder import *
import uuid

INITIALIZE = "Initialize"
RETURN = "Return"

# --------------- Amazon intents ------------------

SESSION_ENDED = "SessionEndedRequest"
LAUNCH_REQUEST = "LaunchRequest"
STOP_INTENT = "StopIntent"
CANCEL_INTENT = "CancelIntent"
HELP_INTENT = "HelpIntent"

# --------------- Generic intents that can be used in any situation ------------------
COMMON_OPTIONS_MENU = "CommonOpenSettingsMenu"
COMMON_RESTART_GAME = "CommonRestartGameFromScratch"
COMMON_RESUME = "CommonReturnToGame"
COMMON_DESCRIBE_INVENTORY = "CommonDescribeInventory"
COMMON_GO_LEFT = "CommonGoLeft"
COMMON_GO_RIGHT = "CommonGoRight"
COMMON_GO_BACK = "CommonGoBack"
COMMON_GO_FORWARD = "CommonGoForward"
COMMON_TAKE_BOOTS = "CommonTakeBoots"
COMMON_DESCRIBE_AREA_AGAIN = "CommonDescribeAreaAgain"
COMMON_EXIT_THE_ROOM = "CommonExitTheRoom"
COMMON_PRESS_BUTTON = "CommonPushButton"
COMMON_OPEN_THE_DOOR = "CommonOpenTheDoor"
COMMON_READ_THE_PAMPHLET = "CommonReadThePamphlet"
COMMON_LOOK_AT_STATUE = "CommonLookAtStatue"
COMMON_WALK_TO_FOUNTAIN = "CommonInspectFountain"
COMMON_LOOK_IN_ROOM = "CommonLookInsideRoom"
COMMON_GO_NORTH = "CommonGoNorth"
COMMON_GO_EAST = "CommonGoEast"
COMMON_GO_SOUTH = "CommonGoSouth"
COMMON_GO_WEST = "CommonGoWest"

# --------------- Goblin Town ------------------
GOBLIN_TOWN_GO_BACK_TO_TOWN = "GoblinTownGoToTownCenter"
GOBLIN_TOWN_GO_TO_MINES = "GoblinTownGoToMines"
GOBLIN_TOWN_GO_TO_CHOW_HALL = "GoblinTownGoToChowHall"
GOBLIN_TOWN_GO_TO_PUGS_HOME = "GoblinTownGoToPugsHouse"
GOBLIN_TOWN_GO_TO_TRADING_POST = "GoblinTownGoToTradingPost"

# --------------- Goblin Town Pugs House ------------------
GOBLIN_TOWN_HOUSE_INSPECT_BED = "GoblinTownHomeInspectBed"
GOBLIN_TOWN_INSPECT_HOME = "GoblinTownHomeInspectHome"

# --------------- Goblin Town Mine ------------------
GOBLIN_TOWN_MINES_BREAK_ROCKS = "GoblinTownMinesBreakRocks"
GOBLIN_TOWN_MINES_USE_PICKAXE = "GoblinTownMinesUsePickaxe"
GOBLIN_TOWN_MINES_GO_THROUGH_HOLE = "GoblinTownMinesGoThroughHole"

# --------------- Goblin Town Chow Hall ------------------
GOBLIN_TOWN_CHOW_HALL_TALK_TO_GRUGG = "GoblinTownChowHallTalkToGrugg"
GOBLIN_TOWN_CHOW_HALL_EAT_WITH_GRUGG = "GoblinTownChowHallEatWithGrugg"
GOBLIN_TOWN_CHOW_HALL_READ_MENU = "GoblinTownChowHallReadMenu"
GOBLIN_TOWN_CHOW_HALL_BUY_STEAK = "GoblinTownChowHallBuySteakTarTar"
GOBLIN_TOWN_CHOW_HALL_BUY_ROCK_JELLY = "GoblinTownChowHallBuyRockJelly"
GOBLIN_TOWN_CHOW_HALL_BUY_SOUP = "GoblinTownChowHallBuySoup"
GOBLIN_TOWN_CHOW_HALL_LEAVE = "GoblinTownChowHallLeaveTheHall"

# --------------- Goblin Town Trading Post ------------------
GOBLIN_TOWN_TRADER_INSPECT_PICKAXE = "GoblinTownTraderInspectPickaxe"
GOBLIN_TOWN_TRADER_INSPECT_KEY = "GoblinTownTraderInspectMasterKey"
GOBLIN_TOWN_TRADER_INSPECT_FRESHENER = "GoblinTownTraderInspectAirFreshener"
GOBLIN_TOWN_TRADER_SELL_BOOTS = "GoblinTownTraderSellBoots"
GOBLIN_TOWN_TRADER_BUY_PICKAXE = "GoblinTownTraderBuyPickaxe"
GOBLIN_TOWN_TRADER_BUY_KEY = "GoblinTownTradeBuyMasterKey"
GOBLIN_TOWN_TRADER_BUY_FRESHENER = "GoblinTownTraderBuyFreshener"

# --------------- Aquarium Visitor Center ------------------
VISITOR_CENTER_GO_BACK = "VisitorCenterGoBack"
VISITOR_CENTER_GOTO_LOST_AND_FOUND = "VisitorCenterGoToLostAndFound"
VISITOR_CENTER_GOTO_LOST_PIRANHA_PARADISE = "VisitorCenterGoToPiranhaParadise"
VISITOR_CENTER_TALK_TO_GOBLIN = "VisitorCenterTalkToGoblin"

# --------------- Aquarium Lost and Found Corpses ------------------

LOST_AND_FOUND_LOOK_AT_OTHER_BODIES = "LostAndFoundLookAtOtherBodies"

LOST_AND_FOUND_INSPECT_RANGER = "LostAndFoundInspectRanger"
LOST_AND_FOUND_TAKE_FISH = "LostAndFoundTakeFish"
LOST_AND_FOUND_TAKE_BOW = "LostAndFoundTakeBow"

LOST_AND_FOUND_INSPECT_DRUID = "LostAndFoundInspectDruid"
LOST_AND_FOUND_TAKE_SATCHEL = "LostAndFoundTakeSatchel"
LOST_AND_FOUND_TAKE_KALE = "LostAndFoundTakeKale"
LOST_AND_FOUND_EAT_KALE = "LostAndFoundEatKale"

# --------------- Aquarium Piranha Paradise Aquarium ------------------
AQUARIUM_GO_TO_MAINTENANCE_ROOM = "AquariumGoToMaintenanceRoom"
AQUARIUM_GO_UP_LADDER = "AquariumGoUpLadder"

AQUARIUM_INSPECT_THE_LIGHT = "AquariumInspectTheLight"
AQUARIUM_CUT_THE_LIGHT = "AquariumCutTheLight"
AQUARIUM_CHARM_PIRANHAS = "AquariumCharmPiranhas"
AQUARIUM_GO_DOWN_LADDER = "AquariumGoDownLadder"
AQUARIUM_GO_BACK = "AquariumGoBack"
AQUARIUM_ENTER_WATER = "AquariumEnterWater"

# --------------- Aquarium Maintenance Room ------------------

MAINTENANCE_TAKE_CHUM = "MaintenanceTakeChum"
MAINTENANCE_GO_TO_SWITCHBOARD = "MaintenanceGoToSwitchboard"

SWITCHBOARD_PULL_LEVER_ONE = "SwitchboardPullLeverOne"
SWITCHBOARD_PULL_LEVER_TWO = "SwitchboardPullLeverTwo"
SWITCHBOARD_PULL_LEVER_THREE = "SwitchboardPullLeverThree"
SWITCHBOARD_PUSH_BUTTON = "SwitchboardPushButton"
SWITCHBOARD_CAMERA_CONTROLS = "SwitchboardCameraControls"
SWITCHBOARD_PUSH_SCREAM_BUTTON = "SwitchboardPushScreamButton"
SWITCHBOARD_CHECK_LIGHTS = "MaintenanceRoomLookAtLights"

# --------------- Keeper Trapper Commons ------------------
KEEPER_TRAPPER_GO_TO_RECEPTION = "KeeperTrapperGoToReception"
KEEPER_TRAPPER_GO_TO_RNDND = "KeeperTrapperGoToRndnd"
KEEPER_TRAPPER_GO_TO_BOARDROOM = "KeeperTrapperGoToBoardRoom"
KEEPER_TRAPPER_GO_THROUGH_GOLDEN_DOOR = "KeeperTrapperGoToGoldenDoor"
KEEPER_TRAPPER_GO_TO_NET_ROOM = "KeeperTrapperGoToNetRoom"
KEEPER_TRAPPER_DRINK_COFFEE = "KeeperTrapperDrinkCoffee"
KEEPER_TRAPPER_READ_ENVELOPE = "KeeperTrapperReadEnvelope"
KEEPER_TRAPPER_OPEN_ENVELOPE = "KeeperTrapperUseLetterOpenerOnEnvelope"
KEEPER_TRAPPER_USE_OPENER = "KeeperTrapperUseLetterOpener"

# --------------- Keeper Trapper Washroom ------------------
KEEPER_TRAPPER_WASHROOM_LEAVE_WASHROOM = "KeeperTrapperWashroomLeaveWashroom"
KEEPER_TRAPPER_WASHROOM_INSPECT_FAUCET = "KeeperTrapperWashroomInspectFaucet"
KEEPER_TRAPPER_WASHROOM_TAKE_FAUCET = "KeeperTrapperWashroomTakeFaucet"
KEEPER_TRAPPER_WASHROOM_INSPECT_PLUMBER = "KeeperTrapperWashroomInspectPlumber"
KEEPER_TRAPPER_WASHROOM_INSPECT_TOOLBELT = "KeeperTrapperWashroomInspectToolbelt"
KEEPER_TRAPPER_WASHROOM_TAKE_WRENCH = "KeeperTrapperWashroomTakeTheWrench"
KEEPER_TRAPPER_WASHROOM_INSPECT_TOILET = "KeeperTrapperWashroomInspectToilet"
KEEPER_TRAPPER_WASHROOM_CLOG_TOILET = "KeeperTrapperWashroomClogToilet"
KEEPER_TRAPPER_WASHROOM_GOO_IN_TOILET = "KeeperTrapperWashroomPutGooInToilet"
KEEPER_TRAPPER_WASHROOM_FLUSH_TOILET = "KeeperTrapperWashroomFlushToilet"

# --------------- Keeper Trapper Reception ------------------
KEEPER_TRAPPER_RECEPTION_TALK_TO_SECRETARY = "KeeperTrapperReceptionTalkToSecretary"
KEEPER_TRAPPER_RECEPTION_TELL_SECRETARY_TOILET = "KeeperTrapperReceptionTellHerAboutOverflow"
KEEPER_TRAPPER_RECEPTION_STONE_FRUIT = "KeeperTrapperReceptionLookAtFruit"
KEEPER_TRAPPER_RECEPTION_TAKE_FRUIT = "KeeperTrapperReceptionTakeFruit"
KEEPER_TRAPPER_RECEPTION_TAKE_APPLE = "KeeperTrapperReceptionTakeApple"
KEEPER_TRAPPER_RECEPTION_TAKE_BANANA = "KepperTrapperReceptionTakeBanana"
KEEPER_TRAPPER_RECEPTION_TAKE_BERRIES = "KeeperTrapperTakeBerries"
KEEPER_TRAPPER_RECEPTION_TAKE_SEED = "KeeperTrapperReceptionTakeSeed"
KEEPER_TRAPPER_RECEPTION_TO_WASHROOM = "KeeperTrapperReceptionGoToWashroom"

# --------------- Keeper Trapper Boardroom ------------------
KEEPER_TRAPPER_BOARDROOM_TALK_TO_OGRE = "KeeperTrapperBoardroomTalkToOgre"
KEEPER_TRAPPER_BOARDROOM_GIVE_COFFEE = "KeeperTrapperBoardroomGiveCoffee"

# --------------- Keeper Trapper RnDnD ------------------
KEEPER_TRAPPER_RNDND_INSPECT_WORKSTATION = "KeeperTrapperRndndInspectWorkstation"
KEEPER_TRAPPER_RNDND_TRAP_BEAR = "KeeperTrapperRndndBearRoom"
KEEPER_TRAPPER_RNDND_INSPECT_MACHINE = "KeeperTrapperRndndInspectMachine"
KEEPER_TRAPPER_RNDND_PRESS_BUTTON = "KeeperTrapperRndndPushButton"
KEEPER_TRAPPER_RNDND_GIVE_WATER = "KeeperTrapperRndndGiveWater"
KEEPER_TRAPPER_RNDND_TALK_TO_CAFFINOX = "KeeperTrapperRndndTalkToCaffinox"

# --------------- Keeper Trapper Workstation ------------------
KEEPER_TRAPPER_WORKSTATION_TAKE_GOO = "KeeperTrapperWorkstationTakeGoo"
KEEPER_TRAPPER_WORKSTATION_TAKE_ENVELOPE = "KeeperTrapperWorkstationTakeEnvelope"
KEEPER_TRAPPER_WORKSTATION_INSPECT_BLUEPRINT = "KeeperTrapperWorkstationLookAtBlueprint"
KEEPER_TRAPPER_TAKE_BLUEPRINT = "KeeperTrapperWorkstationTakeBlueprint"

# --------------- Keeper Trapper Net Room ------------------
KEEPER_TRAPPER_NET_ROOM_TALK_TO_ELF = "KeeperTrapperNetTalkToElf"
KEEPER_TRAPPER_NET_ROOM_ASK_FOR_THEY_KEY = "KeeperTrapperNetAskForKey"
KEEPER_TRAPPER_NET_ROOM_FAUCET_FOR_KEY = "KeeperTrapperNetTradeFaucet"
KEEPER_TRAPPER_NET_ROOM_CUT_DOWN_ELF_WITH_OPENER = "KeeperTrapperNetCutElfWithOpener"
KEEPER_TRAPPER_NET_ROOM_FREE_ELF = "KeeperTrapperNetCutElfDown"
KEEPER_TRAPPER_NET_ROOM_TAKE_KEY = "KeeperTrapperNetTakeKey"

# --------------- Keeper Trapper CEOs Room ------------------
KEEPER_TRAPPER_CEO_OPEN_RAGMUFFIN = "KeeperTrapperCeoOpenRagmuffin"
KEEPER_TRAPPER_CEO_CLOSE_RAGMUFFIN = "KeeperTrapperCeoCloseRagmuffin"
KEEPER_TRAPPER_CEO_GO_TO_DESK = "KeeperTrapperCeoGoToDesk"
KEEPER_TRAPPER_TAKE_PAMPHLET = "KeeperTrapperCeoReadTakePamphlet"
KEEPER_TRAPPER_TAKE_LETTER_OPENER = "KeeperTrapperCeoTakeLetterOpener"
KEEPER_TRAPPER_TAKE_PITCHER = "KeeperTrapperCeoTakePitcher"
KEEPER_TRAPPER_PLACE_PITCHER_BACK = "KeeperTrapperCeoPlacePitcher"
KEEPER_TRAPPER_CEO_GO_TO_SILVER_DOOR = "KeeperTrapperCeoGoToSilverDoor"
KEEPER_TRAPPER_CEO_THROUGH_SILVER_DOORS = "KeeperTrapperCeoEnterSilverDoors"
KEEPER_TRAPPER_LOOK_INSIDE_SILVER_DOORS = "KeeperTrapperCeoDescribeInsideSilverDoor"
KEEPER_TRAPPER_CEO_THROW_LETTER_OPENER_AT_TRAP = "KeeperTrapperCeoThrowLetterOpener"
KEEPER_TRAPPER_USE_PITCHER_ON_TRAP = "KeeperTrapperCeoUsePitcherOnTrap"

KEEPER_TRAPPER_CEO_GO_TO_GARDEN = "KeeperTrapperCeoInspectGarden"
KEEPER_TRAPPER_CEO_WATER_GARDEN = "KeeperTrapperCeoWaterGarden"
KEEPER_TRAPPER_PLANT_SEED = "KeeperTrapperCeoPlantSeed"

KEEPER_TRAPPER_ELEVATOR_PRESS_BUTTON = "KeeperTrapperElevatorPressButton"
KEEPER_TRAPPER_ELEVATOR_LEAVE = "KeeperTrapperElevatorLeave"


# --------------- StoredAttrbitues ------------------

STORED_NEXT_STATE = "next_state"


# --------------- helpers for the game ------------------

def save_game(session):
    storage = get_storage_layer(Config.storage_layer)
    session_string = session_to_json_string(session)
    storage.write_json_string(session.get_user_id_serializable(), session_string)

# --------------- builders ------------------


def get_action_response(session, card_title, speech_output, reprompt_text, should_end_session, buy_product_id=None,
                        cancel_product_id=None):
    session_state_json = session_to_json_string(session)
    return build_response(session_state_json, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, buy_product_id, cancel_product_id))


def build_speechlet_response(title,
                             output,
                             reprompt_text,
                             should_end_session,
                             buy_product_id=None, cancel_product_id=None):
    output_json = {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    if buy_product_id is not None:
        output_json['directives'] = [
            {
                "type": "Connections.SendRequest",
                "name": "Buy",
                "payload": {
                    "InSkillProduct": {
                        "productId": buy_product_id
                    }
                },
                "token": "correlationToken"
            }
        ]
    if cancel_product_id is not None:
        output_json['directives'] = [
            {
                "type": "Connections.SendRequest",
                "name": "Cancel",
                "payload": {
                    "InSkillProduct": {
                        "productId": cancel_product_id
                    }
                },
                "token": "correlationToken"
            }
        ]
    return output_json


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def add_upsell_to_output(output_json, upsell_product_id, upsell_message):
    output_json['response']['shouldEndSession'] = True
    output_json['response']['directives'] = [
        {
            "type": "Connections.SendRequest",
            "name": "Upsell",
            "payload": {
                "InSkillProduct": {
                    "productId": upsell_product_id
                },
                "upsellMessage": upsell_message
            },
            "token": str(uuid.uuid1())
        }
    ]
    return output_json


class ValidationException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ValidationException, self).__init__(message)


# --------------- Helper methods ------------------

def wrap_with_speak(*arg):
    full_final_string = "<speak>"
    for a in arg:
        full_final_string = full_final_string + a
    full_final_string = full_final_string + "</speak>"
    return full_final_string

def wrap_with_audio(text):
    return "<audio src='" + text + "'/>"
