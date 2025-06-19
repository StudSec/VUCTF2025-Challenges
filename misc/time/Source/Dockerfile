FROM ubuntu:22.04

RUN apt update && apt install -y socat gcc make coreutils

RUN useradd -m ctf
WORKDIR /home/ctf

COPY time /home/ctf/run
COPY flag.txt /home/ctf/flag.txt

RUN chmod 400 /home/ctf/flag.txt && \
    chmod +x /home/ctf/run && \
    chown -R ctf:ctf /home/ctf

USER ctf

EXPOSE 6969

CMD socat TCP-LISTEN:6969,reuseaddr,fork EXEC:/home/ctf/run,stderr
