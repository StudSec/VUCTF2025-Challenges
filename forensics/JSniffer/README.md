# JSniffed Challenge Writeup

## Step 1: Initial Analysis of the PCAP File

When examining the handout PCAP file, we can identify two important pieces of information:
- A hidden base64 encoded message and password at the bottom of `decoy.html`
- A suspicious page visit to `def_not_malware.html`

Let's extract the ZIP file from the traffic:

```python
from scapy.all import *

packets = rdpcap("JSniffer.pcapng")
sessions = packets.sessions()
http_payload = b""

for session in sessions.values():
    stream = b""
    for pkt in session:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            stream += bytes(pkt[Raw].load)

    if b"GET /def_not_malware.html" in stream:
        lines = stream.split(b"\r\n")
        host_line = next((line for line in lines if line.startswith(b"Host:")), None)
        if host_line:
            host = host_line.split(b" ", 1)[1].strip()
        continue

    if b"PK\x03\x04" in stream:
        http_payload = stream
        break

zip_start = http_payload.find(b"PK\x03\x04")
if zip_start == -1:
    raise ValueError("ZIP header (PK) not found in HTTP response.")

zip_data = http_payload[zip_start:]

with open("extracted.zip", "wb") as f:
    f.write(zip_data)

print("ZIP file extracted as 'extracted.zip'")
```

After extracting the ZIP file, we need to unzip it using the password found in `decoy.html`:
```bash
unzip extracted.zip # Password: VeryVUSecretPassword33_m4lWar3
```

## Step 2: Analyzing the Traffic for JavaScript Malware

Opening the traffic file in Wireshark reveals a suspicious webpage with unusual HTML content. The page appears to contain obfuscated JavaScript with emoji patterns that need to be replaced to reveal the actual code.

Let's extract the HTML content first:

```python
from scapy.all import *

packets = rdpcap("traffic.pcapng")
sessions = packets.sessions()
http_payload = b""

for session in sessions.values():
    stream = b""
    for pkt in session:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            stream += bytes(pkt[Raw].load)

    if b"GET /index.html" in stream:
        lines = stream.split(b"\r\n")
        host_line = next((line for line in lines if line.startswith(b"Host:")), None)
        if host_line:
            host = host_line.split(b" ", 1)[1].strip()
        continue

    if b"\x48\x54\x54\x50" in stream:
        http_payload = stream
        break

start = http_payload.find(b"\xf0\x9f\x8c\xae\x21\x44\x4f\x43")
html_data = http_payload[start:]

with open("extracted.html", "wb") as f:
    f.write(html_data)

print("HTML content extracted as 'extracted.html'")
```

## Step 3: Deobfuscating the JavaScript

After analyzing the HTML content, we discovered that certain emoji patterns need to be replaced to reveal the actual JavaScript code:

| Emoji | Replacement |
|-------|-------------|
| 😇     | U           |
| 🥷     | Y           |
| 🐢     | p           |
| 🐟     | s           |
| 🌮     | <           |

Let's create a script to perform these replacements:

```python
with open('extracted.html', 'rb') as f:
    data = f.read()

# Replace emojis with specific characters
data = data.replace('😇'.encode('utf-8'), b'U')
data = data.replace('🥷'.encode('utf-8'), b'Y')
data = data.replace('🐢'.encode('utf-8'), b'p')
data = data.replace('🐟'.encode('utf-8'), b's')
data = data.replace('🌮'.encode('utf-8'), b'<')

# Write cleaned data to a new file
with open('cleaned_page.html', 'wb') as f:
    f.write(data)

print("File 'cleaned_page.html' has been created with emoji replacements.")
```

