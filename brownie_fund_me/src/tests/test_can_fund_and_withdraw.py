from brownie import accounts, exceptions
from scripts.deploy import deploy
from scripts.utils import get_account, in_development
import pytest


def test_fund():
    account = get_account()
    fund_me = deploy()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(
        account.address) == entrance_fee, "Funding failed"

    assert fund_me.getBalance() == entrance_fee, "Funding failed"

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(
        account.address) == 0, "Withdrawal failed"

    assert fund_me.getBalance() == 0, "Withdrawal failed"


def test_only_owner_can_withdraw():
    if not in_development():
        pytest.skip("This test runs only in development")
    fund_me = deploy()

    bad_actor = accounts.add()
    with pytest.raises(AttributeError):
        fund_me.withdraw({"from": bad_actor})
