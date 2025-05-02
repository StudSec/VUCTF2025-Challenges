
# Use an official lightweight image with build tools
FROM ubuntu:latest

# Install build-essential for make, gcc, etc.
RUN apt update
RUN apt install -y build-essential gcc-mips-linux-gnu
RUN apt install -y gdb-multiarch
RUN apt install -y qemu-user

# Default command (can be overridden by docker-compose)
WORKDIR /src

CMD ["/bin/bash"]

