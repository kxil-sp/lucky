# speedrun.py

import socket
import time

HOST = "154.57.164.81"   # <-- bu yerga server IP yoki domain yozasiz
PORT = 30415            # <-- kerakli port

def main():
    print("🚀 Starting speedrun with socket...")

    start = time.time()

    try:
        # Socket yaratish
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"🔌 Connecting to {HOST}:{PORT} ...")
            s.connect((HOST, PORT))

            # So'rov yuborish (HTTP example)
            request = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
            s.sendall(request.encode())

            # Javobni olish
            response = s.recv(4096)

            print("📩 Response received:")
            print(response.decode(errors="ignore"))

    except Exception as e:
        print(f"❌ Error: {e}")

    end = time.time()

    print(f"⏱ Time taken: {end - start:.4f} seconds")


if __name__ == "__main__":
    main()
