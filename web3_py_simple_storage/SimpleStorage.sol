// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 storedData = 0;

    function retreive() public view returns (uint256) {
        return storedData;
    }

    function set(uint256 x) public {
        storedData = x;
    }
}
