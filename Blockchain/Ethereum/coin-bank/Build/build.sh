#!/bin/bash

# Ensure the script exits on error
set -e

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --source-path)
            SOURCE_PATH="$2"
            shift 2
            ;;
        --handout-path)
            HANDOUT_PATH="$2"
            shift 2
            ;;
        --flag)
            # Skip flag implementation
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Validate arguments
if [[ -z "$SOURCE_PATH" || -z "$HANDOUT_PATH" ]]; then
    echo "Usage: build.sh --source-path <path> --handout-path <path>"
    exit 1
fi

# Navigate to source directory
cd "$SOURCE_PATH"

# Ensure Foundry is installed
if ! command -v forge &> /dev/null; then
    echo "Forge is not installed. Please install Foundry before running this script."
    exit 1
fi

# Install dependencies and build
forge install OpenZeppelin/openzeppelin-contracts --no-commit
forge build
forge clean

# Copy build output to the handout path
rm -rf "$HANDOUT_PATH/src"
cp -r "$SOURCE_PATH/src" "$HANDOUT_PATH/src"

echo "Build completed successfully!"
exit 0
