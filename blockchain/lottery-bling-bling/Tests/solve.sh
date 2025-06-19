export SETUP=0xceA21CE10BDFc950dd7172752cba9Af3117824b1
export PRIV=0xe944d6fd5c28822b4ce7ed3f75d262ba2bf81ca4782258769630486731bdcac3  
export RPC_URL=http://localhost:8545/234ecc11-b732-4496-bd65-7bb6bd95fa12

forge script script/Solve.s.sol --rpc-url $RPC_URL --tc Solve  -vvvvv
