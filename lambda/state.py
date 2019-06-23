"""
Base class for state

TODO
- Change parent_next to be actual parent next? Then call super?
"""
from world import *
from events import *
from state_machine_helpers import *


class State(object):
    def next(self, input_action, session):

        # Import controls that can happen anywhere
        if input_action == COMMON_DESCRIBE_INVENTORY:
            card_title = "Describe inventory"
            reprompt_text = wrap_with_speak("What should Pug do next?")
            should_end_session = False

            final_speech = "Pug's inventory has the following items:"
            counter = 0
            for item in session.get_item_inventory().get_items():
                # used items are no longer in the inventory
                if (item.is_item_already_used()): continue
                counter += 1
                final_speech = final_speech + " " + get_name_of_item(item.get_item_id()) \
                               + ", " + get_description_of_item(item.get_item_id())
            final_speech = final_speech + " That's everything. What should Pug do next?"
            if (counter == 0):
                final_speech = "Pug's inventory is depressingly empty. What should Pug do next?"
            speech_output = wrap_with_speak(final_speech)
            session.get_event_inventory().add(Events.common_describe_inventory_once)

            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

        # Things the player can do in the game itself that can happen anywhere
        elif input_action == LOST_AND_FOUND_EAT_KALE \
                and session.get_item_inventory().exists(World.druid_kale_snack) \
                and not session.get_event_inventory().exists(Events.attempted_to_eat_kale):
            session.get_event_inventory().add(Events.attempted_to_eat_kale)
            card_title = "Eating kale"
            reprompt_text = wrap_with_speak("What should Pug do next?")
            should_end_session = False
            speech_output = wrap_with_speak(
                "Pug was already feeling queasy simply holding the kale. Yet again, against his better judgement, "
                "Pug takes a bite of one of the Druid's kale bars. It is <emphasis "
                "level=\"reduced\">easily</emphasis> the healthiest thing the Pug has ever eaten. <break "
                "time=\"1s\"/> He promptly vomits. <break time=\"1s\"/> He doesn't know what he expected. "
                "What should Pug do next?")
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
        elif input_action == LOST_AND_FOUND_EAT_KALE \
                and session.get_item_inventory().exists(World.druid_kale_snack) \
                and session.get_event_inventory().exists(Events.attempted_to_eat_kale):
            card_title = "Eating kale again"
            reprompt_text = wrap_with_speak("What should Pug do next?")
            should_end_session = False
            speech_output = wrap_with_speak(
                "Pug remembers the last time he tried to eat kale. It did not go well. He refuses to eat it again. "
                "What would you like to do now?")
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
        elif input_action == KEEPER_TRAPPER_DRINK_COFFEE \
                and session.get_item_inventory().exists(World.keeper_trapper_coffee) \
                and not session.get_item_inventory().is_item_already_used(World.keeper_trapper_coffee):
            card_title = "Drinking coffee"
            reprompt_text = wrap_with_speak("What should Pug do next?")
            should_end_session = False
            speech_output = wrap_with_speak(
                "Pug sniffs the coffee. The aroma smells of rich roasted beans, with an earthy quality. "
                "It reminds Pug of his grandfather, and the days they spent on the Goblin ranch, "
                "playing catch and learning the basics of boot farming. This is truly the best part of waking up. "
                "Pug takes a sip. <break time=\"1s\"/> Nope, nevermind, that tastes like pure acid. "
                "Pug puts the coffee back into his bag. "
                "What should Pug do next?")
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
        elif input_action == KEEPER_TRAPPER_READ_ENVELOPE \
                and session.get_item_inventory().exists(World.keeper_trapper_envelope):
            card_title = "Read envelope"
            reprompt_text = wrap_with_speak("What should Pug do next?")
            should_end_session = False
            if session.get_item_inventory().is_item_already_used(World.keeper_trapper_letter_opener):
                speech_output = wrap_with_speak(
                    "Pug re-reads the letter in the envelope. Inside the letter, it reads: Attention Valued Worker, "
                    "Please take note that the magic word to use the elevator systems has been changed to "
                    "Open Ragamuffin and Close Ragmuffin. Thanks, Maintenance. What should Pug do next?")
            else:
                speech_output = wrap_with_speak(
                    "Pug still cannot open the envelope with his hands, try as he might. Pug thinks a tool might help "
                    "here. What should Pug do next?")
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
        elif input_action == KEEPER_TRAPPER_OPEN_ENVELOPE \
             and session.get_item_inventory().exists(World.keeper_trapper_envelope):
                card_title = "Open envelope"
                reprompt_text = wrap_with_speak("What should Pug do next?")
                should_end_session = False
                if session.get_event_inventory().exists(Events.keeper_trapper_open_envelope):
                    speech_output = wrap_with_speak(
                        "Pug has already opened the envelope. He takes the letter out and reads it again. "
                        "Attention Valued Worker, Please take note that the magic word to use the elevator "
                        "systems has been changed to Open Ragamuffin and Close Ragmuffin. "
                        "Thanks, Maintenance. What should Pug do next?")
                elif session.get_item_inventory().exists(World.keeper_trapper_letter_opener):
                    speech_output = wrap_with_speak(
                        "Pug takes the letter opener plus one and uses it to open the envelope. The colored runes around "
                        "the envelope lose their color and diminish. Inside the letter, it reads: Attention Valued Worker, "
                        "Please take note that the magic word to use the elevator systems has been changed to "
                        "Open Ragamuffin. Thanks, Maintenance. What should Pug do next?")
                    session.get_event_inventory().add(Events.keeper_trapper_open_envelope)
                else:
                    speech_output = wrap_with_speak(
                        "Pug still cannot open the envelope with his hands, try as he might. Pug thinks a tool might help "
                        "here. What should Pug do next?")
                return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
        else:
            return None
