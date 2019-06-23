"""
State machine for the aquarium world.
"""
from state_machine_common import *
from world import *
from events import *
import logging
import random
from state_machine_keeper_trapper import *

logger = logging.getLogger()

class PiranhaParadiseVisitorCenter(State):
    def next(self, input_action, session):
        overriding_action = super(PiranhaParadiseVisitorCenter, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Piranha Paradise Visitors Center"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_item_inventory().exists(World.maintenance_room_key):
            tldr_whats_in_area = "Pug can go to the lost and found or to the aquarium."
            detailed_description = "To the left is a sign marked Lost and Found Corpses. " \
                                   "To the right Pug can enter the park under a banner that says " \
                                   "Piranha Paradise. What should Pug do next?"
        else:
            tldr_whats_in_area = "The goblin who was mopping is still mopping and continues to look dejected. " \
                                 "Pug can go to the lost and found, to the aquarium or talk to the goblin."
            detailed_description = "In front of Pug is a dejected looking goblin with a " \
                                   "mop. To the left is a sign marked Lost and Found Corpses. " \
                                   "To the right Pug can enter the park under a banner that says " \
                                   "Piranha Paradise. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug crawls through the hole with reckless abandon. Eventually, the hole gets too steep and Pug "
                "tumbles through. When Pug lands, he finds himself somewhere completely unlike " + Config.goblin_town_name + ". "
                "The air seems cleaner here and the lights are so much more... fluorescent. "
                "Welcome to Mad Mage " + Config.mad_mage_name + "'s Prize Winning "
                "Aquarium, home to all manner of exotic aquatic life. Two Headed Sharks of the Deep Temple, "
                "Angler Rays, Manticore-of-War and thousands of other deadly sea life inhabit this place. At least "
                "that's what the pamphlet in front of Pug proclaims. It appears that Pug has arrived in the visitor "
                "center for the Aquarium. <break time=\"1s\"/>" + detailed_description)
        elif input_action == RETURN or input_action == LAUNCH_REQUEST or input_action == INITIALIZE:
            speech_output = wrap_with_speak(
                "Pug is back in the piranha paradise visitors center. " + tldr_whats_in_area +
                "  What should Pug do next?")
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(
                "Pug is standing in the lobby of Mad Mage " + Config.mad_mage_name + "'s Prize Winning Aquarium. "
                + detailed_description)
        elif input_action == VISITOR_CENTER_TALK_TO_GOBLIN \
                and not session.get_item_inventory().exists(World.maintenance_room_key):
            session.get_item_inventory().add(World.maintenance_room_key)
            speech_output = wrap_with_speak(
                "As pug approaches the goblin with the mop, the goblin looks up surprised. <prosody "
                "pitch=\"x-low\">Ah! You there! You must be the new transfer! Welcome to the fast paced world of "
                "aquarium maintenance!</prosody>The goblin smiles halfheartedly at Pug.<prosody pitch=\"x-low\"> "
                "Well... that's enough pleasantries. I guess this means my retirement paperwork has finally come "
                "through.</prosody> The goblin throws Pug some keys. <prosody pitch=\"x-low\">If you're lucky like I "
                "was, your relief should show up in two or three hundred years.</prosody> Pug looks at the keys "
                "labeled maintenance and puts them in his bag. Well, wasn't he a nice fellow. What should Pug do "
                "next?")
        elif input_action == COMMON_READ_THE_PAMPHLET:
            random_choice = random.randrange(0, 3)
            if random_choice == 0:
                speech_output = wrap_with_speak(
                    "The albacore (Thunnus alalunga), known also as the longfin tuna, is a species of tuna of the "
                    "order Perciformes. It is found in temperate and tropical waters across the globe in the "
                    "epipelagic and mesopelagic zones. There are six distinct stocks known globally in the Atlantic, "
                    "Pacific, and Indian oceans, as well as the Mediterranean Sea. The albacore has an elongate, "
                    "fusiform body with a conical snout, large eyes, and remarkably long pectoral fins. Its body is a "
                    "deep blue dorsally and shades of silvery white ventrally. Individuals can reach up to 1.4 m (4.6 "
                    "ft) in length. What should Pug do next?")
            elif random_choice == 1:
                speech_output = wrap_with_speak(
                    "Arowanas are freshwater bony fish of the family Osteoglossidae, also known as bonytongues ("
                    "the latter name is now often reserved for Arapaimidae).[2] In this family of fish, the head is "
                    "bony and the elongated body is covered by large, heavy scales, with a mosaic pattern of canals. "
                    "The dorsal and anal fins have soft rays and are long based, while the pectoral and ventral fins "
                    "are small. The name bonytongues is derived from a toothed bone on the floor of the mouth, "
                    "the tongue, equipped with teeth that bite against teeth on the roof of the mouth. The "
                    "arowana is a facultative air breather and can obtain oxygen from air by sucking it into its swim "
                    "bladder, which is lined with capillaries like lung tissue. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Mackerel is a common name applied to a number of different species of pelagic fish, mostly, "
                    "but not exclusively, from the family Scombridae. They are found in both temperate and tropical "
                    "seas, mostly living along the coast or offshore in the oceanic environment. Mackerel typically "
                    "have vertical stripes on their backs and deeply forked tails. Many species are restricted in "
                    "their distribution ranges, and live in separate populations or fish stocks based on geography. "
                    "Some stocks migrate in large schools along the coast to suitable spawning grounds, where they "
                    "spawn in fairly shallow waters. After spawning they return the way they came, in smaller "
                    "schools, to suitable feeding grounds often near an area of upwelling. From there they may move "
                    "offshore into deeper waters and spend the winter in relative inactivity. Other stocks migrate "
                    "across oceans. What should Pug do next?")
        elif input_action == COMMON_GO_LEFT or input_action == VISITOR_CENTER_GOTO_LOST_AND_FOUND:
            return LostAndFoundCorpses().next(INITIALIZE, session)
        elif input_action == COMMON_GO_RIGHT or input_action == VISITOR_CENTER_GOTO_LOST_PIRANHA_PARADISE:
            return PiranhaParadiseAquarium().next(INITIALIZE, session)
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session)
        else:
            speech_output = wrap_with_speak(
                "Pug is in the visitors center for the aquarium. " + tldr_whats_in_area
                + " What should Pug do next?")

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


