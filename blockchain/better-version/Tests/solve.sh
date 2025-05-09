export SETUP=0x3Aa70756A09d3ee7b72189daC8EBFe8bc9872ed6
export PRIV=0xc9e3283999a6e2fae706bdd13e1aa70af7a3c5b8681f750b135223c1afb6ad57  
export RPC_URL=http://localhost:8545/dbcdf6f7-09fb-4071-acb3-d70428f55892

forge script script/Solve.s.sol:Solve --rpc-url $RPC_URL --tc Solve  -vvvvv --broadcast