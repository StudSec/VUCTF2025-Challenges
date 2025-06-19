pragma solidity 0.8.28;

import {Coin} from "./Coin.sol";
import {Bank} from "./Bank.sol";

contract Setup {
    Coin public coin;
    Bank public bank;

    address player;

    constructor(address _player) {
        player = _player;
        coin = new Coin();
        bank = new Bank(coin);
        coin.approve(address(bank), 10 ether);
        bank.depositFor(address(coin), address(this), 10 ether);
    }

    function isSolved() external view returns (bool) {
        return player != address(0) && coin.balanceOf(player) >= 10 ether;
    }
}
