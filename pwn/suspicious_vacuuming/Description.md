##The challenge:
To stop the chaos, the head of StudSec Infrastructure has deployed a new Roomba Intrusion Detection System 
(RIDS) — a high-performance BPFtrace-based sensor suite meant to detect and log suspicious vacuuming behavior on a machine.
However, the head of studsec has left their laptop open.

Your objective is /etc/shadow

## further details:
You may assume `cat /etc/shadow > /dev/null` is frequently called to mimic the head of studsec `sudo <cmd>` behaviour.
Please do not hesitate to ask any bpftrace tips.
