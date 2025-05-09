#!/bin/bash

whoami

while true; do
    socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -oL ./roomba_ids",stderr
done

