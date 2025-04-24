pragma solidity 0.8.28;

import {ShadowEmergency} from "./ShadowEmergency.sol";

contract Setup {
    ShadowEmergency public shadowEmergency;

    address player;

    constructor(address _player) payable {
        require(msg.value == 11 ether, "Setup: Invalid ether amount");
        player = _player;

        shadowEmergency = new ShadowEmergency();
        shadowEmergency.deposit{value: 10 ether}();

        player.call{value: 1 ether}("");
    }

    function isSolved() external view returns (bool) {
        return player != address(0) && address(shadowEmergency).balance == 0;
    }
}
