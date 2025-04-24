import json
from pathlib import Path

import eth_sandbox
from web3 import Web3


def deploy(web3: Web3, deployer_address: str, player_address: str) -> str:
    setup_json = json.loads(Path("/home/ctf/compiled/Setup.sol/Setup.json").read_text())
    bytecode = setup_json["bytecode"]["object"]
    abi = setup_json["abi"]

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    txn = contract.constructor(player_address).build_transaction({
        "from": deployer_address,
        "gas": 3000000,
        "gasPrice": 0,
        "nonce": web3.eth.get_transaction_count(deployer_address),
        "value": 1 * 10**18,
    })

    rcpt = eth_sandbox.sendTransaction(web3, txn)
    return rcpt.contractAddress



eth_sandbox.run_launcher(
    [
        eth_sandbox.new_launch_instance_action(deploy),
        eth_sandbox.new_kill_instance_action(),
        eth_sandbox.new_get_flag_action(),
    ]
)
