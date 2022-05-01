from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({'from': account})

    # Act
    result = simple_storage.get()
    expected = 0

    # Assert
    assert result == expected


def test_set():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({'from': account})
    value = 10

    # Act
    simple_storage.set(value, {'from': account})
    result = simple_storage.get()
    expected = value
    assert result == expected
