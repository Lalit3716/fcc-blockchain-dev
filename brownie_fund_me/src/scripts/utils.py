from brownie import network, accounts, config, MockV3Aggregator

DECIMAL = 8
INTIAL_PRICE = 2 * 10 ** DECIMAL
LOCAL_NETWORKS = ["development", "ganache-local"]


def in_development():
    return network.show_active() in LOCAL_NETWORKS


def get_account():
    if in_development():
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMAL, INTIAL_PRICE, {"from": get_account()})
