// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 store = 0;

    function get() public view returns (uint256) {
        return store;
    }

    function set(uint256 _x) public {
        store = _x;
    }
}
