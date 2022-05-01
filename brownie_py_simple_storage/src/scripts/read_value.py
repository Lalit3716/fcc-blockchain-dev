from brownie import SimpleStorage


def read_value():
    # In case of TestNet, SimpleStorage is an array with all deployed contracts
    simple_storage = SimpleStorage[-1]
    print(simple_storage.get())


def main():
    read_value()
