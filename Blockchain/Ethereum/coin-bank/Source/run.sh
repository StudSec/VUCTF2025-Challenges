#!/bin/bash

# Default values for optional parameters
HOSTNAME="localhost"
RPC_PORT=8545
NC_PORT=1337
FLAG="CTF{1_l0v3_f4k3_c0in5}"

# Parse named arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --hostname)
            HOSTNAME="$2"; shift 2;;
        --port)
            RPC_PORT="$2"; shift 2;;
        --nc-port)
            NC_PORT="$2"; shift 2;;
        --flag)
            FLAG="$2"; shift 2;;
        --help)
            echo "Usage: ./run.sh --hostname HOSTNAME --port PORT --flag FLAG"
            echo "  --hostname   Hostname to bind the service (default: localhost)"
            echo "  --rpc-port       Port to expose the rpc http server (default: 8545)"
            echo "  --nc-port       Port to expose the nc service (default: 1337)"
            echo "  --flag       Flag to set in the container (required)"
            exit 0;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./run.sh --hostname HOSTNAME --port PORT --flag FLAG"
            exit 1;;
    esac
done

# Check if required arguments are provided
if [ -z "$FLAG" ]; then
    echo "Error: --flag argument is required."
    echo "Usage: ./run.sh --hostname HOSTNAME --rpc-port PORT --nc-port PORT --flag FLAG"
    exit 1
fi

# Build and run the Docker container
export HOSTNAME=$HOSTNAME
export RPC_PORT=$RPC_PORT
export NC_PORT=$NC_PORT
export FLAG=$FLAG
docker compose up --build -d
echo "Challenge running on $HOSTNAME:$PORT & $HOSTNAME:$NC_PORT with flag: $FLAG"