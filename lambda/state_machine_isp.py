from state import State
from state_machine_keeper_trapper import KeeperTrapperExecutiveWashroom
from state_machine_helpers import *
from state_machine_common import *
from in_skill_purchase import *


class InitializeWhatCanBePurchased(State):
    def next(self, input_action, session, handler_input):
        card_title = "What can be bought"

        if is_product_purchasable(handler_input, ProductName.KEEPER_TRAPPER):
            speech_output = wrap_with_speak("You can purchase level 3, Keeper Trapper LLC. "
                                            "Going back to Pug, what should he do next?")
        else:
            speech_output = wrap_with_speak("Nothing can be purchased at the moment. "
                                            "Going back to Pug, what should he do next?")

        reprompt_text = "What should Pug do next?"
        should_end_session = False
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhatsBeenPurchased(State):
    def next(self, input_action, session, handler_input):
        card_title = "What has been bought"

        if is_product_purchased(handler_input, ProductName.KEEPER_TRAPPER):
            speech_output = wrap_with_speak("Level 3: Keeper Trapper has been purchased. "
                                            "Going back to Pug, what should he do next?")
        else:
            speech_output = wrap_with_speak("You have not purchased anything. "
                                            "Going back to Pug, what should he do next?")

        reprompt_text = "What should Pug do next?"
        should_end_session = False
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeMoreAboutKeeperTrapper(State):
    def next(self, input_action, session, handler_input):
        card_title = "More about Keeper Trapper"
        speech_output = wrap_with_speak("Level 3: Keeper Trapper LLC is a much more complicated level, full of "
                                        "puzzles, traps, and odd characters. Pug clearly can't handle it."
                                        " Going back to Pug, what should he do next?")
        reprompt_text = "What should Pug do next?"
        should_end_session = False
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhatsFreeVsPaid(State):
    def next(self, input_action, session, handler_input):
        card_title = "What's free and what's not"
        speech_output = wrap_with_speak("Level 1 and level 2 of the game is free, and level 3: Keeper Trapper "
                                        "is premium content. Going back to Pug, what should he do next?")
        reprompt_text = "What should Pug do next?"
        should_end_session = True
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeBuyKeeperTrapper(State):
    def next(self, input_action, session, handler_input):
        card_title = "Buy Keeper Trapper"
        product_id = get_product_id(handler_input, ProductName.KEEPER_TRAPPER)

        if product_id is not None:
            speech_output = wrap_with_speak("")
            reprompt_text = ""
            should_end_session = True
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session,
                                       buy_product_id=product_id)
        else:
            speech_output = wrap_with_speak(
                "I am sorry. That product is not available for purchase. What should Pug do next?"
            )
            reprompt_text = "What should Pug do next?"
            should_end_session = False
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeReturnKeeperTrapper(State):
    def next(self, input_action, session, handler_input):
        card_title = "Return Keeper Trapper"
        product_id = get_product_id(handler_input, ProductName.TSUNDERE_MODE)

        if product_id is not None:
            speech_output = wrap_with_speak("")
            reprompt_text = ""
            should_end_session = True
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session,
                                       cancel_product_id=product_id)
        else:
            speech_output = wrap_with_speak(
                "You have not purchased Level 3: Keeper Trapper. It does not need to be returned."
                " What should Pug do next?"
            )
            reprompt_text = "What should Pug do next?"
            should_end_session = False
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class DirectiveResponseBuyKeeperTrapper(State):
    def next(self, input_action, session, handler_input):
        card_title = "Buying Keeper Trapper"

        if input_action == "ACCEPTED":
            return KeeperTrapperExecutiveWashroom().next(input_action, session, handler_input)
        elif input_action == "ALREADY_PURCHASED":
            speech_output = wrap_with_speak("You've already purchased Keeper Trapper. What should Pug do next?")
        elif input_action == "DECLINED":
            speech_output = wrap_with_speak("Welcome back. What should Pug do next?")
        else:
            speech_output = wrap_with_speak("What should Pug do next?")

        reprompt_text = "What should Pug do next?"
        should_end_session = False
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class DirectiveResponseCancelKeeperTrapper(State):
    def next(self, input_action, session, handler_input):
        card_title = "Refund Keeper Trapper"

        if input_action == "ACCEPTED":
            speech_output = wrap_with_speak("What should Pug do next?")
        elif input_action == "ALREADY_PURCHASED":
            speech_output = wrap_with_speak("You've already purchased Keeper Trapper. What should Pug do next?")
        else:
            speech_output = wrap_with_speak("Welcome back. What should Pug do next?")

        reprompt_text = "What should Pug do next?"
        should_end_session = False
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
