from brownie import accounts, SimpleStorage, network, config


def get_account():
    if (network.show_active() == "development"):
        # In case of development network like ganache, use the default accounts
        return accounts[0]
    else:
        # In case of testnet or mainnet, use the account from the config file
        return accounts.add(config["wallets"]["from_key"])


def deploy():
    # Get Account
    account = get_account()

    # Deploy
    simple_storage = SimpleStorage.deploy({
        'from': account,
    })

    # Read value from deployed contract
    print(simple_storage.get())

    # Update value in deployed contract
    simple_storage.set(15, {'from': account})

    # Read update value from deployed contract
    print(simple_storage.get())


def main():
    deploy()
