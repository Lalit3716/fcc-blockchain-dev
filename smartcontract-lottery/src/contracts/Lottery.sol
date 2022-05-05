// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

enum LOTTERY_STATE {
    OPEN,
    CLOSED,
    CALCULATING_WINNER
}

contract Lottery {
    address public owner;
    address public winner;
    uint256 public usdEnterFee;
    address[] public players;
    AggregatorV3Interface public ethUsdPriceFeed;
    LOTTERY_STATE public state;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        usdEnterFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeed);
        state = LOTTERY_STATE.CLOSED;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function enter() public payable {
        require(state == LOTTERY_STATE.OPEN, "Lottery is not open");
        require(msg.value >= getEntranceFee(), "Not enough ETH for ticket fee");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        uint256 costToEnter = (usdEnterFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function getState() public view returns (LOTTERY_STATE) {
        return state;
    }

    function getWinner() public view returns (address) {
        return winner;
    }

    function startLottery() public onlyOwner {
        require(state == LOTTERY_STATE.CLOSED, "Lottery is already open");
        state = LOTTERY_STATE.OPEN;
    }

    function closeLottery() public onlyOwner {
        require(state == LOTTERY_STATE.OPEN, "Lottery is not open");
        require(players.length > 0, "No players entered");
        state = LOTTERY_STATE.CLOSED;
    }

    function calculateWinner() public onlyOwner {
        require(state == LOTTERY_STATE.CLOSED, "Lottery is not closed");
        require(players.length > 0, "No players entered");
        state = LOTTERY_STATE.CALCULATING_WINNER;
        winner = players[0];
    }
}
