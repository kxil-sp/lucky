# speedrun.py

import socket
import re
import time

HOST = "154.57.164.81"
PORT = 30415

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
    # 40-length hex = SHA1
    match = re.findall(r"\b[a-f0-9]{40}\b", text)
    return match


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            data = recv(s, timeout=5)
            if not data:
                break

            print("📥", data)

            hashes = find_hash(data)

            if hashes:
                for h in hashes:
                    print(f"📤 Sending: {h}")
                    s.sendall((h + "\n").encode())
            else:
                # fallback (enter)
                s.sendall(b"\n")

            if "flag" in data.lower():
                print("🏁 FLAG FOUND!")
                break


if __name__ == "__main__":
    main()
