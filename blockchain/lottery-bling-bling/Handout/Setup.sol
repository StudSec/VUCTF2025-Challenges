pragma solidity 0.8.28;

import {LotteryBlingBling} from "./LotteryBlingBling.sol";

contract Setup {
    LotteryBlingBling public lotteryBlingBling;

    address player;

    constructor(address _player) payable {
        require(msg.value == 101 ether, "Setup: Invalid ether amount");
        player = _player;

        lotteryBlingBling = new LotteryBlingBling(1 ether);

        for (uint256 i = 0; i < 50; i++) {
            lotteryBlingBling.buyTicket{value: 1 ether}();
        }

        player.call{value: 1 ether}("");
    }

    function isSolved() external view returns (bool) {
        return player != address(0) && address(player).balance > 50 ether; // won the JACKPOT
    }
}
