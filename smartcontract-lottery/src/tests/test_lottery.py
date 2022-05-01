from brownie import Lottery
from scripts.deploy import deploy
from web3 import Web3


def test_entrance_fee():
    lottery = deploy()
    assert lottery.getEntranceFee() > Web3.toWei(0.017, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")
