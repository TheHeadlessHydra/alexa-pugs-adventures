"""
The game itself is just an instantiation of a StateMachine
"""
from state_machine import *

class Game(StateMachine):
    def __init__(self, initial_state, session):
        StateMachine.__init__(self, initial_state, session)