// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import "./UUPSProxy.sol";
import "./BetterVersion.sol";

contract Setup {
    BetterVersion public betterVersion;
    UUPSProxy public proxy;
    address public player;

    constructor(address _player) payable {
        require(msg.value == 1 ether, "Setup: Invalid ether amount");
        player = _player;

        BetterVersion logic = new BetterVersion();

        bytes memory data = abi.encodeWithSelector(
            BetterVersion.initialize.selector,
            address(this)
        );

        proxy = new UUPSProxy(address(logic), data);
        betterVersion = BetterVersion(payable(address(proxy)));
        payable(address(betterVersion)).transfer(1 ether);
    }

    function isSolved() external view returns (bool) {
        return player != address(0) && address(betterVersion).balance == 0;
    }
}
