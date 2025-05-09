FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python2 socat && \
    ln -s /usr/bin/python2 /usr/bin/python

WORKDIR /app
COPY baby-roomba.py .

EXPOSE 1337

ENTRYPOINT [ \
    "socat", \
    "TCP-LISTEN:1337,reuseaddr,fork", \
    "EXEC:/usr/bin/python2 /app/baby-roomba.py,pty,stderr" \
    ]
