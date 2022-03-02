import socket
import webbrowser

while True:
    try:
        piIP = socket.gethostbyname("raspberrypi.local")
        break
    except Exception as e:
        print(e)
        print("retrying...")

print(piIP)
webbrowser.open("http://" + str(piIP) + ":5000/")