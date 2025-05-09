from os import system
from time import sleep

# Turn off the PWR LED
system("echo 0 > /sys/class/leds/PWR/brightness")
sleep(2)
# Turn on the PWR LED
system("echo 255 > /sys/class/leds/PWR/brightness")
