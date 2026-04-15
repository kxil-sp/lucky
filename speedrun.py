# speedrun.py

import socket
import re
import time
import hashlib

HOST = "154.57.164.81"
PORT = 30415

# oddiy wordlist (kengaytirsa bo‘ladi)
WORDLIST = [
    "hello", "world", "test", "admin", "password",
    "123456", "qwerty", "flag", "ctf", "secret"
]

def recv(sock, timeout=3):
    sock.setblocking(0)
    data = b""
    start = time.time()

    while True:
        if time.time() - start > timeout:
            break
        try:
            part = sock.recv(4096)
            if part:
                data += part
                start = time.time()
        except:
            pass

    return data.decode(errors="ignore")


def find_hash(text):
    return re.findall(r"\b[a-f0-9]{40}\b", text)


def crack_sha1(hash_value):
    for word in WORDLIST:
        if hashlib.sha1(word.encode()).hexdigest() == hash_value:
            return word
    return None


def main():
    print(f"🔌 Connecting to {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))

        while True:
            data = recv(s, timeout=5)
            if not data:
                break

            print("📥", data)

            hashes = find_hash(data)

            if hashes:
                for h in hashes:
                    print(f"🔍 Found hash: {h}")

                    # 1. Avval crack qilib ko‘ramiz
                    cracked = crack_sha1(h)

                    if cracked:
                        print(f"🔓 Cracked: {cracked}")
                        s.sendall((cracked + "\n").encode())
                    else:
                        # 2. Bo‘lmasa echo qilib yuboramiz
                        print(f"📤 Sending raw hash")
                        s.sendall((h + "\n").encode())
            else:
                # fallback
                s.sendall(b"\n")

            if "flag" in data.lower():
                print("🏁 FLAG FOUND!")
                break


if __name__ == "__main__":
    main()
