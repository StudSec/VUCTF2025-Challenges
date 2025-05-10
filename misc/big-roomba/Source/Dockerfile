FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y socat python3

WORKDIR /app
COPY big-roomba.py .

EXPOSE 1337

ENTRYPOINT [ \
    "socat", \
    "TCP-LISTEN:1337,reuseaddr,fork", \
    "EXEC:/usr/bin/python3 /app/big-roomba.py,pty,stderr" \
    ]
