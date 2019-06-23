from ask_sdk_model.services.monetization import (InSkillProductsResponse)
from ask_sdk_model.services.monetization.entitlement_reason import EntitlementReason
from ask_sdk_model.services.monetization.entitled_state import EntitledState
from ask_sdk_model.services.monetization.purchasable_state import PurchasableState
from enum import Enum
import random
from config import *
from session import Session
from state_machine_helpers import *

KEEPER_TRAPPER_PRODUCT_ID = "amzn1.adg.product.3de2c1ce-baba-44ec-a9bb-c2b8fd25acdf"


class ProductName(Enum):
    KEEPER_TRAPPER = "Level 3: Keeper Trapper"


def decorate_and_validate_session_is_purchased(handler_input, session):
    keeper_trapper_purchased = is_product_purchased(handler_input, ProductName.KEEPER_TRAPPER)
    keeper_trapper_purchasable = is_product_purchasable(handler_input, ProductName.KEEPER_TRAPPER)

    session.set_is_keeper_trapper_purchased(keeper_trapper_purchased)
    session.set_is_keeper_trapper_purchasable(keeper_trapper_purchasable)

    if session.get_stored_game_state().startswith("KeeperTrapper"):
        session.set_stored_game_state("EndingState")


def get_product_list(handler_input):
    locale = handler_input.request_envelope.request.locale
    ms = handler_input.service_client_factory.get_monetization_service()
    product_response = ms.get_in_skill_products(locale)

    list_of_products = []
    if isinstance(product_response, InSkillProductsResponse):
        for l in product_response.in_skill_products:
            if l.purchasable:
                list_of_products.append(l)
    return list_of_products


def upsell_return_object(return_object, handler_input, session):
    tsundere_mode_purchased = is_product_purchased(handler_input, ProductName.TSUNDERE_MODE)
    cafe_date_purchased = is_product_purchased(handler_input, ProductName.CAFE_DATE)
    tsundere_mode_purchasable = is_product_purchasable(handler_input, ProductName.TSUNDERE_MODE)
    cafe_date_purchasable = is_product_purchasable(handler_input, ProductName.CAFE_DATE)

    total_number_of_utterances = session.get_total_number_of_utterances()

    if total_number_of_utterances != 5 and \
            (total_number_of_utterances == 0 or total_number_of_utterances % Config.upsell_mod != 0):
        return return_object

    if not tsundere_mode_purchased and tsundere_mode_purchasable and not cafe_date_purchased and cafe_date_purchasable:
        random_choice_index = random.randrange(1, 3)
        if random_choice_index == 1:
            return add_upsell_to_output(return_object,
                                        get_product_id(handler_input, ProductName.TSUNDERE_MODE),
                                        "If you are enjoying talking with Aiko Chan, you can get the Tsundere Mode voice pack. "
                                        "Do you want to learn more?")
        else:
            return add_upsell_to_output(return_object,
                                        get_product_id(handler_input, ProductName.CAFE_DATE),
                                        "If you are enjoying talking with Aiko Chan, you can go on a date with her too! "
                                        "Do you want to learn more?")
    if not tsundere_mode_purchased and tsundere_mode_purchasable and not cafe_date_purchasable:
        return add_upsell_to_output(return_object,
                                    get_product_id(handler_input, ProductName.TSUNDERE_MODE),
                                    "If you are enjoying talking with Aiko Chan, you can get the Tsundere Mode voice pack. "
                                    "Do you want to learn more?")
    if not cafe_date_purchased and cafe_date_purchasable and not tsundere_mode_purchasable:
        return add_upsell_to_output(return_object,
                                    get_product_id(handler_input, ProductName.CAFE_DATE),
                                    "If you are enjoying talking with Aiko Chan, you can go on a date with her too! "
                                    "Do you want to learn more?")
    else:
        return return_object


def is_product_purchasable(handler_input, product_name):
    product_purchasable = False
    product_list = get_product_list(handler_input)
    for product in product_list:
        if product.name == product_name.value and product.purchasable == PurchasableState.PURCHASABLE:
            product_purchasable = True
    return product_purchasable


def is_product_purchased(handler_input, product_name):
    product_purchased = False
    product_list = get_product_list(handler_input)
    for product in product_list:
        if product.name == product_name.value \
                and product.entitled == EntitledState.ENTITLED \
                and product.entitlement_reason is EntitlementReason.PURCHASED:
            product_purchased = True
    return product_purchased


def get_product_id(handler_input, product_name):
    product_list = get_product_list(handler_input)

    for product in product_list:
        if product.name == product_name.value:
            return product.product_id
    return None