# --------------- Lost and found ------------------

class LostAndFoundCorpses(State):
    def next(self, input_action, session):
        overriding_action = super(LostAndFoundCorpses, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Lost and found corpses"
        reprompt_text = wrap_with_speak("What would Pug do next?")
        should_end_session = False

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug finds himself in the Lost and Found Corpses department, where a bunch of half eaten corpses are "
                "stacked. Deep within himself, Pug feels an urge to start de booting the bodies. Fortunately, "
                "he was able to contain his urges and stop himself. He has something more important to do. Two "
                "bodies seem to still be intact. Pug see the body of a Ranger with a Sabrefish stuck through him. Pug "
                "sees a Druid riddled with bites and a few particularly tenacious piranhas still clamped onto her cold "
                "arms and legs. Pug can inspect the ranger, the druid, or leave the room back to the Visitor Center. "
                "What should Pug do next?")
        elif input_action == RETURN or input_action == INITIALIZE or input_action == LAUNCH_REQUEST:
            speech_output = wrap_with_speak(
                "Pug is standing in front of the two dead bodies. Pug can inspect the ranger, "
                "the druid, or leave back to the Visitor Center. What should Pug do next?")
        elif input_action == COMMON_GO_BACK or \
                input_action == COMMON_EXIT_THE_ROOM or \
                input_action == VISITOR_CENTER_GO_BACK:
            return PiranhaParadiseVisitorCenter().next(RETURN, session)
        elif input_action == LOST_AND_FOUND_INSPECT_RANGER:
            return RangerCorpse().next(RETURN, session)
        elif input_action == LOST_AND_FOUND_INSPECT_DRUID:
            return DruidCorpse().next(RETURN, session)
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(
                 "Pug finds himself in the Lost and Found Corpses department, where a bunch of half eaten corpses are "
                "stacked. Deep within himself, Pug felt an urge to start de booting the bodies. Fortunately, "
                "he was able to contain his urges and stop himself. He has something more important to do. Two "
                "bodies seem to still be intact. Pug sees the body of a Ranger with a Sabrefish stuck through him. Pug "
                "sees a Druid riddled with bites and a few particularly tenacious piranhas still clamped onto her cold "
                "arms and legs. Pug can inspect the ranger, the druid, or leave the room back to the Visitor Center. "
                 "What should Pug do next?")
        else:
            speech_output = wrap_with_speak(
                "Pug can inspect the ranger, the druid, or leave the room back to the Visitor Center. "
                "What should Pug do next?")

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class RangerCorpse(State):
    def next(self, input_action, session):
        overriding_action = super(RangerCorpse, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Corpse of a Ranger"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can attempt to take the fish, take the bow or go back and look at the other bodies."
        if session.get_item_inventory().exists(World.ranger_stiff_fish) \
                and session.get_event_inventory().exists(Events.attempted_to_take_bow):
            tldr_whats_in_area = "There is nothing left to do here. What should Pug do next?"
        elif session.get_item_inventory().exists(World.ranger_stiff_fish) \
                and not session.get_event_inventory().exists(Events.attempted_to_take_bow):
            tldr_whats_in_area = "Pug can attempt to take the bow or go back and look at the other bodies."
        elif not session.get_item_inventory().exists(World.ranger_stiff_fish) \
                and session.get_event_inventory().exists(Events.attempted_to_take_bow):
            tldr_whats_in_area = "Pug can attempt to take the fish or go back and look at the other bodies."

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "A young elf Ranger seems to have met his end here in the Aquarium. Overall, he seems to be quite "
                "well put together. Well, other than the three foot long Sabrefish piercing his chest. In his hand "
                "he has a bow. Pug can attempt to take the fish, take the bow or go back and look at the other bodies. "
                "What should Pug do next?")
        elif input_action == RETURN or input_action == INITIALIZE or input_action == LAUNCH_REQUEST:
            speech_output = wrap_with_speak(
                "Pug is back at the dead ranger. " + tldr_whats_in_area + " What should Pug do next?")
        elif input_action == COMMON_GO_BACK or input_action == LOST_AND_FOUND_LOOK_AT_OTHER_BODIES:
            return LostAndFoundCorpses().next(RETURN, session)
        elif input_action == LOST_AND_FOUND_INSPECT_DRUID:
            return DruidCorpse().next(RETURN, session)
        elif input_action == LOST_AND_FOUND_TAKE_FISH and not session.get_item_inventory().exists(
                World.ranger_stiff_fish):
            session.get_item_inventory().add(World.ranger_stiff_fish)
            speech_output = wrap_with_speak(
                "Like the legends of king arthur, Pug heroically grabs the tail of the fish and pulls it straight out "
                "of the elf. It seems that rigor mortis may have set in for the fish. All the better, this could be "
                "quite the useful weapon. What should Pug do next?")
        elif input_action == COMMON_TAKE_BOOTS:
            speech_output = wrap_with_speak(
                "No, it's probably better to quit cold turkey. What should Pug do next?")
        elif input_action == LOST_AND_FOUND_TAKE_BOW and not session.get_event_inventory().exists(
                Events.attempted_to_take_bow):
            session.get_item_inventory().add(Events.attempted_to_take_bow)
            speech_output = wrap_with_speak(
                "Pug pulls the bow from the hands of the ranger. He stares at the bow for a few seconds. <break "
                "time=\"1s\"/> He suddenly realizes he shouldn't have spent all those years in the Goblin Scouts "
                "trying to perfect the craft of blowdarts. He has no idea how to use a bow. Pug puts the bow down. "
                "What should Pug do next?")
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(
                "A young elf Ranger seems to have met his end here in the Aquarium. Overall, he seems to be quite "
                "well put together. " + tldr_whats_in_area + " What should Pug do next?")
        else:
            speech_output = wrap_with_speak(
                "Pug stands in front of a dead ranger. " + tldr_whats_in_area + " What should Pug do next?")

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class DruidCorpse(State):
    def next(self, input_action, session):
        overriding_action = super(DruidCorpse, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Corpse of a Druid"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_whats_in_area = "Pug can take the satchel or look at the other bodies. What should Pug do next?"

        if session.get_event_inventory().exists(Events.druid_look_at_satchel) \
                and not session.get_item_inventory().exists(World.druid_kale_snack):
            tldr_whats_in_area = "The satchel with that terrible kale snack sits on the floor. What should Pug do next?"
        elif session.get_event_inventory().exists(Events.druid_look_at_satchel) \
                and session.get_item_inventory().exists(World.druid_kale_snack):
            tldr_whats_in_area = "There is nothing left to do here. What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "A druid lies in front of Pug who seems to have been the victim of a school of ravenous piranhas. It "
                "seems just about everything of value has been nibbled apart, except for her satchel. The satchel is "
                "embroidered with sunflowers and reads <break time=\"1s\"/>MEAT IS MURDER. If only "
                "the piranhas had the same outlook on life. Pug can take the satchel or look at the other bodies. "
                "What should Pug do next?")
        elif input_action == RETURN or input_action == INITIALIZE or input_action == LAUNCH_REQUEST:
            speech_output = wrap_with_speak(
                "Pug is back at the dead druid. " + tldr_whats_in_area)
        elif input_action == COMMON_GO_BACK or input_action == LOST_AND_FOUND_LOOK_AT_OTHER_BODIES:
            return LostAndFoundCorpses().next(RETURN, session)
        elif input_action == LOST_AND_FOUND_INSPECT_DRUID:
            return DruidCorpse().next(RETURN, session)
        elif input_action == LOST_AND_FOUND_TAKE_SATCHEL \
                and not session.get_event_inventory().exists(Events.druid_look_at_satchel):
            session.get_item_inventory().add(World.charm_animal_scroll)
            session.get_event_inventory().add(Events.druid_look_at_satchel)
            speech_output = wrap_with_speak(
                "Pug pulls the satchel from the Druid, and looks inside. The first thing he finds is a handful of "
                "Vegan pamphlets and kale snack bars. Knowing kale to be basically poison to all manner of goblins, "
                "Pug digs deeper until finally he finds something useful, a magical scroll of "
                "<break time=\"1s\"/>charm animal. Pug hastily puts it into his own pack and puts the satchel "
                "back down. What should Pug do next?")
        elif input_action == LOST_AND_FOUND_TAKE_KALE and not session.get_item_inventory().exists(
                World.druid_kale_snack):
            session.get_item_inventory().add(World.druid_kale_snack)
            speech_output = wrap_with_speak(
                "Against his better judgement, Pug takes a few Kale bars and puts them into his bag. "
                "What should Pug do next?")
        elif input_action == COMMON_TAKE_BOOTS:
            speech_output = wrap_with_speak(
                "No, it's probably better to quit cold turkey. What should Pug do next?")
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak(
                "A druid lies in front of Pug who seems to have been the victim of a school of ravenous piranhas. It "
                "seems just about everything of value has been nibbled apart, except for her satchel. The satchel is "
                "embroidered with sunflowers and reads <break time=\"1s\"/>MEAT IS MURDER. If only "
                "the piranhas had the same outlook on life. " + tldr_whats_in_area)
        else:
            speech_output = wrap_with_speak(
                "Pug stands in front of the dead druid. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


# --------------- Piranha paradise aquarium ------------------

class PiranhaParadiseAquarium(State):
    def next(self, input_action, session):
        overriding_action = super(PiranhaParadiseAquarium, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Piranha Paradise Aquarium"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug steps out of the visitors center and into the brightly colored aquarium and sees three thirty "
                "foot tall fish tanks on either side of him. Each is filled to the brim with thousands of razor "
                "toothed piranhas. To the left is a ladder that leads up above the tank. To the right is a door "
                "marked maintenance. What should Pug do next?")
        elif input_action == RETURN or input_action == INITIALIZE or input_action == LAUNCH_REQUEST:
            if not session.get_event_inventory().exists(Events.piranhas_all_gone):
                speech_output = wrap_with_speak(
                    "Pug is back in the aquarium. He eyes the piranhas suspiciously. To the left is a ladder that "
                    "leads up above the tank. To the right is a door marked maintenance. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug is back in the aquarium. The piranhas in the tank are still very much dead. To the left is a "
                    "ladder that leads up above the tank. To the right is a door marked maintenance. "
                    "What should Pug do next?")
        elif input_action == VISITOR_CENTER_GO_BACK or input_action == COMMON_GO_BACK:
            return PiranhaParadiseVisitorCenter().next(RETURN, session)
        elif input_action == COMMON_GO_LEFT or input_action == AQUARIUM_GO_UP_LADDER:
            return AquariumOnTopOfTheTank().next(RETURN, session)
        elif (input_action == COMMON_GO_RIGHT or input_action == AQUARIUM_GO_TO_MAINTENANCE_ROOM or
              input_action == COMMON_OPEN_THE_DOOR) \
                and session.get_item_inventory().exists(World.maintenance_room_key):
            return MaintenanceSwitchboard().next(RETURN, session)
        elif input_action == COMMON_GO_RIGHT or input_action == AQUARIUM_GO_TO_MAINTENANCE_ROOM or \
                input_action == COMMON_OPEN_THE_DOOR:
            if session.get_item_inventory().exists(World.maintenance_room_key):
                return SessionEndedRequest().next(input_action, session)
            else:
                speech_output = wrap_with_speak(
                    "Pug heads to the door and tries to open it, however the door is locked and he "
                    "cannot go any further. "
                    "What should Pug do next?")
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            if session.get_event_inventory().exists(Events.piranhas_all_gone):
                speech_output = wrap_with_speak(
                    "Pug is in the brightly colored aquarium and sees three thirty foot tall fish tanks on either "
                    "side of him. Each is filled to the brim with thousands of very dead piranhas. Pug still feels a "
                    "bit bad about that. To the left is a ladder that leads up above the tank. To the right is a door "
                    "marked maintenance. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug is in the brightly colored aquarium and sees three thirty foot tall fish tanks on either "
                    "side of him. Each is filled to the brim with thousands of razor toothed piranhas. To the left is "
                    "a ladder that leads up above the tank. To the right is a door marked maintenance. "
                    "What should Pug do next?")
        else:
            speech_output = wrap_with_speak(
                "To the left is a ladder that leads up above the tank. To the right is a door marked maintenance. "
                "What should Pug do next?")

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class AquariumOnTopOfTheTank(State):
    def next(self, input_action, session):
        overriding_action = super(AquariumOnTopOfTheTank, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "On top of the tank"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        if session.get_event_inventory().exists(Events.piranhas_all_gone):
            tldr_whats_in_area = "All the piranhas are dead and floating in the tank. The way to the exit is clear. " \
                                 "What should Pug do next?"
            detailed_description = "The tank is long, with florescent lights that keep the aquarium well lit. " \
                                   "It seems that one of the lights above the tank is shorting out, " \
                                   "sending sparks into the tank below it. Below, in the water, past the thousands " \
                                   "of very dead piranha corpses, Pug can see a bright neon sign exclaiming " \
                                   "DUNGEON EXIT. What should Pug do next?"
        else:
            tldr_whats_in_area = "Above the tank is a large light source hanging by a suspiciously thin thread, " \
                                 "and in the tank is a school of piranhas. What should Pug do next?"
            detailed_description = "The tank is long, with florescent lights that keep the aquarium well lit. " \
                                   "It seems that one of the lights above the tank is shorting out, " \
                                   "sending sparks into the tank below it. Below, in the water, past the thousands " \
                                   "of hungry piranhas, Pug can see a bright neon sign exclaiming DUNGEON EXIT. " \
                                   "What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Pug climbs the ladder to the top of the tank. " + detailed_description)
        elif input_action == RETURN or input_action == INITIALIZE or input_action == LAUNCH_REQUEST:
            speech_output = wrap_with_speak(
                "Pug is back on top of the tank. " + tldr_whats_in_area)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak("Pug is on top of the tank " + detailed_description)
        elif input_action == COMMON_GO_BACK \
                or input_action == AQUARIUM_GO_DOWN_LADDER \
                or input_action == AQUARIUM_GO_BACK:
            return PiranhaParadiseAquarium().next(RETURN, session)
        elif input_action == AQUARIUM_INSPECT_THE_LIGHT:
            speech_output = wrap_with_speak(
                "A light is above the aquarium; hanging by a precariously thin wire. Pug thinks that if only he could "
                "cut the wire, those piranhas might get a shockingly good time. Or he's thinking about what ladybugs "
                "taste like. Who knows. He's a goblin. What should Pug do next?")
        elif input_action == AQUARIUM_ENTER_WATER:
            if session.get_event_inventory().exists(Events.piranhas_all_gone):
                return KeeperTrapperExecutiveWashroom().next(RETURN, session)
            else:
                speech_output = wrap_with_speak(
                    "Pug dips a toe into the water, which immediately begins getting bitten by ravenous piranhas. "
                    "OUCH! Well, that's certainly the last time Pug will be listening to you. "
                    "What should Pug do next?")
        elif input_action == AQUARIUM_CUT_THE_LIGHT and not session.get_event_inventory().exists(
                Events.piranhas_all_gone):
            if session.get_item_inventory().exists(World.ranger_stiff_fish):
                session.get_event_inventory().add(Events.piranhas_all_gone)
                session.get_item_inventory().mark_item_as_used(World.ranger_stiff_fish)
                speech_output = wrap_with_speak(
                    "Pug pulls out the Saberfish and cuts through the wire, sending the light into the piranha tank. "
                    "With a large spark of electricity, millions of volts went through the water, "
                    "killing all the piranhas inside. After a minute, the light finally dies, "
                    "and the water looks safe to cross. "
                    "What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug tried to jump up to the light to cut it. He jumps a measly 1 foot, getting nowhere near the "
                    "light. <break time=\"1s\"/> He suddenly realizes he should have joined the Goblin Scouts "
                    "basketball team. Maybe he could have jumped higher. What should Pug do next?")
        elif input_action == AQUARIUM_CHARM_PIRANHAS and session.get_item_inventory().exists(World.charm_animal_scroll):
            if session.get_item_inventory().is_item_already_used(World.charm_animal_scroll):
                speech_output = wrap_with_speak(
                    "Pug has already tried to charm the pirnahas and does not want to cast the spell thousands of "
                    "times for each piranha. He refuses to charm any more pirnahas. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug pulls out the magic scroll and casts charm animal. Unfortunately, this version of charm "
                    "animal seems to only affect one fish at a time. So, while one of the 3,000 or so piranhas seems "
                    "particularly enamoured with Pug, the others aren't quite as amused. What should Pug do next?")
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session)
        else:
            speech_output = wrap_with_speak(
                "Pug is above the tank. " + tldr_whats_in_area)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class MaintenanceSwitchboard(State):
    def next(self, input_action, session):
        overriding_action = super(MaintenanceSwitchboard, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = "Maintenance Room"
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False

        tldr_description = "Pug can pull on one of the three levers, press the drain button, " \
                           "press the scream button, look at the camera, or leave maintenance. What should Pug do next?"
        detailed_description = \
            "At this panel, there are three sections. The first section is labeled 'drainage'. " \
            "The second section is labeled 'camera controls'. The third " \
            "section has a single button labeled 'scream'. The first section seems the most interesting. " \
            "There are three light bulbs under three levers with a single button underneath them all marked DRAIN. " \
            "Maybe pulling the levers in the correct sequence will do something? What should Pug do next?"

        if not session.is_location_seen_before(self.__class__.__name__):
            speech_output = wrap_with_speak(
                "Pug pulls out the key given to him by the kind goblin, and opens the door. Inside, Pug sees a "
                "switch board filled with levers and switches. "
                + detailed_description)
            session.get_event_inventory().add(Events.aquarium_maintenance_room_light1_on)
            session.get_event_inventory().add(Events.aquarium_maintenance_room_light3_on)
            session.new_seen_location(self.__class__.__name__)
        elif input_action == INITIALIZE or input_action == RETURN or input_action == LAUNCH_REQUEST:
            speech_output = wrap_with_speak("Pug is staring at the switchboard again. What should Pug do next?")
        elif input_action == COMMON_GO_BACK:
            return PiranhaParadiseAquarium().next(RETURN, session)
        elif input_action == COMMON_DESCRIBE_AREA_AGAIN:
            speech_output = wrap_with_speak("Pug is in front of the complicated panel. " + detailed_description)
        elif input_action == SWITCHBOARD_PULL_LEVER_ONE:
            speech = "Pug pulls on the first lever. "

            # First light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light1_on):
                speech = speech + " The first light turns off."
                session.get_event_inventory().remove(Events.aquarium_maintenance_room_light1_on)
            else:
                speech = speech + " The first light turns on."
                session.get_event_inventory().add(Events.aquarium_maintenance_room_light1_on)

            # Second light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light2_on):
                speech = speech + " The second light turns off."
                session.get_event_inventory().remove(Events.aquarium_maintenance_room_light2_on)
            else:
                speech = speech + " The second light turns on."
                session.get_event_inventory().add(Events.aquarium_maintenance_room_light2_on)

            # Third light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light3_on):
                speech = speech + " The third light turns off."
                session.get_event_inventory().remove(Events.aquarium_maintenance_room_light3_on)
            else:
                speech = speech + " The third light turns on."
                session.get_event_inventory().add(Events.aquarium_maintenance_room_light3_on)

            speech = speech + " What should Pug do next?"
            speech_output = wrap_with_speak(speech)
        elif input_action == SWITCHBOARD_PULL_LEVER_TWO:
            speech = "Pug pulls on the second lever. "

            # Second light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light2_on):
                speech = speech + " The second light turns off."
                session.get_event_inventory().remove(Events.aquarium_maintenance_room_light2_on)
            else:
                speech = speech + " The second light turns on."
                session.get_event_inventory().add(Events.aquarium_maintenance_room_light2_on)

            # Third light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light3_on):
                speech = speech + " The third light turns off."
                session.get_event_inventory().remove(Events.aquarium_maintenance_room_light3_on)
            else:
                speech = speech + " The third light turns on."
                session.get_event_inventory().add(Events.aquarium_maintenance_room_light3_on)

            speech = speech + " What should Pug do next?"
            speech_output = wrap_with_speak(speech)
        elif input_action == SWITCHBOARD_PULL_LEVER_THREE:
            speech = "Pug pulls on the third lever. "

            # Third light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light3_on):
                speech = speech + " The third light turns off."
                session.get_event_inventory().remove(Events.aquarium_maintenance_room_light3_on)
            else:
                speech = speech + " The third light turns on."
                session.get_event_inventory().add(Events.aquarium_maintenance_room_light3_on)

            speech = speech + " What should Pug do next?"
            speech_output = wrap_with_speak(speech)
        elif input_action == SWITCHBOARD_PUSH_BUTTON:
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light1_on) \
                    and session.get_event_inventory().exists(Events.aquarium_maintenance_room_light2_on) \
                    and session.get_event_inventory().exists(Events.aquarium_maintenance_room_light3_on):
                if session.get_event_inventory().exists(Events.piranhas_all_gone):
                    speech_output = wrap_with_speak(
                        "Pug mashes the bright button marked drain. Again. The tank drains. Again. "
                        "But there is nothing left to mercilessly kill. You monster. What should Pug do next?")
                else:
                    speech_output = wrap_with_speak(
                        "Pug mashes the bright button marked drain, causing a loud whirring sound. The water in the tanks "
                        "begin draining. Pug's ear twitches. It's as if thousands of fish all cried out in terror and were "
                        "suddenly flushed. After a few moments, water fills the tank up again. All that's left in the tank"
                        "are thousands of dead piranhas. It looks quite eerie. What should Pug do next?")
                session.get_event_inventory().add(Events.piranhas_all_gone)
            else:
                speech_output = wrap_with_speak(
                    "Pug mashes the bright button marked drain. The lights flicker at Pug, as if laughing at his "
                    "attempt to solve the puzzle. Pug thinks hard. Nothing comes up. Looks like you're on your own "
                    "for this one. What should Pug do next?")
        elif input_action == SWITCHBOARD_CHECK_LIGHTS or input_action == AQUARIUM_INSPECT_THE_LIGHT:
            speech = "Pug looks at the lights. "

            # First light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light1_on):
                speech = speech + " The first light is on."
            else:
                speech = speech + " The first light is off."

            # Second light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light2_on):
                speech = speech + " The second light is on."
            else:
                speech = speech + " The second light is off."

            # Third light
            if session.get_event_inventory().exists(Events.aquarium_maintenance_room_light3_on):
                speech = speech + " The third light is on."
            else:
                speech = speech + " The third light is off."

            speech = speech + " What should Pug do next?"
            speech_output = wrap_with_speak(speech)
        elif input_action == SWITCHBOARD_CAMERA_CONTROLS:
            speech_output = wrap_with_speak(
                "In the monitor, Pug sees a section of the park marked GNAWS TANK. It looks like there is a huge "
                "creature in the waters below the tanks. What should Pug do next?")
        elif input_action == SWITCHBOARD_PUSH_SCREAM_BUTTON:
            speech_output = wrap_with_speak(
                "Pug pushes the button labelled scream. In the distance, he can hear the sound of someone screaming. "
                "Entertaining, but not very useful. What should Pug do next?")
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session)
        else:
            speech_output = wrap_with_speak("Pug is in the maintenance room. " + tldr_description)

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
