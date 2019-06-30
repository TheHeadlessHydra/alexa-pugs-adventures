"""
State machine for the keeper trapper world.
"""
from state_machine_common import *
from world import *
from events import *
import logging
from in_skill_purchase import *


class EndingState(State):
    def next(self, input_action, session, handler_input):
        overriding_action = super(EndingState, self).next(input_action, session, handler_input)
        if overriding_action is not None:
            return overriding_action

        should_end_session = False
        card_title = "Ending screen"
        reprompt_text = wrap_with_speak(
            "You are in the end game screen. You really can't do much here other than"
            "open the options menu to restart the game or exit the game. What would you like to do now?")

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            if session.get_is_keeper_trapper_purchased():
                speech_output = wrap_with_speak(
                    "Congratulations! You've completed Pug's Adventures. Thank you very much for playing our game. If you "
                    "enjoyed the game, please leave us a rating or comment. If we see that people enjoyed the game, "
                    "we would love to build out more of Pug's world. You can open up the Options menu by saying open "
                    "options menu. That will let you restart the game anytime. You can also exit the game normally "
                    "by telling Alexa to exit. Really not much else to do here, "
                    "to be honest. Thanks again for playing! What would you like to do now?")
            elif not session.get_is_keeper_trapper_purchased() and session.get_is_keeper_trapper_purchasable():
                return add_upsell_to_output(get_action_response(session, card_title, "", "", should_end_session),
                                            KEEPER_TRAPPER_PRODUCT_ID,
                                            "If you are enjoying the game so far, there is the next level, level 3,"
                                            " KEEPER TRAPPER LLC. Do you want to learn more?")
            else:
                speech_output = wrap_with_speak(
                    "Congratulations! You've completed Pug's Adventures. Thank you very much for playing our game. If you "
                    "enjoyed the game, please leave us a rating or comment. Unfortunately, the next level of Pug's "
                    "adventures, Keeper Trapper LLC, is not available for purchase in your region. "
                    "You can open up the Options menu by saying open "
                    "options menu. That will let you restart the game anytime. You can also exit the game normally "
                    "by telling Alexa to exit. Really not much else to do here, "
                    "to be honest. Thanks again for playing! What would you like to do now?")
        else:
            if session.get_is_keeper_trapper_purchased():
                speech_output = wrap_with_speak(
                    "Welcome back to the ending screen! You can open up the Options menu by saying open "
                    "options menu. That will let you restart the game anytime. We promise there's no secret dialogue "
                    "between Pug and Mad Mage " + Config.mad_mage_name + " or anything. What would you like to do now?")
            elif not session.get_is_keeper_trapper_purchased() and session.get_is_keeper_trapper_purchasable():
                return add_upsell_to_output(get_action_response(session, card_title, "", "", should_end_session),
                                            KEEPER_TRAPPER_PRODUCT_ID,
                                            "Welcome back to the ending screen! If you are enjoying the game so far, "
                                            "there is the next level, level 3, KEEPER TRAPPER LLC. "
                                            "Do you want to learn more?")
            else:
                speech_output = wrap_with_speak(
                    "Welcome back to the ending screen! We are sorry, the next level of Pug's Adventures is not "
                    "available in your region. You can open up the Options menu by saying open "
                    "options menu. That will let you restart the game anytime. We promise there's no secret dialogue "
                    "between Pug and Mad Mage " + Config.mad_mage_name + " or anything. What would you like to do now?")

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)