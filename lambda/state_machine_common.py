"""
All states that can be transitioned to from a level.
"""
from game import *
from state import State
from state_machine_helpers import *

class SessionEndedRequest(State):
    def next(self, input_action, session, handler_input):
        card_title = "See you next time!"
        speech_output = wrap_with_speak("Bye")
        reprompt_text = ""
        should_end_session = True
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class StopIntent(State):
    def next(self, input_action, session, handler_input):
        return SessionEndedRequest().next(input_action, session)


class CancelIntent(State):
    def next(self, input_action, session, handler_input):
        return SessionEndedRequest().next(input_action, session)


class HelpIntent(State):
    """When a user asks for help"""
    def next(self, input_action, session, handler_input):
        card_title = "Help"
        speech_output = wrap_with_speak(
            "You play the game by telling Pug what to do next. You can skip some dialogue by saying your launch word. "
            "You can describe the area again to get more information by saying, "
            "describe area again. You can list Pugs inventory by saying, describe Pug's inventory. "
            "You can open the settings by saying, Open settings. So, what should Pug do next?")
        reprompt_text = wrap_with_speak("What should Pug do next?")
        should_end_session = False
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class NotUnderstood(State):
    """When something bad happened in the game and we cannot continue
    """
    def next(self, input_action, session, handler_input):
        card_title = "Internal failure"
        speech_output = wrap_with_speak("A problem occurred with the game and it cannot continue. We are "
                                        "sorry for the inconvenience. Report this to us at info@crossfade.gg")
        reprompt_text = ""
        should_end_session = True
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

def initialize_new_game_not_understood():
    return Game(NotUnderstood(), Session(SessionState(None)))

def initialize_new_stop_game(session):
    return Game(SessionEndedRequest(), session)

def initialize_new_help_game(session):
    return Game(HelpIntent(), session)