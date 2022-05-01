from brownie import network, accounts, config, MockV3Aggregator

DECIMAL = 8
INITIAL_PRICE = 2000 * (10**18)
LOCAL_NETWORKS = ["development", "ganache-local"]
MAINNET_FORKS = ["mainnet-fork"]


def in_development():
    return network.show_active() in LOCAL_NETWORKS


def in_mainnet_fork():
    return network.show_active() in MAINNET_FORKS


def get_account():
    if in_development() or in_mainnet_fork:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("Deploying mocks")
    if len(MockV3Aggregator) <= 0:
        account = get_account()
        MockV3Aggregator.deploy(DECIMAL, INITIAL_PRICE, {"from": account})
    print("Mocks deployed")
