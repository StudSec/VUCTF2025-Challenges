pragma solidity 0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Coin is ERC20 {
    constructor() ERC20("Coin", "COIN") {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
