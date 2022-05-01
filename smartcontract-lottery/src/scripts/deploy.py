from brownie import Lottery, MockV3Aggregator, config, network
from scripts.utils import get_account, in_development, deploy_mocks, in_mainnet_fork


def deploy():
    account = get_account()
    price_feed = None
    if in_development() and not in_mainnet_fork():
        deploy_mocks()
        price_feed = MockV3Aggregator[-1].address
    else:
        price_feed = config["networks"][network.show_active()]["eth_usd_price_feed"]

    lottery = Lottery.deploy(price_feed, {"from": account})
    return lottery


def main():
    deploy()
