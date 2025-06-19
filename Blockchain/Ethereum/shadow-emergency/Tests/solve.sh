export SETUP=0x499DF9b02881f4B9764cbc718e0426e7B52fe7de
export PRIV=0x224e196e66ddd30a37783b8a86bfa8bf56f4708870430d670ee6d05a2bd1480f  
export RPC_URL=http://localhost:8545/e6e96548-5b13-4003-b0cd-ed8a9b3c17b1

forge script script/Solve.s.sol --rpc-url $RPC_URL --tc Solve  -vvvvv --broadcast