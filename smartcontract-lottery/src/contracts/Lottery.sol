// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address public owner;
    address public winner;
    uint256 public usdEnterFee;
    address[] public players;
    AggregatorV3Interface public ethUsdPriceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        usdEnterFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeed);
    }

    function enter() public payable {
        require(msg.value >= getEntranceFee(), "Not enough ETH for ticket fee");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        uint256 costToEnter = (usdEnterFee * 10**18) / adjustedPrice;
        return costToEnter;
    }
}
