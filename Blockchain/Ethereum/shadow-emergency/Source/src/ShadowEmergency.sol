pragma solidity 0.8.28;

contract ShadowEmergency {
    mapping(address => uint256) public balance;

    event Withdrawal(address indexed user, uint256 amount);
    event Deposit(address indexed user, uint256 amount);

    function deposit() public payable {
        require(
            msg.value > 0,
            "ShadowEmergency: Deposit an amount greater than 0"
        );
        balance[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 _amount) public {
        require(
            _amount <= balance[msg.sender],
            "ShadowEmergency: Insufficient balance"
        );

        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "ShadowEmergency: Withdrawal failed");

        balance[msg.sender] -= _amount;
        emit Withdrawal(msg.sender, _amount);
    }

    function checkBalance() public view returns (uint256) {
        return balance[msg.sender];
    }

    function transfer(address _to, uint256 _amount) public {
        require(
            _amount <= balance[msg.sender],
            "ShadowEmergency: Insufficient balance"
        );
        require(_to != address(0), "ShadowEmergency: Invalid address");

        balance[msg.sender] -= _amount;
        balance[_to] += _amount;
    }

    function emergencyWithdrawal() public {
        uint256 _balance = balance[msg.sender];
        require(_balance > 0, "ShadowEmergency: No balance to withdraw");

        (bool success, ) = msg.sender.call{value: _balance}("");
        require(success, "ShadowEmergency: Emergency withdrawal failed");

        balance[msg.sender] = 0;
        emit Withdrawal(msg.sender, _balance);
    }
}
