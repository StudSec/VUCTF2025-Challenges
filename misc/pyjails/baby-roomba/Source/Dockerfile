FROM ubuntu:22.04

RUN apt install -y socat python2

WORKDIR /app
COPY baby-roomba.py .

EXPOSE 1337

ENTRYPOINT [ \
    "socat", \
    "TCP-LISTEN:1337,reuseaddr,fork", \
    "EXEC:/usr/bin/python2 /app/baby-roomba-cnc.py,pty,stderr" \
    ]
