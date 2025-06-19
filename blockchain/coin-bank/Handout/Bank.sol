pragma solidity 0.8.28;

import {Coin} from "./Coin.sol";
interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function allowance(
        address owner,
        address spender
    ) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);
}

contract Bank {
    mapping(address owner => uint) public balance;

    Coin public coin;

    constructor(Coin _coin) {
        coin = _coin;
    }

    function depositFor(address _coin, address receiver, uint amount) external {
        balance[receiver] += amount;
        IERC20(_coin).transferFrom(msg.sender, address(this), amount);
    }

    function withdraw(address _coin, uint amount) external {
        balance[msg.sender] -= amount;
        IERC20(_coin).transfer(msg.sender, amount);
    }
}