After replacing the emojis, we need to base64 decode and URL decode the content. Using an online deobfuscator like [https://deobfuscate.relative.im/](https://deobfuscate.relative.im/), we obtain the following JavaScript code:

```javascript
function MalwareKey(_0x91cc53) {
  if (typeof _0x91cc53 !== 'string') {
    return false
  }
  if (_0x91cc53.length !== 32) {
    return false
  }
  const _0x40d4fc = [2, 3, 5, 7, 11, 13]
  function _0x32e4bf(_0x5148ca) {
    let _0x1ac593 = _0x5148ca.split(''),
      _0xf05a69 = _0x1ac593.map((_0x42a2c1, _0x1a9a36) => {
        let _0x161530 = _0x40d4fc[_0x1a9a36 % _0x40d4fc.length]
        return String.fromCharCode(
          _0x42a2c1.charCodeAt(0) ^ (_0x161530 + _0x1a9a36)
        )
      })
    for (let _0x23e5bf = 0; _0x23e5bf < _0xf05a69.length; _0x23e5bf += 4) {
      let _0x44a780 = _0xf05a69[_0x23e5bf]
      for (let _0x3478c6 = 0; _0x3478c6 < 3; _0x3478c6++) {
        _0xf05a69[_0x23e5bf + _0x3478c6] = _0xf05a69[_0x23e5bf + _0x3478c6 + 1]
      }
      _0xf05a69[_0x23e5bf + 3] = _0x44a780
    }
    let _0x4726df = _0xf05a69.join(''),
      _0x1abe54 = btoa(_0x4726df),
      _0x53eb3e = _0x1abe54.split('').reverse().join(''),
      _0x4b4231 = ''
    for (let _0x5f1164 of _0x53eb3e) {
      _0x4b4231 += _0x5f1164.charCodeAt(0).toString(16).padStart(2, '0')
    }
    return _0x4b4231
  }
  return (
    _0x32e4bf(_0x91cc53) ===
    '3d5178585a7856655142306271306b517952455a6b6758657a46324953525849396c5557696c475665525555'
  )
}
```

## Step 4: Reversing the Algorithm to Get the Flag

Now that we understand the algorithm, we need to reverse it to find the original input (our flag):

1. The algorithm performs several transformations:
   - XOR each character with a value based on prime numbers
   - Left rotate every 4 bytes
   - Base64 encode
   - Reverse the string
   - Convert to hexadecimal

Let's write a function to reverse these steps:

```javascript
function reversed_algo(hex) {
    // Step 1: Hex decode
    let reversedB64 = '';
    for (let i = 0; i < hex.length; i += 2) {
        reversedB64 += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }

    // Step 2: Reverse the Base64 string
    let b64 = reversedB64.split('').reverse().join('');
    let xoredStr = atob(b64); // Base64 decode

    // Step 3: Reverse the circular rotation (right rotate every 4 bytes)
    let chars = xoredStr.split('');
    for (let i = 0; i < chars.length; i += 4) {
        if (i + 3 < chars.length) {
            let tmp = chars[i + 3];
            for (let j = 3; j > 0; j--) {
                chars[i + j] = chars[i + j - 1];
            }
            chars[i] = tmp;
        }
    }

    // Step 4: Reverse XOR with prime numbers
    const primes = [2, 3, 5, 7, 11, 13];
    let original = chars.map((char, i) => {
        if (!char) throw new Error(`char undefined at index ${i}`);
        let key = primes[i % primes.length];
        return String.fromCharCode(char.charCodeAt(0) ^ (key + i));
    });

    return original.join('');
}

const expectedDigest = "3d5178585a7856655142306271306b517952455a6b6758657a46324953525849396c5557696c475665525555";
console.log(reversed_algo(expectedDigest));
```

Running this code reveals the flag: `VUCTF{jS_m4lw3re_f0r3ncics_r3vy}`

## Flag

The flag is: `VUCTF{jS_m4lw3re_f0r3ncics_r3vy}`

This can be verified by using the original `MalwareKey` function:
```javascript
MalwareKey("VUCTF{jS_m4lw3re_f0r3ncics_r3vy}") // Returns true
```