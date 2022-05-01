from brownie import FundMe, network, config, MockV3Aggregator
from scripts.utils import deploy_mocks, get_account, in_development


def deploy():
    account = get_account()
    priceFeed = None
    active_network = network.show_active()
    if not in_development():
        priceFeed = config["networks"].get(active_network).get("priceFeed")
    else:
        print("Deploying Mocks")
        deploy_mocks()
        print("Mock deployed")
        priceFeed = MockV3Aggregator[-1].address

    print("Deploying FundMe")
    fund_me = FundMe.deploy(
        priceFeed,
        {
            "from": account
        },
        publish_source=config["networks"][active_network].get("verify")
    )
    print("FundMe deployed")
    return fund_me


def main():
    deploy()
