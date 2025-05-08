# Use a lightweight base image
FROM ubuntu:22.04

# Install necessary packages
RUN apt update && apt install -y gcc socat

# Create a working directory
WORKDIR /challenge

# Copy the challenge
COPY challenge .

# Expose the port, this does not actually mean the port is automatically exposed, that's done in the docker-compose
EXPOSE 1234

# Run socat to expose the binary
CMD ["socat", "TCP-LISTEN:1234,reuseaddr,fork", "EXEC:/challenge/challenge,stderr"]