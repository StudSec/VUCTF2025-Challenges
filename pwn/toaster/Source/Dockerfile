FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3 \
    python3-pip \
    openssh-server \
    libssl-dev \
    libffi-dev \
    build-essential \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install pwntools
RUN pip3 install pwntools

# Create SSH user
RUN useradd -ms /bin/bash vuctf && \
    echo 'vuctf:pwnChallToaster' | chpasswd

# Add challenge files
COPY toaster.c /root/
COPY flag.txt /flag.txt

# Setup SSH
RUN mkdir /var/run/sshd && \
    echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Compile and move the SUID binary
RUN gcc /root/toaster.c -o /root/toaster -fno-stack-protector && \
    chmod 4755 /root/toaster && \
    chown root:root /root/toaster && \
    mv /root/toaster /home/vuctf/toaster && \
    chmod 755 /home/vuctf/toaster && \
    rm /root/toaster.c

# Secure flag
RUN chown root:root /flag.txt && chmod 400 /flag.txt

# Restrict user access
RUN echo "exec /bin/bash --noprofile --norc" > /home/vuctf/.bashrc

# Set proper ownership of home
RUN chown -R vuctf:vuctf /home/vuctf
RUN chown root:root /home/vuctf/toaster
RUN chmod u+s /home/vuctf/toaster

# Expose SSH
EXPOSE 22

# Run SSH
CMD ["/usr/sbin/sshd", "-D"]
