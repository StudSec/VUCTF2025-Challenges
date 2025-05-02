# Use an official lightweight image with build tools
FROM ubuntu:latest

# Install build-essential for make, gcc, etc.
RUN apt-get update -y && apt-get -y upgrade
RUN apt-get install -y build-essential
RUN apt-get install -y gcc-11-mips-linux-gnu python3

COPY cross_cmp_tools /tools/

# Default command (can be overridden by docker-compose)
WORKDIR /src

CMD ["make"]
#CMD ["/bin/bash"]
