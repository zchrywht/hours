from gpiozero import MCP3008
import time


def analogRead():
    a0 = MCP3008(0)
    a0 = a0.value
    rst = MCP3008(3)
    rst = rst.value
    #print(dir.value)
    print(a0)
    print(rst)

    if a0 < 0.1:
        return "R"
    elif a0 < 0.2:
        return "U"
    elif a0 < 0.5:
        return "D"
    elif a0 < 0.8:
        return "L"
    elif a0 < 1:
        return "S"
    elif rst < 0.005:
        return "E"
    else:
        return


def readKeypad():
    v1 = analogRead()
    if v1:
        time.sleep(0.1)
        v2 = analogRead()
        if v1 == v2:
            return v2
    else:
        return
    
while True:
    v = analogRead()
    if v:
        print(v)
    time.sleep(0.5)