"""
State machine for the keeper trapper world.
"""
from state_machine_common import *
from world import *
from events import *
import logging
from state_machine_aquarium import *

logger = logging.getLogger()

# TODO: teach about describing inventory and option menu
class GoblinTownPugsHome(State):
    def next(self, input_action, session):
        overriding_action = super(GoblinTownPugsHome, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Pug's home"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_item_inventory().exists(World.goblin_town_various_boots) \
                and not session.get_event_inventory().exists(Events.common_describe_inventory_once):
            tldr_whats_in_area = "Try describing Pug's inventory. What should Pug do next?"
            detailed_description = "Right now Pug is in his home deep underground. " \
                    "It's a small hut within the Goblin Town of " + Config.goblin_town_name + ". His house is much like all of the " \
                    "other huts in " + Config.goblin_town_name + ". Pug's room has a small bed, and a door that leads out to " + Config.goblin_town_name + ". " \
                    + tldr_whats_in_area
        elif session.get_item_inventory().exists(World.goblin_town_various_boots) \
                and session.get_event_inventory().exists(Events.common_describe_inventory_once):
            tldr_whats_in_area = "Pug can inspect the room, " \
                                 "his own bed or leave through the door. What should Pug do next?"
            detailed_description = "Right now Pug is in his home deep underground. " \
                                   "It's a small hut within the Goblin Town of " + Config.goblin_town_name + ". His house is much like all of the " \
                                   "other huts in " + Config.goblin_town_name + ". Pug's room has a small bed, and a door that leads out to " + Config.goblin_town_name + ". " \
                                   + tldr_whats_in_area
        elif session.get_event_inventory().exists(Events.goblin_town_inspect_pugs_house):
            tldr_whats_in_area = "Try having Pug pick up the boots. What should Pug do next?"
            detailed_description = \
                "A dozen boots litter the floor of Pug's house. In Goblin society, each goblin is given a " \
                "very important task to fulfill. Pug is a De-booter. His job is to remove shoes and boots from " \
                "heroes who have met an unfortunate end in Mad Mage " + Config.mad_mage_name + "'s Dread Lair. The boots scattered here " \
                "are his latest haul. You can have Pug pick up items of interest in this game by simply saying " \
                "pick up followed by the item. Try having Pug pick up the boots. What should Pug do next?"
        else:
            tldr_whats_in_area = "You should start by having Pug inspect his room. So. What should Pug do next?"
            detailed_description = \
                "A dozen boots litter the floor of Pug's house. In Goblin society, each goblin is given a " \
                "very important task to fulfill. Pug is a De-booter. His job is to remove shoes and boots from " \
                "heroes who have met an unfortunate end in Mad Mage " + Config.mad_mage_name + "'s Dread Lair. The boots scattered here " \
                "are his latest haul. You can have Pug pick up items of interest in this game by simply saying " \
                "pick up followed by the item. Try having Pug pick up the boots. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Once upon a time, there lived an evil wizard named Mad Mage " + Config.mad_mage_name + ". "
                + Config.mad_mage_name + " ruled over all "
                "breed of fearsome Dragons, trolls and goblins. Adventurers from across the land entered his "
                "Dread Lair to end his evil ways, but none had ever escaped. However, on a very peculiar Wednesday, "
                "something odd happened. Deep within " + Config.mad_mage_name + "'s lair, one of the wizard's "
                "most uninteresting underlings awoke and realized he no longer wanted to be evil. "
                "This is the story of Pug, the Goblin.<break time=\"1s\"/> "
                "Right now Pug is in his home deep underground. "
                "It's a small hut within the Goblin Town of " + Config.goblin_town_name + ". His house is much like all of the "
                "other huts in town. Pug's room has a small bed, and a door that leads out to " + Config.goblin_town_name + ". "
                "The only other thing of note is the dozen or so boots scattered across his floor. "
                "During this game you'll be following Pug on his journey and be able to give him directions "
                "on what he should do. You should start by having Pug inspect his room. So. What should Pug do next?")
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug enters his home. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN or input_action == GOBLIN_TOWN_INSPECT_HOME:
            speech_output = wrap_with_speak(detailed_description)
            session.get_event_inventory().add(Events.goblin_town_inspect_pugs_house)
        elif input_action == COMMON_TAKE_BOOTS \
                and not session.get_item_inventory().exists(World.goblin_town_various_boots) \
                and session.get_event_inventory().exists(Events.goblin_town_inspect_pugs_house):
            speech_output = \
                wrap_with_speak("Pug gathers up the various shoes, boots, slippers and flip-flops in his room "
                                "and throws them into his satchel. Pug's satchel is magical and can hold an abnormally "
                                "large number of items. You should inspect Pug's inventory next. That will probably "
                                "come in handy. What should Pug do next?")
            session.get_item_inventory().add(World.goblin_town_various_boots)
        elif input_action == GOBLIN_TOWN_HOUSE_INSPECT_BED \
                and session.get_item_inventory().exists(World.goblin_town_various_boots):
            speech_output = wrap_with_speak(
                "Pug looks at his self-proclaimed comfy bed, which, in reality, is closer to a rock than a bed. "
                "Goblin's aren't the brightest creatures in the Dread Lair. They also coincidentally "
                "suffer from bad back problems and insomnia. What should Pug do next?")
        elif (input_action == COMMON_EXIT_THE_ROOM
              or input_action == GOBLIN_TOWN_GO_BACK_TO_TOWN
              or input_action == COMMON_OPEN_THE_DOOR) \
                and session.get_item_inventory().exists(World.goblin_town_various_boots):
            return GoblinTownCenter().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in his home. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class GoblinTownCenter(State):
    def next(self, input_action, session):
        overriding_action = super(GoblinTownCenter, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = Config.goblin_town_name + " Town Center"
        reprompt_text = wrap_with_speak("Where should Pug head next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can go north to the mines, east to go back to Pug's house, south to the " \
                             "Goblin Chow hall, or west to the trading post. Where should Pug head next?"
        detailed_description = "A bustling town " \
                "full of various goblins with even more various tasks to complete throughout the Dread Lair. They " \
                "all end up here at the end of their day. To the north is the closed down mine, which Pug thinks " \
                "could be his ticket out of " + Config.goblin_town_name + ". To the East is the residential district, where Pug's home is " \
                "and where he came from. To the South is is the chow hall where goblins gather to eat. To the " \
                "west is the trading post, used to buy all manner of goods. Where should Pug head next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug walks out of his home and ends up in the familiar " + Config.goblin_town_name + " Town Center. " + detailed_description)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back at the " + Config.goblin_town_name + " town center. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak("Pug is in the " + Config.goblin_town_name + " town Center. " + detailed_description)
        elif input_action == COMMON_GO_NORTH or input_action == GOBLIN_TOWN_GO_TO_MINES:
            return GoblinTownMines().next(RETURN, session)
        elif input_action == COMMON_GO_EAST or input_action == COMMON_GO_BACK \
                or input_action == GOBLIN_TOWN_GO_TO_PUGS_HOME:
            return GoblinTownPugsHome().next(RETURN, session)
        elif input_action == COMMON_GO_SOUTH or input_action == GOBLIN_TOWN_GO_TO_CHOW_HALL:
            return GoblinTownChowHall().next(RETURN, session)
        elif input_action == COMMON_GO_WEST or input_action == GOBLIN_TOWN_GO_TO_TRADING_POST:
            return GoblinTownTradingPost().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in the " + Config.goblin_town_name + " Town Center. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class GoblinTownMines(State):
    def next(self, input_action, session):
        overriding_action = super(GoblinTownMines, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Goblin Rubble and Rock mines"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_event_inventory().exists(Events.goblin_town_break_rocks):
            tldr_whats_in_area = "Pug can crawl through the hole he has made to leave " + Config.goblin_town_name + " or go " \
                                 "back to the town center. What should Pug do next?"
            detailed_description = \
                "Pug is outside Goblin Rubble and Rock Mines, or GRRM for short. " \
                "The GRRM is notorious for years and years of delays without showing much in the way of product. " \
                "Goblins have used this mine over the centuries to get rocks to make beds and other goblin luxuries. " \
                "Unfortunately this mine was filled with useless soft gold and diamonds so it was put out of " \
                "commission after the last cave in. Outside the mine is a sign that reads: " \
                "Mine Closed due to Cave In and Sharks. This is the way that Pug is going to leave the town, " \
                "and he has already created a hole in the rocks to crawl through. What should Pug do next?"
        else:
            tldr_whats_in_area = "Pug can try to break through the rocks or go back. What should Pug do next?"
            detailed_description = \
                "Pug is outside Goblin Rubble and Rock Mines, or GRRM for short. " \
                "The GRRM is notorious for years and years of delays without showing much in the way of product. " \
                "Goblins have used this mine over the centuries to get rocks to make beds and other goblin luxuries. " \
                "Unfortunately this mine was filled with useless soft gold and diamonds so it was put out of " \
                "commission after the last cave in. Outside the mine is a sign that reads: " \
                "Mine Closed due to Cave In and Sharks. This is the way that Pug is going to leave the town, " \
                "so it looks like he's going to need some way to break through the rocks."

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug finds himself outside the Goblin Rubble and Rock Mines, or GRRM for short. "
                "The GRRM is notorious for years and years of delays without showing much in the way of product. "
                "Goblins have used this mine over the centuries to get rocks to make beds and other goblin luxuries. "
                "Unfortunately this mine was filled with useless soft gold and diamonds so it was put out of "
                "commission after the last cave in. Outside the mine is a sign that reads: "
                "Mine Closed due to Cave In and Sharks. This is the way that Pug is going to leave the town, "
                "so it looks like he's going to need some way to break through the rocks. Pug can try to break "
                "through the rocks or head back. What should Pug do next?")
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back at the Goblin Rubble and Rock Mines. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == GOBLIN_TOWN_MINES_BREAK_ROCKS:
            if session.get_event_inventory().exists(Events.goblin_town_go_through_rocks):
                speech_output = wrap_with_speak(
                    "Pug looks at the rocks for a second. He remembers the last time he tried to break the rocks. "
                    "His hands still hurt. He refuses to try it again without using some sort of tool to help him. "
                    "What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug looks at the rocks for a second before beginning to smack them with his fists. He "
                    "very quickly realizes that smacking rocks with his hands is not a particularly efficient way of "
                    "clearing rock debris. He stops. Pug's hands now hurt. Pug is going to need some sort of "
                    "tool to help him clear these rocks. What should Pug do next?")
                session.get_event_inventory().add(Events.goblin_town_go_through_rocks)
        elif input_action == GOBLIN_TOWN_MINES_USE_PICKAXE \
                and session.get_item_inventory().exists(World.goblin_town_pickaxe):
            speech_output = wrap_with_speak("Pug begins smashing rocks with his pickaxe. After several minutes it shatters. "
                                            "So much for Goblin engineering. Luckily, it looks like he's opened up a "
                                            "large enough hole that he can climb through. Pug can now "
                                            "crawl through the hole to finally leave "
                                            "Ikkbutt. What should Pug do next?")
            session.get_item_inventory().mark_item_as_used(World.goblin_town_pickaxe)
            session.get_event_inventory().add(Events.goblin_town_break_rocks)
        elif input_action == GOBLIN_TOWN_MINES_GO_THROUGH_HOLE:
            return PiranhaParadiseVisitorCenter().next(RETURN, session)
        elif input_action == COMMON_GO_BACK or input_action == GOBLIN_TOWN_GO_BACK_TO_TOWN \
                or input_action == COMMON_GO_SOUTH:
            return GoblinTownCenter().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in the Goblin Rubble and Rock Mines. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class GoblinTownTradingPost(State):
    def next(self, input_action, session):
        overriding_action = super(GoblinTownTradingPost, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = Config.goblin_town_name + " Trading Post"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
            tldr_whats_in_area = "There are three items for sale. A pickaxe, a Dread Lair master key, and an Air " \
                                 "Freshener dripping with Foreshadowing. " \
                                 "Pug can inspect these items, sell his boots, buy the items, or go back " \
                                 "to the town center. What should Pug do next?"
        elif session.get_item_inventory().exists(World.goblin_town_pickaxe) \
            and not session.get_item_inventory().exists(World.goblin_town_freshener):
            tldr_whats_in_area = "There are two more items for sale. A Dread Lair master key, and an Air " \
                                 "Freshener dripping with Foreshadowing. " \
                                 "Pug can inspect these items, but the items, or go back " \
                                 "to the town center. What should Pug do next?"
        elif session.get_item_inventory().exists(World.goblin_town_pickaxe) \
            and session.get_item_inventory().exists(World.goblin_town_freshener):
            tldr_whats_in_area = "There is only one item for sale. A Dread Lair master key. " \
                                 "Pug can inspect this item, buy it, or go back " \
                                 "to the town center. What should Pug do next?"
        elif not session.get_item_inventory().exists(World.goblin_town_pickaxe) \
                and session.get_item_inventory().exists(World.goblin_town_freshener):
            tldr_whats_in_area = "There are two more items for sale. A pickaxe, and a Dread Lair master key. " \
                                 "Pug can inspect these items, buy the items, or go back " \
                                 "to the town center. What should Pug do next?"
        else:
            tldr_whats_in_area = "There are three items for sale. A pickaxe, a Dread Lair master key, and an Air " \
                                 "Freshener dripping with Foreshadowing. " \
                                 "Pug can inspect these items, buy the items, or go back " \
                                 "to the town center. What should Pug do next?"

        detailed_description = "Wug mart. The establishment meant to be a sort of superstore for supplying the " \
                               "different goblin trades. " + tldr_whats_in_area

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug walks west up the winding and precarious trail to the Trading Post. "
                "Goblins, not known for their economic models, aren't exactly experts at trade. "
                "But one goblin, Wug, established Wug mart as a sort of Goblin superstore. She's been squirreling "
                "away different treasures from other parts of the dungeon and supplying the "
                "different Goblin trades. Wug looks to Pug when she seems him approaching. "
                "<prosody pitch=\"high\" volume=\"loud\"> Hullo. Welcome to Wug mart. Can I have gold now? "
                "</prosody>" + tldr_whats_in_area)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back at the " + Config.goblin_town_name + " trading post. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == GOBLIN_TOWN_GO_BACK_TO_TOWN or input_action == COMMON_GO_BACK \
                or input_action == COMMON_GO_WEST:
            return GoblinTownCenter().next(RETURN, session)
        elif input_action == GOBLIN_TOWN_TRADER_INSPECT_PICKAXE:
            speech_output = wrap_with_speak(
                "A jagged neon pink pickaxe lays on the shelf. Aside from its awful coloring, it seems to be a perfectly "
                "capable pickaxe. This is probably here for Goblin minors. It's also useful for older goblins "
                "working in the mines.<break time=\"1s\"/> "
                "<prosody pitch=\"high\" volume=\"loud\">Good for smashing,</prosody><break time=\"1s\"/> exclaims Wug. "
                "25 is scribbled in chalk beside the axe. What should Pug do next?")
            session.get_event_inventory().add(Events.goblin_town_seen_pickaxe)
        elif input_action == GOBLIN_TOWN_TRADER_INSPECT_KEY:
            speech_output = wrap_with_speak(
                "A key emblazoned with sinister runes sits on the shelf. Blood covers the handle of the key. This "
                "probably used to belong to an adventurer that met their end in the dungeon. Etched onto the handle "
                "there is a note. Used to open everything in the dungeon. Pug sees no value in this and puts it back "
                "down rudely. <break time=\"1s\"/><prosody pitch=\"high\" volume=\"loud\">Useless thing,</prosody>sighs Wug. "
                "<break time=\"1s\"/>A crude number 1 is scrawled in chalk beside it. What should Pug do next?")
            session.get_event_inventory().add(Events.goblin_town_seen_key)
        elif input_action == GOBLIN_TOWN_TRADER_INSPECT_FRESHENER:
            speech_output = wrap_with_speak(
                "An air freshener sits on the shelf in front of Pug. He inhales deeply. It is the scent of mud "
                "and sweaty armpit. Pug loves the smell and jumps up and down ecstatically. This air freshener "
                "drips with an aura of Foreshadowing related to the future of this game. A 10 is scrawled in "
                "chalk beside it. What should Pug do next?")
            session.get_event_inventory().add(Events.goblin_town_seen_freshener)
        elif input_action == GOBLIN_TOWN_TRADER_SELL_BOOTS and \
                not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
            speech_output = wrap_with_speak(
                "Pug gives Wug the boots from his bag. Wug looks wide eyed at them. "
                "<break time=\"1s\"/><prosody pitch=\"high\" volume=\"loud\">AAHHH, BOOTS!!!</prosody> "
                "<break time=\"1s\"/>She takes a big whiff of them. "
                "<break time=\"1s\"/><prosody pitch=\"high\" volume=\"loud\">Oooo, fresh ones too! "
                "I'll give you 15 gold a boot for these. So that's uh...<break time=\"1s\"/> 61 gold</prosody>"
                "<break time=\"1s\"/>Pug doesn't think that's quite the right price, but lacks the wits to know "
                "for sure, nor the nerve to demand for more. Pug has received 61 gold. "
                "What should Pug do next?")
            session.get_event_inventory().add(Events.goblin_town_sell_boots)
            session.get_item_inventory().mark_item_as_used(World.goblin_town_various_boots)
        elif input_action == GOBLIN_TOWN_TRADER_BUY_PICKAXE \
                and not session.get_item_inventory().exists(World.goblin_town_pickaxe):
            if not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
                speech_output = wrap_with_speak(
                    "Pug has exactly 0 gold coins to his name. Without selling his latest boot haul, Pug won't be "
                    "able to make any purchases. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.goblin_town_seen_pickaxe):
                speech_output = wrap_with_speak(
                    "Not being good at counting, and being too scared of underpaying, Pug throws what he thinks far "
                    "surpasses the 25 gold coins required for the purchase of the axe onto the counter. "
                    "Pug actually puts down 18 coins. "
                    "<prosody pitch=\"high\" volume=\"loud\"> COIN! COIN! COIN!</prosody> "
                    "At least Wug seems happy enough. "
                    "Pug loses 18 gold but stashes the pickaxe in his satchel. What should Pug do next?")
                session.get_item_inventory().add(World.goblin_town_pickaxe)
            else:
                speech_output = wrap_with_speak(
                    "Regardless of how bad Goblins are at micro economics, not even Pug will buy something "
                    "without first looking at what he's buying. Pug should probably inspect the pickaxe "
                    "before buying it. What should Pug do next?")
        elif input_action == GOBLIN_TOWN_TRADER_BUY_KEY:
            if not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
                speech_output = wrap_with_speak(
                    "Pug has exactly 0 gold coins to his name. Without selling his latest boot haul, Pug won't be "
                    "able to make any purchases. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.goblin_town_seen_key):
                speech_output = wrap_with_speak(
                    "Pug scoffs at the master key on the shelf. He sees no need for it, and refuses to spend any "
                    "gold on it. Wug scoffs at the key in agreement. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Regardless of how bad Goblins are at micro economics, not even Pug will buy something "
                    "without first looking at what he's buying. Pug should probably inspect the master key "
                    "before buying it. What should Pug do next?")
        elif input_action == GOBLIN_TOWN_TRADER_BUY_FRESHENER \
                and not session.get_item_inventory().exists(World.goblin_town_freshener):
            if not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
                speech_output = wrap_with_speak(
                    "Pug has exactly 0 gold coins to his name. Without selling his latest boot haul, Pug won't be "
                    "able to make any purchases. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.goblin_town_seen_freshener):
                speech_output = wrap_with_speak(
                    "Pug is giddy with excitement at the prospect of buying the air freshener. He slaps a fistful "
                    "of coins on the counter. In total, 22 coins are on the counter. That is far more gold then "
                    "necessary, but it seems neither Wug nor Pug cares. Pug loses 22 gold but gains the "
                    "air freshener. What should Pug do next?")
                session.get_item_inventory().add(World.goblin_town_freshener)
            else:
                speech_output = wrap_with_speak(
                    "Regardless of how bad Goblins are at micro economics, not even Pug will buy something "
                    "without first looking at what he's buying. Pug should probably inspect the air freshener "
                    "before buying it. What should Pug do next?")
        else:
            speech_output = wrap_with_speak("Pug is in the " + Config.goblin_town_name + " trading post. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class GoblinTownChowHall(State):
    def next(self, input_action, session):
        overriding_action = super(GoblinTownChowHall, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = Config.goblin_town_name + " Chow Hall"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can read the menu, buy something, " \
                             "talk to Grugg, or leave the Chow Hall. What should Pug do next?"
        detailed_description = "The chow hall is a warehouse with long dining tables strewn throughout, with no" \
                               "symmetry or form to it at all. It's perfect. There are waiters all around taking " \
                               "orders. To the right Pug sees Grugg, his most " \
                               "hated neighbour. Grugg was lucky enough to get a corner lot and has a fantastic mud " \
                               "garden. Just thinking about it gets Pug furiously jealous. " + tldr_whats_in_area

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug steps into the Chow Hall and the familiar smell of mud-fusion cuisine wafts to his nose. Pug "
                "salivates at the thought of their delicious mud-glazed pebble soup. " + detailed_description)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back at the " + Config.goblin_town_name + " Chow Hall. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak("Pug is in the " + Config.goblin_town_name + " Chow Hall. " + detailed_description)
        elif input_action == GOBLIN_TOWN_GO_BACK_TO_TOWN or input_action == COMMON_GO_BACK \
                or input_action == GOBLIN_TOWN_CHOW_HALL_LEAVE or input_action == COMMON_EXIT_THE_ROOM \
                or input_action == COMMON_GO_NORTH:
            return GoblinTownCenter().next(RETURN, session)
        elif input_action == GOBLIN_TOWN_CHOW_HALL_TALK_TO_GRUGG:
            if not session.get_event_inventory().exists(Events.goblin_town_talked_to_grugg):
                speech_output = wrap_with_speak(
                    "Pug meekly approaches Grugg with his head held down. Grugg puts his fork down and bellows at Pug: "
                    "<prosody pitch=\"low\" volume=\"loud\">Pug! How have you been!</prosody> "
                    "Grugg throws his arms around Pug roughly and gives him a hug. Pug really, really hates Grugg. "
                    "Nobody else seems to know why, though, as Grugg is a stand up Goblin. <break time=\"1s\"/>"
                    "<prosody pitch=\"low\" volume=\"loud\">Grab some food an eat with me Pug!</prosody> "
                    "There is no way Pug will be eating with Grugg. What should Pug do next?")
                session.get_event_inventory().add(Events.goblin_town_talked_to_grugg)
            else:
                #TODO: Add random shit that grugg says here.
                speech_output = wrap_with_speak("<prosody pitch=\"low\" volume=\"loud\">Pug! Great seeing you again! "
                                                "<break time=\"1s\"/>Did you know Wug has some great new stock over at the Trading Post? "
                                                "In fact, there might be some tools there to help clear those rocks "
                                                "you've been talking about clearing over at the mine!</prosody> "
                                                "<break time=\"1s\"/>Pug really, really hates Grugg and regrets talking to him "
                                                "immensely. What should Pug do next?")
        elif input_action == GOBLIN_TOWN_CHOW_HALL_EAT_WITH_GRUGG \
            and session.get_event_inventory().exists(Events.goblin_town_talked_to_grugg):
            speech_output = wrap_with_speak(
                "Absolutely not. What did Pug say earlier? Pug shakes his head viciously and smacks his head a "
                "few times. There is no way in " + Config.goblin_town_name + " Pug will be eating food with Grugg. He would rather starve. "
                "What should Pug do next?")
        elif input_action == GOBLIN_TOWN_CHOW_HALL_READ_MENU:
            speech_output = wrap_with_speak(
                "Pug reads the menu. It has some of Pug's favorite foods. Mud steak tar tar: 5 gold. "
                "Rock jelly: 3 gold. His favourite dish is back on the menu, mud-glazed pebble soup: 4 gold. "
                "Just thinking about it is making Pug hungry. What should Pug do next?")
        elif input_action == GOBLIN_TOWN_CHOW_HALL_BUY_STEAK:
            speech_output = wrap_with_speak(
                "<prosody pitch=\"x-high\" volume=\"medium\">Sold out.</prosody> The server mumbles meekly. "
                "What should Pug do next?")
        elif input_action == GOBLIN_TOWN_CHOW_HALL_BUY_ROCK_JELLY:
            if not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
                speech_output = wrap_with_speak("Pug has exactly 0 coins to his name. All he can do is stare at the "
                                                "rock jelly hungrily. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.goblin_town_eat_rock_jelly):
                speech_output = wrap_with_speak("Pug has been trying to cut down on his granite intake. He thinks "
                                                "better of buying more rock jelly. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug throws some coin on the counter and asks for some Rock Jelly. The server grabs "
                    "the coins, exactly 6 coins, and gives Pug a dejected shrug and throws him the Rock Jelly. "
                    "Pug thinks he might have the willpower to save this for his journey later. "
                    "He stashes the jelly in his satchel. <break time=\"1s\"/> Nope, he does not. He pulls it back "
                    "out and eats it with great vigor. What should Pug do next?")
                session.get_event_inventory().add(Events.goblin_town_eat_rock_jelly)
        elif input_action == GOBLIN_TOWN_CHOW_HALL_BUY_SOUP:
            if not session.get_event_inventory().exists(Events.goblin_town_sell_boots):
                speech_output = wrap_with_speak("Pug has exactly 0 coins to his name. All he can do is stare at his "
                                                "favourite dish, mud-glazed pebble soup, hungrily. "
                                                "What should Pug do next?")
            elif session.get_event_inventory().exists(Events.goblin_town_eat_soup):
                speech_output = wrap_with_speak("No. Pug knows better than to eat too much of a good thing. He "
                                                "will think wistfully about the next time he will be able to eat such"
                                                "magnificence. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug throws a fistful of coins on the counter and asks for his favorite dish. The server "
                    "grabs the 7 coins, and gives pug a bowl of his favourite soup. Pug cannot and will not wait. "
                    "He takes a seat and scarfs down the soup with impressive vigor for a goblin. Pug feels the "
                    "energy flow through him. Pug is filled with determination. What should Pug do next?")
                session.get_event_inventory().add(Events.goblin_town_eat_soup)
        else:
            speech_output = wrap_with_speak("Pug is in the " + Config.goblin_town_name + " Chow Hall. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)