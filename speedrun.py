# speedrun.py

import socket
import time

HOST = "154.57.164.81"
PORT = 30415

def recv_until_timeout(sock, timeout=3):
    sock.setblocking(0)
    data = b""
    start = time.time()

    while True:
        if time.time() - start > timeout:
            break
        try:
            chunk = sock.recv(4096)
            if chunk:
                data += chunk
                start = time.time()  # reset timeout if data comes
        except:
            pass

    return data.decode(errors="ignore")


def main():
    print(f"🔌 Connecting to {HOST}:{PORT} ...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))

        # 1. Server banner / savol
        banner = recv_until_timeout(s, timeout=5)
        print("📥 Server:")
        print(banner)

        # 2. Agar hash ko‘rsak → yuboramiz
        if "a26af69be951a213d495a4c3e4e4022e16d87065" in banner:
            payload = "a26af69be951a213d495a4c3e4e4022e16d87065\n"
            print(f"📤 Sending hash...")
            s.sendall(payload.encode())

        # 3. Generic input (ba'zi challar ENTER kutadi)
        s.sendall(b"\n")

        # 4. Javobni olish
        response = recv_until_timeout(s, timeout=5)
        print("📩 Response:")
        print(response)

        # 5. Flag check
        if "flag" in response.lower():
            print("🏁 FLAG FOUND!")
        else:
            print("❌ Flag topilmadi (yana step bo‘lishi mumkin)")


if __name__ == "__main__":
    main()
