from brownie import FundMe
from scripts.utils import get_account


def fund():
    account = get_account()
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee()
    print(f"Funding with Entrance Fee: {entrance_fee}")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    account = get_account()
    fund_me = FundMe[-1]
    fund_me.withdraw({"from": account})
    print("Withdrawal complete")


def main():
    fund()
    withdraw()
