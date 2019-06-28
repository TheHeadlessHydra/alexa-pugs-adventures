"""
State machine for the keeper trapper world.
"""
from state_machine_common import *
from world import *
from events import *
import logging
from state_machine_ending import *

logger = logging.getLogger()


class KeeperTrapperExecutiveWashroom(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperExecutiveWashroom, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Executive Washroom"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
            tldr_whats_in_area = "Pug can look at the gold faucets, the toilets, inspect the newly arrived plumber, " \
                                 "or exit to the left. What should Pug do next?"
            detailed_description = "Opulent marble floors, beautiful murals adorn the ceiling, crystal clear " \
                                   "mirrors cover one of the walls, leading down to priceless gold " \
                                   "adornments on the wall. There is a plumber heads down fixing the mess that " \
                                   "Pug had caused. Around his waist, pointing away from him and directly at Pug, " \
                                   "is an array of incomprehensible tools. What should Pug do next?"
        elif session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
            tldr_whats_in_area = "It is currently overflowing. Pug should probably tell someone about that. " \
                                 "Pug can look at the gold faucets, the toilets, or leave the washroom to the left. " \
                                 "What should Pug do next?"
            detailed_description = "Opulent marble floors, beautiful murals adorn the ceiling, crystal clear " \
                                   "mirrors cover one of the walls, leading down to priceless gold " \
                                   "adornments on the wall. Water is still coming out of the toilet that Pug clogged. " \
                                   "What should Pug do next?"
        else:
            tldr_whats_in_area = "Pug can look at the gold faucets, the toilets, or leave the washroom to the left. " \
                                 "What should Pug do next?"
            detailed_description = "Opulent marble floors, beautiful murals adorn the ceiling, crystal clear " \
                                   "mirrors cover one of the walls, leading down to priceless gold " \
                                   "adornments on the wall. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug begins swimming through the piranha tank and is halfway to the exit, when suddenly, "
                "a whirling begins and both the water in the tank and Pug are sucked down towards a drain. "
                "After riding the wild whirlpool from the Aquarium, Pug finds that the pipes spit him out into a "
                "magnificent throne room. Opulent marble floors, beautiful murals adorn the ceiling, crystal clear "
                "mirrors cover one of the walls, leading down to priceless gold adornments on the wall. Pug thinks "
                "to himself <break time=\"1s\"/> \"I've finally made it. This is the room I deserve to live in.\" "
                "<break time=\"1s\"/>A moment later a loud flushing comes from the stall next to him. "
                "Welcome to the Executive Washroom. " + tldr_whats_in_area)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug enters the Restroom. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == KEEPER_TRAPPER_WASHROOM_INSPECT_FAUCET:
            speech_output = \
                wrap_with_speak("A beautifully crafted mid-arc golden faucet sits above a marble sink. "
                                "It's the most valuable thing Pug has ever seen in his life and can be "
                                "yours for only 500 gold pieces at the Dungeon Depot. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_WASHROOM_TAKE_FAUCET \
                and not session.get_item_inventory().exists(World.keeper_trapper_faucet):
            if session.get_item_inventory().exists(World.keeper_trapper_eldritch_wrench):
                speech_output = wrap_with_speak(
                    "Pug pulls the Eldritch Wrench out of his backpack and quickly removes the faucet. "
                    "Of course, he didn't think about the fact that water would suddenly start pouring "
                    "out from where the faucet once was. The Plumber yells out in surprise as water "
                    "erupts into the room. Pug quickly bolts out of the restroom, "
                    "with a string of obscenities coming from behind him. What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_faucet_removed)
                session.get_item_inventory().add(World.keeper_trapper_faucet)
                session.get_item_inventory().mark_item_as_used(World.keeper_trapper_eldritch_wrench)
                # Force change the state to the reception but play the string from above.
                # TODO find a cleaner way of doing this
                session.set_stored_game_state("KeeperTrapperReception")
                return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
            else:
                speech_output = wrap_with_speak("Unfortunately, the faucets seem to be magically fastened to the sink. "
                                                "Pug would need some kind of tool to remove it. "
                                                "What should Pug do next?")
        elif input_action == COMMON_GO_LEFT or input_action == COMMON_EXIT_THE_ROOM \
                or input_action == KEEPER_TRAPPER_GO_TO_RECEPTION or input_action == COMMON_OPEN_THE_DOOR \
                or input_action == KEEPER_TRAPPER_WASHROOM_LEAVE_WASHROOM:
            return KeeperTrapperReception().next(RETURN, session)
        elif input_action == KEEPER_TRAPPER_WASHROOM_INSPECT_PLUMBER \
                and session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
            speech_output = wrap_with_speak(
                "A man stands before Pug wearing a robe with a constellations of the heavens upon it. "
                "He brandishes a plunger and is working his magic upon the toilet before him. "
                "Around his waist, pointing away from him and directly at Pug, "
                "is an array of incomprehensible tools. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_WASHROOM_INSPECT_TOOLBELT \
                and session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
            speech_output = wrap_with_speak("Pug inspects the toolbelt of the Arcane Plumber. "
                                            "There is a myriad of different tools with different sizes and "
                                            "shapes, most of which Pug cannot even fathom their uses. "
                                            "The only one he can comprehend is a wrench, which resembles one Pug "
                                            "once used to Deboot a Golem in his past life. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_WASHROOM_TAKE_WRENCH \
                and not session.get_item_inventory().exists(World.keeper_trapper_eldritch_wrench):
            speech_output = wrap_with_speak("Pug deftly takes the Wrench from the Plumbers tool belt. "
                                            "Pug has Obtained the Eldrtich Wrench and has gained a "
                                            "level at Pickpocketing. Of course, this game doesn't use "
                                            "levels in any meaningful way, but it will look good on a resume. "
                                            "What should Pug do next?")
            session.get_item_inventory().add(World.keeper_trapper_eldritch_wrench)
        elif input_action == KEEPER_TRAPPER_WASHROOM_INSPECT_TOILET:
            if session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
                speech_output = wrap_with_speak("The plumber is currently working on fixing the mess that Pug "
                                                "had caused. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_goo_in_toilet) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
                speech_output = wrap_with_speak("The goo is in the toilet alright. Pug thinks about this for a second. "
                                                "What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_goo_in_toilet) \
                    and session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
                speech_output = wrap_with_speak("Water is still flowing from out of the toilet. Pug should probably "
                                                "tell someone before this gets any worse. What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug looks down into the toilet that he left the Aquarium through. "
                                                "It is, indeed, a toilet. It can be flushed. Well, unless it's clogged "
                                                "that is. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_WASHROOM_CLOG_TOILET:
            if session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
                speech_output = wrap_with_speak("He's already done that. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_goo_in_toilet) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
                speech_output = wrap_with_speak("Well. There's some goo in the toilet. Is that what clogging means, "
                                                "Pug wonders. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_goo_in_toilet) \
                    and session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
                speech_output = wrap_with_speak("He's already done that. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Clog the toilet? Pug has no idea what that even means let alone how to do it. "
                    "What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_WASHROOM_GOO_IN_TOILET \
                and session.get_item_inventory().exists(World.keeper_trapper_goo) \
                and not session.get_item_inventory().is_item_already_used(World.keeper_trapper_goo):
            speech_output = wrap_with_speak("Pug puts the Goo into the toilet. What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_place_goo_in_toilet)
            session.get_item_inventory().mark_item_as_used(World.keeper_trapper_goo)
        elif input_action == KEEPER_TRAPPER_WASHROOM_FLUSH_TOILET:
            if session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
                speech_output = wrap_with_speak("Pug doesn't dare to flush the toilet again while the plumber "
                                                "is literally fixing it at that exact moment. That would be madness. "
                                                "What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_goo_in_toilet) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
                speech_output = wrap_with_speak("Pug watches as the Super Goo is set on its maiden journey "
                                                "down the pipes. Then he has a sudden feeling of horror as the "
                                                "water from within the toilet begins to start rising and "
                                                "overflowing. What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_overflowing_toilet)
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_goo_in_toilet) \
                    and session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet):
                speech_output = wrap_with_speak("No. Pug has done enough damage for one day. What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug flushes the toilet. He giggles. What should Pug do next?")
        else:
            speech_output = wrap_with_speak("Pug is in the executive washroom. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class KeeperTrapperReception(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperReception, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Reception"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can speak to the secretary, head to RnDnD, the Boardroom or the Washroom. " \
                             "What should Pug do next?"
        detailed_description = \
            "In front of Pug is a demonic looking secretary sitting in front of large lettering that proclaims " \
            "KEEPER TRAPPER LLC. This must be the area of Mad Mage " + Config.mad_mage_name + "'s dungeon where all of the " \
            "traps are made. In the center of the room sits a bowl of stone fruits. There are three " \
            "doors in this room. The first reads Boardroom. The next reads Research and Design and Development, " \
            "or RnDnD for short. And the final one is the room you just exited, which reads " \
            "Executive Washroom. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug exits the restroom and finds himself in what seems to be a reception area. "
                + detailed_description)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug returns to reception. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == KEEPER_TRAPPER_RECEPTION_TALK_TO_SECRETARY:
            if session.get_event_inventory().exists(Events.keeper_trapper_talked_to_secretary):
                speech_output = wrap_with_speak("Pug begins to approach the secretary, but can't quite "
                                                "build up the courage to talk to her without a reason to. "
                                                "What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug approaches the secretary. She looks completely bored, but beautiful with some "
                    "very demonic qualities. 'Welcome to Keeper Trapper, the kingdom's finest Trapmakers. "
                    "Do you have an appointment?' Pug finds himself paralyzed in her gaze due to a mix of "
                    "fear and love. He shakes his head, unable to lie to such a creature. 'Well, if you "
                    "don't have an appointment, I can't do anything for you,' She says. What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_talked_to_secretary)
        elif input_action == KEEPER_TRAPPER_RECEPTION_TELL_SECRETARY_TOILET \
                and session.get_event_inventory().exists(Events.keeper_trapper_overflowing_toilet) \
                and not session.get_event_inventory().exists(Events.keeper_trapper_plumber_in_washroom):
            speech_output = wrap_with_speak(
                "Pug approaches the secretary and timidly points towards the washroom, which is by now "
                "flooding into the reception area. 'Oh no, not again.' The secretary creates "
                "swirling flames with her hands and suddenly a gate of Hellfire appears before Pug. "
                "A powerful looking demon steps through the portal. 'Who hath summoned the "
                "Infernal Plumber?' bellows the plumber. The secretary points towards the restroom. "
                "'This is a worthy adversary for the master of the Plumbing Arts.' "
                "The demon enters the washroom. What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_plumber_in_washroom)
        elif input_action == KEEPER_TRAPPER_RECEPTION_STONE_FRUIT or input_action == COMMON_LOOK_AT_STATUE:
            speech_output = wrap_with_speak(
                "In the center of the room is a large bowl of stone fruit including apples, bananas, "
                "and a variety of berries. Each piece of fruit is nearly the size of Pug. "
                "It's quite the conversation piece. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_RECEPTION_TAKE_FRUIT:
            speech_output = wrap_with_speak("Which fruit should Pug attempt to steal? There is an apple, a banana, "
                                            "and a bunch of berries. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_RECEPTION_TAKE_APPLE:
            speech_output = wrap_with_speak("Pug tugs at the apple, but it doesn't budge. "
                                            "It appears Pug should work on his core strength. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_RECEPTION_TAKE_BANANA:
            speech_output = wrap_with_speak("Pug stares up at the appealing banana. "
                                            "It's twice his size. He pulls on it, but it seems to "
                                            "have given him the slip. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_RECEPTION_TAKE_BERRIES:
            if session.get_event_inventory().exists(Events.keeper_trapper_take_berries):
                speech_output = wrap_with_speak("Pug remembers the last time he tried to take the berries. "
                                                "He isn't falling for it this time. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug grabs hold of one of the berries, and pulls at it. In his attempt, "
                    "Pug slips to the floor. The berries don't look like they are going anywhere. "
                    "Then pug sees a small stone fall out from inside the berries. A stone seed. "
                    "What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_take_berries)
        elif input_action == KEEPER_TRAPPER_RECEPTION_TAKE_SEED \
                and session.get_event_inventory().exists(Events.keeper_trapper_take_berries):
            if session.get_item_inventory().exists(World.keeper_trapper_seed):
                speech_output = wrap_with_speak("There are no more seeds to take. What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug pockets the seed. What should Pug do next?")
                session.get_item_inventory().add(World.keeper_trapper_seed)
        elif input_action == COMMON_GO_BACK or input_action == KEEPER_TRAPPER_RECEPTION_TO_WASHROOM:
            if session.get_event_inventory().exists(Events.keeper_trapper_faucet_removed):
                speech_output = \
                    wrap_with_speak("Pug can still hear the Arcane Plumber inside battling the mess he had "
                                    "left behind. <break time=\"1s\"/>It's probably not a good idea to "
                                    "return to the scene of the crime. What should Pug do next?")
            else:
                return KeeperTrapperExecutiveWashroom().next(RETURN, session)
        elif input_action == KEEPER_TRAPPER_GO_TO_RNDND:
            return KeeperTrapperRNDND().next(RETURN, session)
        elif input_action == KEEPER_TRAPPER_GO_TO_BOARDROOM:
            return KeeperTrapperBoardRoom().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in reception. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class KeeperTrapperBoardRoom(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperBoardRoom, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Boardroom"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can attempt to talk to an Ogre, go through the gold door or " \
                             "return to reception. What should Pug do next?"

        if session.get_event_inventory().exists(Events.keeper_trapper_seen_coffee_carnage):
            detailed_description = "The once semi-peaceful board room is in shambles. Ogres lay slain here and there. " \
                                   "Apparently the coffee drove them into a fierce battle, their bodies now littering the room, " \
                                   "impaled by various office supplies. One final Ogre remains standing. What should Pug do next?"
        else:
            detailed_description = "Inside the room, a broad oaken table is " \
                                   "surrounded by twelve large burly figures wearing tailored suits and Elf-hide Boots. " \
                                   "Pug has entered the lair of the Business Ogres. Each Ogre motions wildly and " \
                                   "bellows at one another in a bizarre foreign language. " \
                                   "Luckily it seems that either Pug's stealth is too high or " \
                                   "his pay grade is too low to be noticed here. " \
                                   "To the back of the room Pug sees a door covered in gold. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug opens the door and enters into the Board Room. Inside the room, a broad oaken table is "
                "surrounded by twelve large burly figures wearing tailored suits and Elf-hide Boots. "
                "Pug has entered the lair of the Business Ogres. Each Ogre motions wildly and "
                "bellows at one another in a bizarre foreign language. 'OUTSIDE THE BOX ORGANIC GROWTH!' "
                "'STREAMLINED SARBANES OXLEY!' 'GLOBALIZED WIN-WIN PARADIGM SHIFT!' "
                "'SYNERGY SYNERGY SYNERGY!!!' Luckily it seems that either Pug's stealth is too high or "
                "his pay grade is too low to be noticed here. "
                "To the back of the room Pug sees a door covered in gold. " + tldr_whats_in_area)
        elif input_action == RETURN:
            if session.get_event_inventory().exists(Events.keeper_trapper_give_ogre_coffee) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_seen_coffee_carnage):
                session.get_event_inventory().add(Events.keeper_trapper_seen_coffee_carnage)
                speech_output = wrap_with_speak(
                    "The once semi-peaceful board room is in shambles. Ogres lay slain here and there. "
                    "Apparently the coffee drove them into a fierce battle, their bodies now littering the room, "
                    "impaled by various office supplies. One final Ogre remains standing. "
                    "\"ME STRONG OGRE WIN THE FIGHT.\" \"END ALL OGRE DISPUTES.\" "
                    "\"THANK LITTLE GOBLIN MAKE IT RIGHT.\" \"HERE YOU TAKE MY BOOTS.\" With that, "
                    "the Ogre takes off his fine Elven boots and throws them to Pug. "
                    "Oh, what a happy day. " + tldr_whats_in_area)
                session.get_item_inventory().add(World.keeper_trapper_elven_boot)
            elif session.get_event_inventory().exists(Events.keeper_trapper_give_ogre_coffee) \
                    and session.get_event_inventory().exists(Events.keeper_trapper_seen_coffee_carnage):
                speech_output = wrap_with_speak("Pug re-enters the board room. The carnage in the room is still there. "
                                                + tldr_whats_in_area)
            else:
                speech_output = wrap_with_speak("Pug re-enters the board room. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == KEEPER_TRAPPER_BOARDROOM_TALK_TO_OGRE:
            if session.get_event_inventory().exists(Events.keeper_trapper_talk_to_ogres):
                speech_output = wrap_with_speak(
                    "No. Pug would prefer not to be rhymed at again. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug gets the attention of one of the Business Ogres, who turns his head to Pug. "
                    "Upon seeing Pug he licks his lips and smiles. \"NON-FAT, MOCHA EXTRA WHIP."
                    "\"4-PUMP SUGAR-FREE GRANDE. \"SKINNY DECAF EXTRA SHOT.\" \"UPSIDE DOWN CARAMEL LATTE.\" "
                    "The Ogre then returns to yelling at the other Ogres. Pug never realized that Ogres spoke "
                    "such a bizarre language. What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_talk_to_ogres)
        elif input_action == KEEPER_TRAPPER_BOARDROOM_GIVE_COFFEE \
                and not session.get_event_inventory().exists(Events.keeper_trapper_give_ogre_coffee) \
                and session.get_event_inventory().exists(Events.keeper_trapper_talk_to_ogres) \
                and session.get_item_inventory().exists(World.keeper_trapper_coffee):
            speech_output = wrap_with_speak(
                "Pug gets the attention of one of the Business Ogre again and holds the cup of "
                "coffee up to the giant. The Ogre takes the cup and sips it. "
                "His eyes glow red as he chugs the rest of it. \"BRICK AND MORTAR DOWNSIZING.\" "
                "\"LEVERAGE UPWARD MOBILITY.\" \"BE TO BE OFFSHORE EMPOWERMENT.\" "
                "\"SYNERGY SYNERGY SYNERGY!\" The Ogre then picks up his chair and flings it across the "
                "table at one of the other Ogres. The other ogres then begin throwing their own "
                "chairs in kind. Pug darts out of the room to Reception as the Ogres begin "
                "attacking one another. It seems Pug should have requested decaf after all. "
                "What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_give_ogre_coffee)
            session.get_item_inventory().mark_item_as_used(World.keeper_trapper_coffee)
            # Force change the state to the reception but play the string from above.
            # TODO find a cleaner way of doing this
            session.set_stored_game_state("KeeperTrapperReception")
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
        elif input_action == KEEPER_TRAPPER_GO_THROUGH_GOLDEN_DOOR:
            if session.get_item_inventory().exists(World.keeper_trapper_golden_door_key):
                session.get_item_inventory().mark_item_as_used(World.keeper_trapper_golden_door_key)
                return KeeperTrapperCEOsRoom().next(input_action, session)
            else:
                speech_output = wrap_with_speak("Pug attempts to open the golden door. However it seems that the "
                                                "door is locked. Pug would need a key to get through this door. "
                                                "What should Pug do next?")
        elif input_action == COMMON_GO_BACK or input_action == KEEPER_TRAPPER_GO_TO_RECEPTION:
            return KeeperTrapperReception().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in the board room. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class KeeperTrapperCEOsRoom(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperCEOsRoom, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "CEOs Room"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can look at the Zen Garden, silver doors, fountains, the oak desk " \
                             "or return to the boardroom. What should Pug do next?"

        describe_inside_silver_door = "Inside the room " \
                                      "is a pile of three, quite dead, adventurers. A human paladin lies on the " \
                                      "bottom, his armor having been punctured several hundred times. Atop him is a " \
                                      "lizardfolk warlock, who has been burnt to a crisp. A gnome bard lies atop " \
                                      "the lizard except it looks like he's been turned inside out. " \
                                      "Finally, atop the carnage within is a small stuffed unicorn. "

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug uses the glowing key and opens the golden door. He sees a spacious room filled with "
                "several fountains with sculptures "
                "of Ogre women pouring water. To the left is a zen garden, to the right "
                "is two large silver doors with no handles. Straight ahead is a large wooden desk. "
                "What should Pug do next?" + tldr_whats_in_area)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug has returned to the extravagant office. " + tldr_whats_in_area)
        elif input_action == COMMON_GO_RIGHT or input_action == KEEPER_TRAPPER_CEO_GO_TO_SILVER_DOOR:
            speech_output = wrap_with_speak("Pug looks up at two monolithic silver doors with no handles "
                                            "and scratches his head. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_CEO_OPEN_RAGMUFFIN:
            if session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open):
                speech_output = wrap_with_speak("The elevator doors are already open. It does not open harder like "
                                                "Pug might have hoped. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_opened_elevator_after_trap_broken):
                speech_output = wrap_with_speak("The elevator doors open again. "
                                                "The twisted scrap metal is still strewn all over the floor of the "
                                                "room. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_trap_broken):
                speech_output = wrap_with_speak("Water pours out from inside the elevator. Pug gets soaked as it "
                                                "rushes into the grates behind him. "
                                                "In the middle of the room where the Unicorn once stood menacingly, "
                                                "is a ball of shredded scrap metal with bent and broken blades "
                                                "protruding from it. It seems that the UltraTrap9000 still has a "
                                                "few design flaws. Unfortunately, it seems to have taken the "
                                                "everlasting pitcher with it in the explosion. "
                                                "Pug can now enter the silver doors. "
                                                "What should Pug do?")
                session.get_event_inventory().add(Events.keeper_trapper_opened_elevator_after_trap_broken)
            else:
                if session.get_event_inventory().exists(Events.keeper_trapper_looked_at_blueprints):
                    speech_output = \
                        wrap_with_speak("The two large silver doors slide open revealing an elevator room. "
                                        + describe_inside_silver_door +
                                        "Pug remembers the blueprint from RnDnD. "
                                        "This is clearly the work of the UltraTrap 9000 Pro Edition. "
                                        "The finest in ultimate trap destruction. "
                                        "What should Pug do next?")
                else:
                    speech_output = \
                        wrap_with_speak("The two large silver doors slide open revealing an elevator room. " +
                                        describe_inside_silver_door + "What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_silver_door_open)
        elif (input_action == COMMON_LOOK_IN_ROOM or input_action == KEEPER_TRAPPER_LOOK_INSIDE_SILVER_DOORS) \
                and session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open):
            if session.get_event_inventory().exists(Events.keeper_trapper_looked_at_blueprints) \
                    and session.get_event_inventory().exists(Events.keeper_trapper_pitcher_in_trap_room):
                speech_output = \
                    wrap_with_speak(describe_inside_silver_door +
                                    "The pitcher that Pug threw is still in the room, its water flowing out "
                                    "and draining in a grate outside the room. "
                                    "Pug remembers the blueprint from RnDnD. "
                                    "This is clearly the work of the UltraTrap 9000 Pro Edition. "
                                    "The finest in ultimate trap destruction. "
                                    "What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_looked_at_blueprints) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_pitcher_in_trap_room):
                speech_output = \
                    wrap_with_speak(describe_inside_silver_door +
                                    "Pug remembers the blueprint from RnDnD. "
                                    "This is clearly the work of the UltraTrap 9000 Pro Edition. "
                                    "The finest in ultimate trap destruction. "
                                    "What should Pug do next?")
            else:
                if session.get_event_inventory().exists(Events.keeper_trapper_pitcher_in_trap_room):
                    speech_output = \
                        wrap_with_speak(describe_inside_silver_door + "What should Pug do next?")
                else:
                    speech_output = \
                        wrap_with_speak(describe_inside_silver_door +
                                        "The pitcher that Pug threw is still in the room, its water flowing out "
                                        "and draining in a grate outside the room. " +
                                        "What should Pug do next?")
        elif input_action == COMMON_OPEN_THE_DOOR or input_action == KEEPER_TRAPPER_CEO_THROUGH_SILVER_DOORS:
            if session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_trap_broken):
                speech_output = wrap_with_speak("It looks like quite a few people have met their demise in this room. "
                                                "Pug is in no hurry to incur the wrath of the stuffed Unicorn. He "
                                                "refuses to enter the room. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open) \
                    and session.get_event_inventory().exists(Events.keeper_trapper_trap_broken):
                return KeeperTrapperElevator().next(RETURN, session)
            else:
                speech_output = wrap_with_speak("Pug looks up at two monolithic silver doors with no handles "
                                                "and scratches his head. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_CEO_THROW_LETTER_OPENER_AT_TRAP \
                and session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open) \
                and session.get_item_inventory().exists(World.keeper_trapper_letter_opener) \
                and not session.get_event_inventory().exists(Events.keeper_trapper_trap_broken):
            speech_output = wrap_with_speak("Pug throws the Letter Opener at the Unicorn's head. "
                                            "Right as it is about to hit the Unicorn, a rainbow colored flash of "
                                            "magic deflects the letter opener back at him. The letter opener just "
                                            "barely misses pug on its way back as it clatters on the ground beside "
                                            "him. He picks it up and puts it back in his pack. "
                                            "What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_USE_PITCHER_ON_TRAP \
                and not session.get_item_inventory().is_item_already_used(World.keeper_trapper_everlasting_pitcher) \
                and session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open):
            speech_output = wrap_with_speak("Pug takes the Everflowing Pitcher from his bag and rolls it into "
                                            "the Unicorn's room. Water continues to feebly flood out of the room "
                                            "towards Pug, eventually draining down a grate. What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_pitcher_in_trap_room)
            session.get_item_inventory().mark_item_as_used(World.keeper_trapper_everlasting_pitcher)
        elif input_action == KEEPER_TRAPPER_CEO_CLOSE_RAGMUFFIN:
            if not session.get_event_inventory().exists(Events.keeper_trapper_silver_door_open):
                speech_output = wrap_with_speak("The elevator doors are not open anyway. He doesn't know what he "
                                                "expected. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_pitcher_in_trap_room) \
                    and not session.get_event_inventory().exists(Events.keeper_trapper_opened_elevator_after_trap_broken):
                speech_output = wrap_with_speak("The elevator doors slide closed with the stuffed unicorn and the "
                                                "Everflowing Pitcher inside. From inside the elevator, Pug can "
                                                "hear more and more water rising within the Unicorn's room. "
                                                "After a few minutes, Pug hears the sound of a "
                                                "mechanical neighing followed by a loud explosion. "
                                                "What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_trap_broken)
            else:
                speech_output = wrap_with_speak("Pug hears the same whirring from before "
                                                "and the doors to the elevator slide closed. "
                                                "What should Pug do next?")
            session.get_event_inventory().remove(Events.keeper_trapper_silver_door_open)
        elif input_action == COMMON_GO_LEFT or input_action == KEEPER_TRAPPER_CEO_GO_TO_GARDEN:
            if session.get_event_inventory().exists(Events.keeper_trapper_sprout_seed_zen_garden):
                # TODO add random flower here
                speech_output = wrap_with_speak("A beautiful bouquet of chrysanthemum's lie where the zen garden "
                                                "used to be. Pug can't help but feel calm looking at the arrangement. "
                                                "What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_place_seed_zen_garden):
                speech_output = wrap_with_speak("A sand pit sits to the left in the office. There is nothing "
                                                "notable about the garden except for the seed that he carefully "
                                                "placed in the center. Pug has a strange feeling that this "
                                                "could be the key to the inner peace he's been seeking. What should "
                                                "pug do next?")
            else:
                speech_output = wrap_with_speak("A sand pit sits to the left in the office. There is nothing "
                                                "notable about the garden, however Pug has a strange feeling that this "
                                                "could be the key to the inner peace he's been seeking. What should "
                                                "pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_water_zen_garden)
        elif input_action == KEEPER_TRAPPER_PLANT_SEED \
                and not session.get_event_inventory().exists(Events.keeper_trapper_place_seed_zen_garden):
            speech_output = wrap_with_speak("Pug digs a small hole in the dirt and places the stone seed "
                                            "into the sand. What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_place_seed_zen_garden)
        elif input_action == KEEPER_TRAPPER_CEO_WATER_GARDEN \
                and session.get_item_inventory().exists(World.keeper_trapper_everlasting_pitcher) \
                and not session.get_item_inventory().is_item_already_used(World.keeper_trapper_everlasting_pitcher) \
                and session.get_event_inventory().exists(Events.keeper_trapper_place_seed_zen_garden) \
                and not session.get_event_inventory().exists(Events.keeper_trapper_sprout_seed_zen_garden):
            # TODO add random flower here
            speech_output = wrap_with_speak("A small stone leaf begins to sprout from the Zen Garden. "
                                            "Then, suddenly stone vines begin encircling the Zen Garden. Out from the "
                                            "garden sprouts a beautiful bouquet of chrysanthemum's. Pug is both "
                                            "amazed and confused by the sudden sprouting of flowers. "
                                            "What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_sprout_seed_zen_garden)
        elif input_action == COMMON_WALK_TO_FOUNTAIN or input_action == COMMON_LOOK_AT_STATUE:
            if session.get_item_inventory().exists(World.keeper_trapper_everlasting_pitcher):
                speech_output = wrap_with_speak("Pug approaches one of the fountains. A marble female Ogre that "
                                                "used to be holding the Everlasting Pitcher. It looks morose without "
                                                "the pitcher. What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug approaches one of the fountains. A marble female Ogre holding a "
                                                "conspicuous pitcher that is pouring water into the fountain below. "
                                                "What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_seen_fountain)
        elif input_action == KEEPER_TRAPPER_TAKE_PITCHER \
                and session.get_event_inventory().exists(Events.keeper_trapper_seen_fountain) \
                and not session.get_item_inventory().exists(World.keeper_trapper_everlasting_pitcher):
            speech_output = \
                wrap_with_speak("Pug climbs onto the statue and rips the decanter from the arms of the marble Ogre. "
                                "With a little effort, Pug is able to pull the Pitcher free. To Pug's surprise, "
                                "it continues to fill and overflow with water. Pug has obtained the Everflowing "
                                "Pitcher. He's also created quite a safety hazard by pouring water all over the floor. "
                                "What should Pug do next?")
            session.get_item_inventory().add(World.keeper_trapper_everlasting_pitcher)
        elif input_action == KEEPER_TRAPPER_PLACE_PITCHER_BACK \
                and session.get_item_inventory().exists(World.keeper_trapper_everlasting_pitcher):
            speech_output = wrap_with_speak("Pug thinks about this carefully and decides he does not want to place "
                                            "the pitcher back. At all. What should Pug do next?")
        elif input_action == COMMON_GO_FORWARD or input_action == KEEPER_TRAPPER_CEO_GO_TO_DESK:
            if session.get_item_inventory().exists(World.keeper_trapper_letter_opener):
                speech_output = wrap_with_speak("Pug looks at the oaken desk. It's a nice desk. There is only "
                                                "a pamphlet left on it. "
                                                "What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug looks at the oaken desk. "
                                                "The desk is bare except for a pamphlet sitting next to "
                                                "a golden letter opener. What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_seen_desk)
        elif (input_action == COMMON_READ_THE_PAMPHLET or input_action == KEEPER_TRAPPER_TAKE_PAMPHLET) \
                and session.get_event_inventory().exists(Events.keeper_trapper_seen_desk):
            speech_output = wrap_with_speak("Pug picks up the pamphlet and reads it. \"MISSING GOBLIN: "
                                            "It appears that Goblin Town has misplaced one of its goblins. "
                                            "If you find it, please contact Goblin Control for it to be "
                                            "returned to its rightful place. Thank you.\" Pug puts the pamphlet "
                                            "back down nervously. What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_TAKE_LETTER_OPENER \
                and session.get_event_inventory().exists(Events.keeper_trapper_seen_desk) \
                and not session.get_item_inventory().exists(World.keeper_trapper_letter_opener):
            speech_output = wrap_with_speak("Pug picks up the Letter Opener. Arcane energy ripples through Pug's "
                                            "body when he picks it up. Pug has obtained the Letter Opener Plus One. "
                                            "What should Pug do next?")
            session.get_item_inventory().add(World.keeper_trapper_letter_opener)
        elif input_action == COMMON_GO_BACK or input_action == KEEPER_TRAPPER_GO_TO_BOARDROOM:
            return KeeperTrapperBoardRoom().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in the extravagant office. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class KeeperTrapperElevator(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperElevator, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Elevator Room"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug sees that the room actually only has one button. " \
                             "Next to the button is a crude drawing of several vicious looking dogs. " \
                             "What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug steps through the elevator doors minding the broken trap strewn around him. He hears rather irritating music playing from... somewhere. "
                + tldr_whats_in_area)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back in the elevator with the irritating music. "
                                            + tldr_whats_in_area)
        elif input_action == COMMON_PRESS_BUTTON or input_action == KEEPER_TRAPPER_ELEVATOR_PRESS_BUTTON:
            return EndingState().next(RETURN, session)
        elif input_action == COMMON_GO_BACK or input_action == KEEPER_TRAPPER_ELEVATOR_LEAVE:
            return KeeperTrapperCEOsRoom().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in the elevator. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


# TODO add hints inbetween sections by asking again, etc.
class KeeperTrapperRNDND(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperRNDND, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "RnDnD"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can check out the strange workstation, the terrifying looking device, go to the " \
                             "room marked Trap Bears, the netting room or go back to Reception. " \
                             "What should Pug do next?"

        detailed_description = "This room is where all of the traps of the dungeon are designed. Nearly all of the " \
                               "workstations are spotless, except for one that has a strange gray clay on it. " \
                               "Near the front of the room is a terrifying looking device. " \
                               "To the left is a room marked Trap Bears and to the right is a " \
                               "room marked Netting. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug finds himself in a large room filled with experimental trap designs on the walls. " +
                detailed_description)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back in RnDnD. " + tldr_whats_in_area)
        elif input_action == COMMON_GO_RIGHT or input_action == KEEPER_TRAPPER_GO_TO_NET_ROOM:
            return KeeperTrapperNetRoom().next(RETURN, session)
        elif input_action == KEEPER_TRAPPER_RNDND_INSPECT_WORKSTATION:
            return KeeperTrapperWorkstation().next(RETURN, session)
        elif input_action == COMMON_GO_LEFT \
                or input_action == KEEPER_TRAPPER_RNDND_TRAP_BEAR \
                or input_action == COMMON_OPEN_THE_DOOR:
            if session.get_event_inventory().exists(Events.keeper_trapper_opened_trap_bear_door):
                speech_output = wrap_with_speak("No, Pug would rather not relive the most "
                                                "terrifying experience of his short life. What should Pug do next?")
            else:
                speech_output = \
                    wrap_with_speak("Pug opens the door clearly mismarked Trap Bears. Inside he finds out "
                                    "that it's he who is mistaken as two ten foot tall bears made out of traps are "
                                    "standing above the body of several half-eaten goblins in lab coats. "
                                    "The great beasts roar ferociously at Pug and begin to charge. "
                                    "Pug quickly closes the door and returns to the RnDnD room. "
                                    "What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_opened_trap_bear_door)
        elif input_action == KEEPER_TRAPPER_RNDND_TALK_TO_CAFFINOX and \
            session.get_event_inventory().exists(Events.keeper_trapper_caffenox_lives):
            if session.get_event_inventory().exists(Events.keeper_trapper_given_strange_machine_water) \
                and not session.get_item_inventory().exists(World.keeper_trapper_coffee):
                speech_output = wrap_with_speak("Pug meekly asks Caffinox what to do next. "
                                                "<prosody pitch=\"x-low\" volume=\"loud\"> FOOL! Press my button, "
                                                "and obtain the ichor of life.</prosody> What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_given_strange_machine_water) \
                and session.get_item_inventory().exists(World.keeper_trapper_coffee):
                speech_output = wrap_with_speak("Pug meekly asks Caffinox for some more coffee. "
                                                "<prosody pitch=\"x-low\" volume=\"loud\"> FOOL! The ichor of life "
                                                "is not to be given twice!</prosody> What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug meekly asks Caffinox what it wanted again. "
                                                "<prosody pitch=\"x-low\" volume=\"loud\"> FOOL! Bring me water, "
                                                "little one.</prosody> What should Pug do next?")
        elif input_action == COMMON_GO_FORWARD or input_action == KEEPER_TRAPPER_RNDND_INSPECT_MACHINE:
            if session.get_event_inventory().exists(Events.keeper_trapper_looked_at_strange_machine):
                speech_output = wrap_with_speak("Caffinox stands before Pug. Quite a menacing visage. "
                                                "What should Pug do next?")
            else:
                speech_output = \
                    wrap_with_speak("Before Pug is what must be one of the diabolical machinations of the "
                                    "Keeper Trapper inventors. A monolithic machine with a face made of gears "
                                    "towers above, but in the middle is a red button. "
                                    "Does Pug dare to touch the button? What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_looked_at_strange_machine)
        elif input_action == COMMON_PRESS_BUTTON or input_action == KEEPER_TRAPPER_RNDND_PRESS_BUTTON \
                and session.get_event_inventory().exists(Events.keeper_trapper_looked_at_strange_machine):
            if session.get_event_inventory().exists(Events.keeper_trapper_given_strange_machine_water) \
                    and not session.get_item_inventory().exists(World.keeper_trapper_coffee):
                speech_output = \
                    wrap_with_speak("A small cup dispenses from just below Caffinox's mouth. Caffinox's mouth opens "
                                    "and a hot, fragrant brown liquid pours from the machine's mouth. "
                                    "<prosody pitch=\"x-low\" volume=\"loud\">There you go little one, enjoy! "
                                    "</prosody> Pug has obtained one hot cup of coffee. What should Pug do next?")
                session.get_item_inventory().add(World.keeper_trapper_coffee)
            elif session.get_event_inventory().exists(Events.keeper_trapper_caffenox_lives):
                speech_output = wrap_with_speak("Pug presses the button again. That was probably ill-advised. "
                                                "<prosody pitch=\"x-low\" volume=\"loud\">DO NOT PRESS "
                                                "ME FOR NO REASON.</prosody> Pug gulps. What should Pug do next?")
            elif session.get_event_inventory().exists(Events.keeper_trapper_strange_machine_tried_pushing_button):
                speech_output = \
                    wrap_with_speak("The machine begins whirring to life, gears turning and the eyes on the "
                                    "face glow a faint blue color. <prosody pitch=\"x-low\" volume=\"loud\"> "
                                    "\"CAFFINOX AWAKENS! The creation of the Elder Men, "
                                    "the culmination of a thousand minds, who is it who has awoken me?\" </prosody>"
                                    "Pug waves meekly.  <prosody pitch=\"x-low\" volume=\"loud\">"
                                    "\"In gratitude for returning me to the realm of the living, "
                                    "I offer you a covenant. Bring me water to quench my eternal thirst and I "
                                    "shall give to you the blood of the gods, the ichor of life itself. "
                                    "Tell me tiny one, do you agree to this contract?\"</prosody> "
                                    "Pug sighs and agrees. What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_caffenox_lives)
            else:
                speech_output = wrap_with_speak(
                    "Pug thinks about the consequences of pushing such a button and wonders "
                    "if he should really press it... What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_strange_machine_tried_pushing_button)
        elif input_action == KEEPER_TRAPPER_RNDND_GIVE_WATER \
                and session.get_item_inventory().exists(World.keeper_trapper_everlasting_pitcher) \
                and not session.get_item_inventory().is_item_already_used(World.keeper_trapper_everlasting_pitcher) \
                and not session.get_event_inventory().exists(Events.keeper_trapper_given_strange_machine_water) \
                and session.get_event_inventory().exists(Events.keeper_trapper_caffenox_lives):
            speech_output = \
                wrap_with_speak("Pug pulls out the still overflowing Everlasting Pitcher. "
                                "<prosody pitch=\"x-low\" volume=\"loud\">What's this? You have brought me the "
                                "necessary water to quell this incessant drought? Please tiny one, "
                                "pour the contents into my mouth. </prosody> Pug pours the pitcher into "
                                "Caffinox's mouth. <prosody pitch=\"x-low\" volume=\"loud\"> gurgle... gurgle... "
                                "Ahhhh, yes, that hits the spot! Now little one, press the button once "
                                "more and receive my gift. </prosody> What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_given_strange_machine_water)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == COMMON_GO_BACK or input_action == KEEPER_TRAPPER_GO_TO_RECEPTION:
            return KeeperTrapperReception().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in RnDnD. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class KeeperTrapperWorkstation(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperWorkstation, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Workstation"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_item_inventory().exists(World.keeper_trapper_goo) \
                and session.get_item_inventory().exists(World.keeper_trapper_envelope):
            detailed_description = "All that's left at the workstation is a blueprint. What should Pug do next?"
            tldr_description = "All that's left here is to look at the blueprint or head back. " \
                               "What should Pug do next?"
        elif session.get_item_inventory().exists(World.keeper_trapper_goo) \
                and not session.get_item_inventory().exists(World.keeper_trapper_envelope):
            detailed_description = "There appears to be some kind of envelope on the workstation and bolted to the " \
                                   "wall is an interesting looking blueprint. What should Pug do next?"
            tldr_description = "Pug can take the envelope, look at the blueprint, or head back. " \
                               "What should Pug do next?"
        elif not session.get_item_inventory().exists(World.keeper_trapper_goo) \
                and session.get_item_inventory().exists(World.keeper_trapper_envelope):
            detailed_description = "There's some packaging next to the gray puddy that proclaims it to be " \
                                   "\"SUPER GOO\" the amazing new toy from KEEPER TRAPPER FOR KIDS! " \
                                   "Bolted to the wall is an interesting looking blueprint. What should Pug do next?"
            tldr_description = "Pug can take the envelope, look at the blueprint, or head back. " \
                               "What should Pug do next?"
        else:
            detailed_description = "There's some packaging next to the gray puddy that proclaims it to be " \
                                   "\"SUPER GOO\" the amazing new toy from KEEPER TRAPPER FOR KIDS! " \
                                   "There also appears to be some kind of envelope here and bolted to the wall " \
                                   "is an interesting looking blueprint. What should Pug do next?"
            tldr_description = "Pug can take the super goo, the envelope, look at the blueprint, or head back. " \
                               "What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak("Pug approaches a workstation with some strange gray substance on it. "
                                            + detailed_description)
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug is back at the workstation. " + tldr_description)
        elif input_action == KEEPER_TRAPPER_WORKSTATION_TAKE_GOO \
                and not session.get_item_inventory().exists(World.keeper_trapper_goo):
            speech_output = wrap_with_speak("When Pug picks up the goo, it starts moving around in his hands. "
                                            "Pug quickly throws it into his bag. What should pug do next?")
            session.get_item_inventory().add(World.keeper_trapper_goo)
        elif input_action == KEEPER_TRAPPER_WORKSTATION_TAKE_ENVELOPE \
                and not session.get_item_inventory().exists(World.keeper_trapper_envelope):
            speech_output = \
                wrap_with_speak("Pug picks up the envelope. It has several colored runes around it. "
                                "However, try as he might, Pug can't seem to open the envelope. "
                                "Not even biting it seems to be working. Well, stealing it still works. "
                                "Pug puts the Envelope into his bag. What should Pug do next?")
            session.get_item_inventory().add(World.keeper_trapper_envelope)
        elif input_action == KEEPER_TRAPPER_WORKSTATION_INSPECT_BLUEPRINT:
            speech_output = \
                wrap_with_speak("Pug inspects the Blueprint on the front wall. At the top it reads "
                                "\"Ultra Trap 9000 Pro Edition\". The trap shows a model that's a "
                                "hybrid of every kind of trap Pug had ever seen. Sharp metal spikes, "
                                "poisoned darts, arcane runes and spouts of flame cover the entire thing. "
                                "And it's all shaped inside what looks like a stuffed unicorn. "
                                "There's some text written in red pencil at the bottom that reads <break time=\"1s\"/>"
                                "\"Shorts out if submerged in water. Must fix before deployment!\" "
                                "What should Pug do next?")
            session.get_event_inventory().add(Events.keeper_trapper_looked_at_blueprints)
        elif input_action == KEEPER_TRAPPER_TAKE_BLUEPRINT:
            speech_output = wrap_with_speak("The blueprint is very clearly bolted to the wall. Pug smacks the "
                                            "bolts bemusedly knowing it's not going to happen. He could try to"
                                            "memorize it, Pug guesses... What should Pug do next?")
        elif input_action == COMMON_GO_BACK:
            return KeeperTrapperRNDND().next(RETURN, session)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        else:
            speech_output = wrap_with_speak("Pug is at the workstation. " + tldr_description)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class KeeperTrapperNetRoom(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(KeeperTrapperNetRoom, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Net room"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_item_inventory().exists(World.keeper_trapper_golden_door_key):
            if session.get_event_inventory().exists(Events.keeper_trapper_free_elf):
                tldr_whats_in_area = "There's nothing left here. What should Pug do next?"
                detailed_description = "There is a fine assortment of nets within the Net room." \
                                       "Fishing nets, butterfly nets, Newsnets, Internets, " \
                                       "Brooklyn Nets, all sorts of nets. The elf has been freed already." \
                                       "What should Pug do next?"
            else:
                tldr_whats_in_area = "The Half-Elf Thief is still here, still hanging out. Pug already has his key " \
                                     "and sees no reason to set the elf free anymore. What should Pug do next?"
                detailed_description = "There is a fine assortment of nets within the Net room." \
                                       "Fishing nets, butterfly nets, Newsnets, Internets, " \
                                       "Brooklyn Nets, all sorts of nets. The elf is still hanging upside down. " \
                                       "Pug wonders how he isn't passing out. Pug already has the glowing key. " \
                                       "What should Pug do next?"
        else:
            tldr_whats_in_area = "The Half-Elf Thief is still here, still hanging out, with a glowing key " \
                                 "draped around his neck. What should Pug do next?"
            detailed_description = "There is a fine assortment of nets within the Net room." \
                                   "Fishing nets, butterfly nets, Newsnets, Internets, " \
                                   "Brooklyn Nets, all sorts of nets. The elf is still hanging upside down. " \
                                   "Pug wonders how he isn't passing out. The elf has a glowing key draped around " \
                                   "his neck that looks like it could be useful. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug opens the door labelled Netting and finds a fine assortment of Nets within. "
                "Fishing nets, butterfly nets, Newsnets, Internets, Brooklyn Nets, all sorts of nets. "
                "<prosody pitch=\"low\" volume=\"medium\">"
                "Hey you! Help me down from here!</prosody> exclaims a voice from above. "
                "A Half-Elf thief hangs from one of the nets above with a glowing key draped around his neck. "
                "What should Pug do next?")
        elif input_action == RETURN:
            speech_output = wrap_with_speak("Pug returns to Net Room. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(detailed_description)
        elif input_action == KEEPER_TRAPPER_NET_ROOM_TAKE_KEY \
                and not session.get_item_inventory().exists(World.keeper_trapper_golden_door_key):
            speech_output = wrap_with_speak(
                "Pug thinks about trying to take the glowing key from the neck of this elf for a second. "
                "<break time=\"1s\"/>Nope, that is definitely a bad idea. Although hanging, the elf's arms are "
                "very clearly free. Maybe Pug can try asking nicely instead? What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_NET_ROOM_TALK_TO_ELF:
            if session.get_event_inventory().exists(Events.keeper_trapper_talk_to_elf_part_one):
                speech_output = \
                    wrap_with_speak("Pug approaches the half-elf trapped in the net. He's wearing leather armor "
                                    "and has a glowing key around his neck. This must be another adventurer who got "
                                    "trapped while infiltrating the dungeon. "
                                    "<prosody pitch=\"low\" volume=\"medium\">"
                                    "Hey, you! <break time=\"1s\"/> You need to help me out of here. "
                                    "I seem to have gotten into a bit of a bind. If you can help me out of here, "
                                    "I'll make it worth your while.</prosody> the half-elf exclaims. "
                                    "Pug doesn't have a while, so he wasn't sure what it would be worth, "
                                    "but perhaps helping this Half-Elf would allow Pug to get out of this dungeon. "
                                    "Pug can continue talking with the half-elf or leave. What should Pug do next?")
                session.get_event_inventory().add(Events.keeper_trapper_talk_to_elf_part_one)
            else:
                speech_output = \
                    wrap_with_speak("<prosody pitch=\"low\" volume=\"medium\">"
                                    "You'll help me? Great! I need you to find me a knife to cut me out of this. "
                                    "</prosody>Pug tells the half-elf he'll start looking for a fish right away. "
                                    "<prosody pitch=\"low\" volume=\"medium\"> Wha? <break time=\"1s\"/>"
                                    "A fish? What... No, what we need is a magical weapon. I've got plenty of knives, "
                                    "but this is a Magic Net Plus One, so it would need an equally powerful "
                                    "magic weapon to cut through.</prosody> Pug nods. <break time=\"1s\"/> "
                                    "Though he's not sure what plus one means... he's sure he'll figure it out. "
                                    "What should Pug do next?")
        elif input_action == KEEPER_TRAPPER_NET_ROOM_ASK_FOR_THEY_KEY:
            speech_output = wrap_with_speak("<prosody pitch=\"low\" volume=\"medium\">"
                                            "What. This? Oh, yes, this is a master key! "
                                            "It can open any door but can only be used once. It's priceless. "
                                            "If you have any valuable treasure though, I'd be willing to trade "
                                            "it to you... Or, you know... You can cut me down... </prosody>"
                                            "What should Pug do next?\"")
        elif input_action == KEEPER_TRAPPER_NET_ROOM_FAUCET_FOR_KEY \
                and not session.get_item_inventory().exists(World.keeper_trapper_golden_door_key):
            speech_output = wrap_with_speak("<prosody pitch=\"low\" volume=\"medium\">"
                                            "That's... not exactly the treasure I was thinking of, but okay. "
                                            " </prosody>Pug trades the Faucet to the Half-Elf and receives the "
                                            "One-Time Master Key. What should Pug do next?")
            session.get_item_inventory().mark_item_as_used(World.keeper_trapper_faucet)
            session.get_item_inventory().add(World.keeper_trapper_golden_door_key)
        elif input_action == KEEPER_TRAPPER_NET_ROOM_FREE_ELF:
            speech_output = wrap_with_speak("Pug ponders for a second and moves in to try and bite the rope. The "
                                            "Half-elf chimes in, irritated. <prosody pitch=\"low\" volume=\"medium\"> "
                                            "... I told you only a magical plus one weapon can cut this plus "
                                            "one net... </prosody> What should pug do next?")
        elif (input_action == KEEPER_TRAPPER_NET_ROOM_CUT_DOWN_ELF_WITH_OPENER or input_action == KEEPER_TRAPPER_USE_OPENER) \
                and session.get_item_inventory().exists(World.keeper_trapper_letter_opener) \
                and not session.get_event_inventory().exists(Events.keeper_trapper_free_elf):
            if session.get_item_inventory().exists(World.keeper_trapper_golden_door_key):
                speech_output = wrap_with_speak("Pug pulls out his Letter Opener plus one and cuts the "
                                                "Half-Elf free from the net. "
                                                "<prosody pitch=\"low\" volume=\"medium\">"
                                                "Wow... A goblin freeing me... "
                                                "I guess I've seen everything now.</prosody> The Half-Elf "
                                                "runs off. Pug feels cheated. What should Pug do next?")
            else:
                speech_output = wrap_with_speak("Pug pulls out his Letter Opener plus one and cuts the "
                                                "Half-Elf free from the net. "
                                                "<prosody pitch=\"low\" volume=\"medium\">"
                                                "Wow... A goblin freeing me... "
                                                "I guess I've seen everything now.</prosody> "
                                                "The Half-Elf thanks Pug, passing him the key around his neck, "
                                                "and runs off. What should Pug do next?\"")
                session.get_item_inventory().add(World.keeper_trapper_golden_door_key)
            session.get_event_inventory().add(Events.keeper_trapper_free_elf)
        elif input_action == COMMON_GO_BACK or input_action == KEEPER_TRAPPER_GO_TO_RNDND:
            return KeeperTrapperRNDND().next(RETURN, session)
        else:
            speech_output = wrap_with_speak("Pug is in the Net Room. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
