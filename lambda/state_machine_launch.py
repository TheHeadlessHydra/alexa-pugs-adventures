"""
The LaunchRequest is unique in that it must launch the first world. To avoid circular dependencies, it must be isolated
from the common state machine classes.

This file also holds are initializer helper methods used to start the state machine.
"""

from game import *
from state import *
from state_machine_goblin_town import *
from cannot_build_state_machine_exception import *
import sys

class LaunchRequest(State):
    """This is the beginning of the entire game for a user. For now, we start at the piranha paradise visitor center.
    """

    def next(self, input_action, session_state):
        return GoblinTownPugsHome().next(input_action, session_state)

# --------------- State Machine Initializers ------------------

def rebuild_state_machine_from_session(session):
    """Given a session object, will restore the state machine.

    :param session: The session to restore from
    :return: A state machine of what was stored in the session
    """
    print("Initializing state machine with stored session state")

    try:
        print(session)
        stored_game_state = session.get_stored_game_state()
        if stored_game_state == None:
            print("Stored game state is empty, initializing game state from scratch.")
            return initialize_new_state_machine_from_input(session.get_user_id_serializable(), "LaunchRequest")
        print("Restoring game at state: " + str(stored_game_state))
        state_machine = Game(globals()[stored_game_state](), session)
    except:
        message = "Unexpected error getting state machine from SessionState: " + str(sys.exc_info()[0])
        print(message, sys.exc_info()[0])
        raise CannotBuildStateMachineException(message)

    return state_machine


def initialize_new_state_machine_from_input(user_id, input_action):
    """TODO: These end up being just the special ones (launch, help, etc)
    Everything else should start from a state.

    TODO: should think about these cases more. When do they happen? Only launch? What about help? etc
    - StopInput can get here if called first time with no other state
    - LaunchRequest can get here if called first time with no other state
    """

    print("Initializing state machine with with no stored session state, but with input: " + str(input_action))

    try:
        print("Converting " + input_action + " to class")
        state_object = Game(globals()[input_action](), Session(SessionState(user_id)))
    except:
        message = "Unexpected error converting " + str(input_action) + " to a class." + str(sys.exc_info()[0])
        print(message, sys.exc_info()[0])
        raise CannotBuildStateMachineException(message)
    return state_object

"""
The menus need to go here as they require the ability to go back to any level, and the launchers above need them 
as well to return back to them on the next lambda iteration. I can't think of a better way of modularizing this at
the moment.
"""
def initialize_new_options_menu(session):
    return Game(OptionsMenu(), session)

class OptionsMenu(State):
    """The options menu of the game"""
    def next(self, input_action, session):
        card_title = "Options"
        should_end_session = False

        if not session.get_stored_game_state() == self.__class__.__name__:
            session.set_previous_stored_game_state(session.get_stored_game_state())
            session.set_stored_game_state(self.__class__.__name__)

        tldr_what_to_do = \
            "This is the options menu. Right now, all you can do here is completely restart the game. If you " \
            "would like to completely restart the game, say, restart game from scratch. You can also resume the " \
            "game by saying, resume. What would you like to do?"
        reprompt_text = wrap_with_speak(tldr_what_to_do)

        if input_action == COMMON_RESTART_GAME:
            if session.get_event_inventory().exists(Events.common_restart_the_game_are_you_sure):
                session.restart_session()
                save_game(session)
                should_end_session = True
                speech_output = wrap_with_speak("This run has been deleted. The next time you start the game, "
                                                "it will be from the beginning. Thank you for playing.")
            else:
                session.get_event_inventory().add(Events.common_restart_the_game_are_you_sure)
                speech_output = wrap_with_speak(
                    "Restarting the game means losing all progress and being brought back to the beginning "
                    "of the game. This action cannot be undone. If you are sure, say, restart the game from scratch. "
                    "You can also resume the game by saying, resume. What would you like to do?")
        elif input_action == COMMON_RESUME:
            session.get_event_inventory().remove(Events.common_restart_the_game_are_you_sure)
            previous_game_state = session.get_previous_stored_game_state()
            session.set_stored_game_state(previous_game_state)
            state_machine = rebuild_state_machine_from_session(session)
            return state_machine.next(RETURN)
        else:
            speech_output = wrap_with_speak(tldr_what_to_do)

        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)