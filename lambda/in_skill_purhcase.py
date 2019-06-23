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

