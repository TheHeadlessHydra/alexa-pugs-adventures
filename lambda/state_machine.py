"""
State machine for the game.

This is meant to work with a lambda function, therefore state is never stored between sessions. This means the state
must be rebuilt on each call. This changes the way the state machine works. Instead of passing the next state along
as a "next state" class, each state "class" must be mapped to a value. That value is stored in the session_state
object and passed back in the request to be carried over to the next lambda call. When the session ends with a call
to AMAZON.StopIntent, the session state is stored in an external store. When a user launches the game the next time,
the state is pulled from the external store and restored back to where they were.

The state holds more than just where the user was, however. It holds a variety of things that are necessary to make
the game work.

State machine concepts pulled from: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html
"""


class StateMachine:
    def __init__(self, initial_state, session):
        self.session = session
        self.current_state = initial_state
        self.list_of_actions = []

    def __str__(self):
        return self.current_state.__class__.__name__

    def get_session(self):
        return self.session

    def next(self, input, handler_input):
        return self.current_state.next(input, self.session, handler_input)
