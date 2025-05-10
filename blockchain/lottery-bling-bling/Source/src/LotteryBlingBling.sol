// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

contract LotteryBlingBling {
    address public lastWinner;
    uint256 public ticketPrice;
    address[] public players;
    bool public winnerPicked = false;

    event TicketPurchased(address indexed player);
    event WinnerPicked(address indexed winner, uint256 prize);

    constructor(uint256 _ticketPrice) {
        ticketPrice = _ticketPrice;
    }

    function buyTicket() public payable {
        require(
            msg.value == ticketPrice,
            "LotteryBlingBling: Incorrect ticket price"
        );
        players.push(msg.sender);
        emit TicketPurchased(msg.sender);
    }

    function pickWinner() public {
        require(
            players.length > 0,
            "LotteryBlingBling: No players in the lottery"
        );

        require(
            !winnerPicked,
            "LotteryBlingBling: The winner has already been picked"
        );

        uint256 randomIndex = uint256(
            keccak256(
                abi.encodePacked(
                    block.timestamp,
                    block.difficulty,
                    block.number,
                    gasleft()
                )
            )
        ) % players.length;
        lastWinner = players[randomIndex];

        uint256 prize = address(this).balance;
        (bool success, ) = lastWinner.call{value: prize}("");

        emit WinnerPicked(lastWinner, prize);
        winnerPicked = true;

        delete players;
    }

    function getPlayers() public view returns (address[] memory) {
        return players;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
