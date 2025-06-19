pragma solidity 0.8.28;

import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract BetterVersion is Initializable, OwnableUpgradeable, UUPSUpgradeable {
    int public challenge_version = 1;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize(address initialOwner) public initializer {
        __Ownable_init(initialOwner);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address newImplementation) internal override {}

    receive() external payable {}

    fallback() external payable {}

    function withdraw(uint amount) external {
        require(msg.sender == owner(), "Only owner can withdraw");
        require(address(this).balance >= amount, "Insufficient balance");
        address(msg.sender).call{value: amount}("");
    }

    function updateVersion(int newVersion) external {
        challenge_version = newVersion;
    }
}
