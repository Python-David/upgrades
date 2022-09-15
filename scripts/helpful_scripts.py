from brownie import (
    accounts,
    network,
    config,
    # MockV3Aggregator,
    # Contract,
    # VRFCoordinatorMock,
    # LinkToken,
    # interface,
)
from web3 import Web3
import eth_utils

DECIMALS = 8
STARTING_PRICE = 200000000000

FORKED_ENV = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_ENV
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address, encoded_function_call, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from": account})

    return transaction


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


# contract_to_mock = {
#     "eth_usd_price_feed": MockV3Aggregator,
#     "vrf_coordinator": VRFCoordinatorMock,
#     "link_token": LinkToken,
# }


# def get_contract(contract_name):
#     """This function will grab the contract addresses from the brownie config
#     if defined, otherwise, it will deploy a mock version of that contract, and
#     return that mock contract.
#         Args:
#             contract_name (string)
#         Returns:
#             brownie.network.contract.ProjectContract: The most recently deployed
#             version of this contract.
#     """
#     contract_type = contract_to_mock[contract_name]
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         if len(contract_type) <= 0:
#             # MockV3Aggregator.length
#             deploy_mocks()
#         contract = contract_type[-1]
#         # MockV3Aggregator[-1]
#     else:
#         contract_address = config["networks"][network.show_active()][contract_name]
#         # address
#         # ABI
#         contract = Contract.from_abi(
#             contract_type._name, contract_address, contract_type.abi
#         )
#         # MockV3Aggregator.abi
#     return contract


# def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
#     account = get_account()
#     MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
#     link_token = LinkToken.deploy({"from": account})
#     VRFCoordinatorMock.deploy(link_token.address, {"from": account})
#     print("Deployed!")


# def fund_with_link(
#     contract_address, account=None, link_token=None, amount=100000000000000000
# ):  # 0.1 LINK
#     account = account if account else get_account()
#     link_token = link_token if link_token else get_contract("link_token")
#     tx = link_token.transfer(contract_address, amount, {"from": account})

#     # link_token_contract = interface.LinkTokenInterface(link_token.address)
#     # tx = link_token_contract.transfer(contract_address, amount, {"from": account})

#     tx.wait(1)
#     print("Contract funded")

#     return tx
