import requests

from stellar_sdk.asset import Asset
from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.operation.manage_sell_offer import ManageSellOffer
from stellar_sdk.server import Server
from stellar_sdk.transaction_builder import TransactionBuilder

import json

# Preparation
## Configure Stellar SDK to talk to the horizon instance hosted by Stellar.org
## To use the live network, set the hostname to 'https://horizon.stellar.org'
server = Server(horizon_url="https://horizon-testnet.stellar.org")
## Use test network, if you need to use public network,
## please set it to `Network.PUBLIC_NETWORK_PASSPHRASE`
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
## Max fee you're willing to pay per operation in this transaction (**in stroops**).
base_fee = 100

## Create seller account
print("Create Seller Account:")
#seller_keys = "SAHSDPH6RD2IBUX3TVAJ4E6VIM6EVUXDYH72ZL4VRLAXTEBF7ZPRE4SU"
seller_secret_key = "SAHSDPH6RD2IBUX3TVAJ4E6VIM6EVUXDYH72ZL4VRLAXTEBF7ZPRE4SU"
seller_public_key = "GADJC34B5SLXJHPAL3BMZAILZOHZNS6OENDOO5EII2D5YOS4RC4CJG25"
print(f"Seller Account Secret Key: {seller_secret_key}")
print(f"Seller Account Public Key: {seller_public_key}")

friendbot_url = "https://friendbot.stellar.org"


response1 = requests.get(friendbot_url, params={"addr": seller_public_key})

print(response1)

seller_account = server.load_account(account_id=seller_public_key)

awesome_asset_coin = Asset("AAC", seller_public_key)


# create sell offer
print("Create Sell Offer")


lumen = Asset("XLM", issuer=None)


amount = "10"
price = "0.5"

sell_offer_transaction = (
    TransactionBuilder(
        source_account=seller_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_manage_sell_offer_op(
        selling=awesome_asset_coin, buying=lumen, amount=amount, price=price
    )
    .set_timeout(30)
    .build()
)


sell_offer_transaction.sign(seller_secret_key)
sell_offer_transaction_resp = server.submit_transaction(sell_offer_transaction)
print("Sell offer created\n")
    
## get offer
print("Get Offer:")
list_amount = []
offers = server.offers().for_selling(lumen).call()
for offer in offers["_embedded"]["records"]:
    print(
        f"ID: {offer['id']}\nSeller: {offer['seller']} \
          \nSelling: {offer['buying']['asset_code']} \
          \nAmount: {offer['amount']}\nPrice: {offer['price']}"
    )
    list_amount.append((offer['amount'],offer['price']))
    offer_id = offer["id"]

print("#" * 30)
print(list_amount)

