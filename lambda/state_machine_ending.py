"""
State machine for the keeper trapper world.
"""
from state_machine_common import *
from world import *
from events import *
import logging

class EndingState(State):
    def next(self, input_action, session):
        overriding_action = super(EndingState, self).next(input_action, session)
        if overriding_action is not None:
            return overriding_action

        card_title = Config.goblin_town_name + " Town Center"
        reprompt_text = wrap_with_speak(
            "You are in the end game screen. You really can't do much here other than"
            "open the options menu to restart the game or exit the game. What would you like to do now?")
        should_end_session = False

        if not session.is_location_seen_before(self.__class__.__name__):
            session.new_seen_location(self.__class__.__name__)
            speech_output = wrap_with_speak(
                "Congratulations! You've completed Pug's Adventures. Thank you very much for playing our game. If you "
                "enjoyed the game, please leave us a rating or comment. If we see that people enjoyed the game, "
                "we would love to build out more of Pug's world. You can open up the Options menu by saying open "
                "options menu. That will let you restart the game anytime. You can also exit the game normally "
                "by telling Alexa to exit. Really not much else to do here, "
                "to be honest. Thanks again for playing! What would you like to do now?")
        elif input_action == RETURN:
            speech_output = wrap_with_speak(
                "Welcome back to the ending screen! You can open up the Options menu by saying open "
                "options menu. That will let you restart the game anytime. We promise there's no secret dialogue "
                "between Pug and Mad Mage " + Config.mad_mage_name + " or anything. What would you like to do now?")
        else:
            speech_output = wrap_with_speak("You are in the end game screen. You really can't do much here other than"
                                            "open the options menu to restart the game or exit the game. "
                                            "What would you like to do now?")

        session.set_stored_game_state(self.__class__.__name__)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)