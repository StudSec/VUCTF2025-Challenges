FROM pwn.red/jail
COPY --from=ubuntu:24.04 / /srv
COPY chall /srv/app/run
COPY flag.txt /srv/app/flag.txt
ENV JAIL_PORT=1569
